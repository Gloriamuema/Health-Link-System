from flask import Blueprint, request, jsonify, current_app
import stripe
import os
from models import db, Payment, Appointment
from _auth_helpers import login_required

bp = Blueprint('payments', __name__)
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@bp.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session(current_user):
    body = request.get_json() or {}
    appointment_id = body.get('appointment_id')
    amount = body.get('amount')  # amount in currency units, e.g., 20.0
    currency = body.get('currency', 'usd')

    if not appointment_id or not amount:
        return jsonify({'message': 'appointment_id and amount required'}), 400

    # Create Stripe checkout session
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='payment',
            line_items=[{
                'price_data': {
                    'currency': currency,
                    'product_data': {
                        'name': 'Consultation Fee',
                    },
                    'unit_amount': int(float(amount) * 100),  # cents
                },
                'quantity': 1,
            }],
            metadata={'appointment_id': str(appointment_id), 'user_id': str(current_user.id)},
            success_url=os.getenv('FRONTEND_SUCCESS_URL', 'http://localhost:5173/payment-success?session_id={CHECKOUT_SESSION_ID}'),
            cancel_url=os.getenv('FRONTEND_CANCEL_URL', 'http://localhost:5173/payment-cancel'),
        )
        # create or update Payment record (status pending)
        p = Payment(user_id=current_user.id, appointment_id=appointment_id, amount=amount, status='pending', provider='stripe', metadata={'session_id': session.id})
        db.session.add(p)
        db.session.commit()
        return jsonify({'sessionId': session.id, 'checkout_url': session.url})
    except Exception as e:
        current_app.logger.exception(e)
        return jsonify({'message': 'stripe error', 'error': str(e)}), 500
