from flask import Flask
from flask_cors import CORS
from models import db
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

from auth import bp as auth_bp
from doctors import bp as doctors_bp
from appointments import bp as appt_bp
from payments import bp as payments_bp
from video import bp as video_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(doctors_bp, url_prefix='/api/doctors')
app.register_blueprint(appt_bp, url_prefix='/api/appointments')
app.register_blueprint(payments_bp, url_prefix='/api/payments')
app.register_blueprint(video_bp, url_prefix='/api/video')

@app.route('/api/health')
def health():
    return {'status': 'ok'}

if __name__ == '__main__':
    port = int(os.getenv('FLASK_RUN_PORT', 4000))
    app.run(debug=True, host='0.0.0.0', port=port)
