from flask import Blueprint, request, jsonify
from models import db, Appointment, AvailabilitySlot, Payment, DoctorProfile, User
from _auth_helpers import login_required
from datetime import datetime
import stripe
import os

bp = Blueprint('appointments', __name__)

@bp.route('/', methods=['GET'])
def list_appointments():
    items = Appointment.query.order_by(Appointment.scheduled_time.desc()).all()
    return jsonify([{
        'id': a.id,
        'patient_id': a.patient_id,
        'doctor_id': a.doctor_id,
        'scheduled_time': a.scheduled_time.isoformat(),
        'status': a.status,
        'notes': a.notes
    } for a in items])

@bp.route('/book', methods=['POST'])
@login_required
def book_appointment(current_user):
    body = request.get_json() or {}
    doctor_id = body.get('doctor_id')
    slot_id = body.get('slot_id')      # optional: book by slot
    scheduled_time = body.get('scheduled_time')  # optional: ISO string
    pay = body.get('pay', False)

    if not doctor_id:
        return jsonify({'message': 'doctor_id required'}), 400

    # if slot provided, verify it's free
    if slot_id:
        slot = AvailabilitySlot.query.get(slot_id)
        if not slot or slot.is_booked:
            return jsonify({'message': 'slot not available'}), 400
        scheduled_time = slot.start_time
        slot.is_booked = True
    else:
        if not scheduled_time:
            return jsonify({'message': 'scheduled_time or slot_id required'}), 400
        scheduled_time = datetime.fromisoformat(scheduled_time)

    # create appointment row (patient is current_user)
    appt = Appointment(patient_id=current_user.id, doctor_id=doctor_id, scheduled_time=scheduled_time)
    db.session.add(appt)
    db.session.commit()

    # if doctor charges, optionally create a Payment record and return payment instructions
    doc = DoctorProfile.query.get(doctor_id)
    fee = doc.consultation_fee if doc else 0.0

    if fee and pay:
        # create a pending payment record
        payment = Payment(user_id=current_user.id, appointment_id=appt.id, amount=fee, status='pending', provider='stripe')
        db.session.add(payment)
        db.session.commit()
        return jsonify({'message': 'appointment created', 'appointment_id': appt.id, 'payment_id': payment.id, 'amount': fee}), 201

    return jsonify({'message': 'appointment created', 'appointment_id': appt.id}), 201
