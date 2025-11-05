from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import enum

db = SQLAlchemy()

class Role(enum.Enum):
    PATIENT = 'patient'
    DOCTOR = 'doctor'
    ADMIN = 'admin'

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(120))
    role = db.Column(db.Enum(Role), default=Role.PATIENT)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    doctor_profile = db.relationship('DoctorProfile', uselist=False, back_populates='user')

class DoctorProfile(db.Model):
    __tablename__ = 'doctor_profile'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    specialties = db.Column(db.String(300))
    bio = db.Column(db.Text)
    experience_years = db.Column(db.Integer)
    consultation_fee = db.Column(db.Float, default=0.0)
    location = db.Column(db.String(200))
    rating = db.Column(db.Float, default=0.0)

    user = db.relationship('User', back_populates='doctor_profile')
    availability = db.relationship('AvailabilitySlot', back_populates='doctor')

class AvailabilitySlot(db.Model):
    __tablename__ = 'availability_slot'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor_profile.id'))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    is_booked = db.Column(db.Boolean, default=False)

    doctor = db.relationship('DoctorProfile', back_populates='availability')

class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor_profile.id'), nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='scheduled')  # scheduled, completed, cancelled
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship('User', foreign_keys=[patient_id])
    doctor = db.relationship('DoctorProfile', foreign_keys=[doctor_id])

class Prescription(db.Model):
    __tablename__ = 'prescription'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Float)
    currency = db.Column(db.String(10), default='USD')
    provider = db.Column(db.String(50))  # e.g., 'stripe'
    status = db.Column(db.String(50))
    extra_data = db.Column(db.JSON)  # renamed from metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
