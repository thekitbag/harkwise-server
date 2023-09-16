from flask import jsonify, request
import logging

from webapp import app, db
from webapp.models import Establishment, Rating, Interest

logging.basicConfig(level=logging.DEBUG)

@app.route('/api/get_establishment_details/<int:establishment_id>', methods=['GET'])
def get_establishment_details(establishment_id):
    """Retrieve establishment details by its ID."""
    print("request:", request.json)
    establishment = Establishment.query.get(establishment_id)
    print("establishment:", establishment)
    if establishment:
        return jsonify({'name': establishment.name})
    else:
        logging.warning(f"Establishment ID {establishment_id} not found")
        return jsonify({'error': 'Establishment not found'}), 404

@app.route('/api/review', methods=["POST"])
def review():
    """Save a review for an establishment."""
    data = request.json
    try:
        establishment_id = data['establishmentId']
        rating = data['rating']
        comment = data['comment']
    except KeyError as e:
        logging.error(f"Missing field in request data: {e}")
        return jsonify({'error': f"Missing field: {e}"}), 400
    
    establishment = Establishment.query.get(establishment_id)
    if not establishment:
        logging.error(f"Establishment ID {establishment_id} not found when adding review")
        return jsonify({'error': 'Establishment not found for the given review'}), 404

    r = Rating(rating=rating, comment=comment)
    establishment.ratings.append(r)
    db.session.add_all([establishment, r])
    db.session.commit()

    logging.info(f"Review added for Establishment ID {establishment_id}")
    return jsonify({'message': 'Review Received'})

@app.route('/api/interest', methods=['POST'])
def capture_interest():
    data = request.json

    if not data:
        logging.error("Received empty request data")
        return jsonify(error="Invalid data"), 400

    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        logging.error("Received incomplete data for capturing interest")
        return jsonify(error="Incomplete data. 'name' and 'email' are required."), 400

    existing_interest = Interest.query.filter_by(email=email).first()
    if existing_interest:
        logging.warning(f"Duplicate entry attempt for email: {email}")
        return jsonify(error="Email already registered"), 409

    interest = Interest(name=name, email=email)
    db.session.add(interest)
    db.session.commit()

    logging.info(f"Captured interest for name: {name}, email: {email}")
    return jsonify(status='success'), 200
