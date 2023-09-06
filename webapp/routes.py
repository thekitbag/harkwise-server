from flask import json, request, jsonify

from webapp import app, db
from webapp.models import Establishment, Rating

@app.route('/api/get_establishment_details/<int:establishment_id>', methods=['GET'])
def get_establishment_details(establishment_id):
    establishment = Establishment.query.get(establishment_id)
    if establishment:
        name = establishment.name
        return jsonify({'name': name})
    else:
        return jsonify({'error': 'Establishment not found'}), 404


@app.route('/api/review', methods=["POST"])
def review():
    data = json.loads(request.data.decode('utf-8'))
    establishment_id = data['establishmentId']
    rating = data['rating']
    comment = data['comment']

    e = Establishment.query.get(establishment_id)
    r = Rating(rating=rating, comment=comment)
    e.ratings.append(r)
    db.session.add_all([e,r])
    db.session.commit()

    return "Review Received"