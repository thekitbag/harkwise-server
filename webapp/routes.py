from flask import json, request

from webapp import app, db
from webapp.models import Establishment, Rating


@app.route('/api/review', methods=["POST"])
def review():
    data = json.loads(request.data.decode('utf-8'))
    establishment_name = data['establishmentName']
    rating = data['rating']
    comment = data['comment']

    e = Establishment(name=establishment_name)
    r = Rating(rating=rating, comment=comment)
    e.ratings.append(r)
    db.session.add_all([e,r])
    db.session.commit()

    return "Thanks for leaving a review"