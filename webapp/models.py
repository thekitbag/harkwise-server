from webapp import db

class Establishment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    establishment_type = db.Column(db.String(64))
    name = db.Column(db.String(120))
    ratings = db.relationship('Rating', backref='establishment', lazy='dynamic')

    def __repr__(self):
        return f'<Establishment {self.id}>'

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    comment = db.Column(db.String(160))
    establishment_id = db.Column(db.Integer, db.ForeignKey('establishment.id'))

    def __repr__(self):
        return f'<Rating {self.id}>'