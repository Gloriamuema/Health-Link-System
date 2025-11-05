from flask import Blueprint, request, jsonify
from models import db, DoctorProfile, User, AvailabilitySlot, Role
from sqlalchemy import or_

bp = Blueprint('doctors', __name__)

@bp.route('/', methods=['GET'])
def list_doctors():
    q = request.args.get('q','')
    location = request.args.get('location','')
    page = int(request.args.get('page', '1'))
    per = int(request.args.get('per', '20'))

    query = DoctorProfile.query.join(User).filter(User.role == Role.DOCTOR)
    if q:
        pattern = f"%{q}%"
        query = query.filter(or_(DoctorProfile.specialties.ilike(pattern), User.name.ilike(pattern)))
    if location:
        query = query.filter(DoctorProfile.location.ilike(f"%{location}%"))
    docs = query.offset((page-1)*per).limit(per).all()
    return jsonify([{
        'id': d.id,
        'name': d.user.name,
        'specialties': d.specialties,
        'location': d.location,
        'fee': d.consultation_fee,
        'rating': d.rating
    } for d in docs])

@bp.route('/<int:id>', methods=['GET'])
def doctor_detail(id):
    d = DoctorProfile.query.get_or_404(id)
    slots = AvailabilitySlot.query.filter_by(doctor_id=d.id, is_booked=False).order_by(AvailabilitySlot.start_time).limit(50).all()
    return jsonify({
        'id': d.id,
        'name': d.user.name,
        'specialties': d.specialties,
        'bio': d.bio,
        'fee': d.consultation_fee,
        'rating': d.rating,
        'location': d.location,
        'slots': [{'id': s.id, 'start': s.start_time.isoformat(), 'end': s.end_time.isoformat()} for s in slots]
    })

@bp.route('/<int:id>/availability', methods=['POST'])
def add_slot(id):
    # For simplicity: anyone can add. In production guard by doctor's auth.
    body = request.get_json() or {}
    start = body.get('start')
    end = body.get('end')
    if not start or not end:
        return jsonify({'message': 'start and end required'}), 400
    slot = AvailabilitySlot(doctor_id=id, start_time=start, end_time=end)
    db.session.add(slot)
    db.session.commit()
    return jsonify({'message': 'slot added'}), 201
