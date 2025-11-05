from flask import Blueprint, jsonify, request
import os

bp = Blueprint('video', __name__)

@bp.route('/token', methods=['POST'])
def get_token():
    from twilio.jwt.access_token import AccessToken
    from twilio.jwt.access_token.grants import VideoGrant

    identity = request.json.get('identity', 'user')
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    api_key = os.getenv('TWILIO_API_KEY')
    api_secret = os.getenv('TWILIO_API_SECRET')

    if not all([account_sid, api_key, api_secret]):
        return jsonify({'message': 'Twilio not configured'}), 501

    token = AccessToken(account_sid, api_key, api_secret, identity=identity)
    token.add_grant(VideoGrant(room='telemedicine-room'))
    jwt_token = token.to_jwt().decode('utf-8')
    return jsonify({'token': jwt_token})
