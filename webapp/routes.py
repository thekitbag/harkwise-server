from flask import jsonify, request
import logging

from webapp import app, db
from webapp.models import Establishment, Rating

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
    name = data.get('name')
    email = data.get('email')
    
    print(name, email)
    
    # Handle data as needed, like storing it in a database
    
    return jsonify(status='success'), 200
