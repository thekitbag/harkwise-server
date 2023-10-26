from webapp import db
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import JSON

class CapturedEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    establishment_id = db.Column(db.Integer, db.ForeignKey('establishment.id'))
    captured_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CapturedEmail {self.email}>'

class Establishment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    establishment_type = db.Column(db.String(64))
    name = db.Column(db.String(120))
    ratings = db.relationship('Rating', backref='establishment', lazy='dynamic')
    emails = db.relationship('CapturedEmail', backref='establishment', lazy='dynamic')
    publicReviewSites = db.Column(JSON)
    capture_email = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Establishment {self.id}>'

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    comment = db.Column(db.String(160))
    establishment_id = db.Column(db.Integer, db.ForeignKey('establishment.id'))
    timestamp = db.Column(DateTime, default=datetime.utcnow)  # New column for timestamp


    def __repr__(self):
        return f'<Rating {self.id}>'

class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(120), nullable=False)
    lastName = db.Column(db.String(120), nullable=False)
    businessName = db.Column(db.String(250)) 
    email = db.Column(db.String(120), unique=True, nullable=False)
    phoneNumber = db.Column(db.String(20))  

    def __repr__(self):
        return f'<Interest {self.id}>'