from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
import logging
import time
import os

from webapp import app, db
from webapp.models import Establishment, Rating, Interest, CapturedEmail
from webapp.hubspot_gw import add_contact

logging.basicConfig(level=logging.DEBUG)
FLASK_ENV = os.environ.get('FLASK_ENV')


@app.route('/api/get_establishment_details/<int:establishment_id>', methods=['GET'])
def get_establishment_details(establishment_id):
    """Retrieve establishment details by its ID."""
    establishment = Establishment.query.get(establishment_id)
    print(establishment.capture_email)
    if establishment:
        return jsonify({
            'name': establishment.name,
            'publicReviewSites': establishment.publicReviewSites,
            'captureEmail': bool(establishment.capture_email),
            'logoURL': establishment.logo_url
        })
    else:
        logging.warning(f"Establishment ID {establishment_id} not found")
        return jsonify({'error': 'Establishment not found'}), 404


from flask import request, jsonify

@app.route('/api/review', methods=["POST"])
def review():
    """Save a review for an establishment."""
    data = request.json

    try:
        establishment_id = data['establishmentId']
        rating = data['rating']
        comment = data['comment']
        method = data['reviewMethod']
    except KeyError as e:
        logging.error(f"Missing field in request data: {e}")
        return jsonify({'error': f"Missing field: {e}"}), 400

    establishment = Establishment.query.get(establishment_id)
    if not establishment:
        logging.error(f"Establishment ID {establishment_id} not found when adding review")
        return jsonify({'error': 'Establishment not found for the given review'}), 404

    r = Rating(rating=rating, comment=comment, method=method)
    establishment.ratings.append(r)
    db.session.add_all([establishment, r])
    db.session.commit()

    logging.info(f"Review added for Establishment ID {establishment_id} with method {method}")
    return jsonify({'message': 'Review Received'})


@app.route('/api/interest', methods=['POST'])
def capture_interest():
    if FLASK_ENV != 'prod' :
        time.sleep(5)  # simulating some processing delay

    data = request.json

    if not data:
        logging.error("Received empty request data")
        return jsonify(error="Invalid data"), 400

    firstName = data.get('firstName')
    lastName = data.get('lastName')
    businessName = data.get('businessName')
    email = data.get('email')
    phoneNumber = data.get('phoneNumber')

    if not firstName or not lastName or not email:
        logging.error("Received incomplete data for capturing interest")
        return jsonify(error="Incomplete data. 'firstName', 'lastName', and 'email' are required."), 400

    existing_interest = Interest.query.filter_by(email=email).first()
    if existing_interest:
        logging.warning(f"Duplicate entry attempt for email: {email}")
        return jsonify(error="Email already registered"), 409

    interest = Interest(firstName=firstName, lastName=lastName, businessName=businessName, email=email, phoneNumber=phoneNumber)
    db.session.add(interest)
    db.session.commit()

    logging.info(f"Captured interest for name: {firstName} {lastName}, email: {email}")

    add_contact(firstName=firstName, lastName=lastName, email=email, businessName=businessName, phoneNumber=phoneNumber)

    return jsonify(status='success'), 200


@app.route('/api/captured-emails', methods=['POST'])
def capture_email():
    data = request.json

    if not data or "email" not in data:
        return jsonify({'error': 'Email not provided'}), 400

    email_address = data["email"]
    establishment_id = int(data['establishmentId'])

    # Check if email already exists for the establishment
    existing_email = CapturedEmail.query.filter_by(email=email_address, establishment_id=establishment_id).first()
    if existing_email:
        return jsonify({'error': 'email_exists'}), 409

    new_email = CapturedEmail(email=email_address, establishment_id=establishment_id)

    try:
        db.session.add(new_email)
        db.session.commit()
    except IntegrityError:
        # Handle unique constraint violations or other database errors
        db.session.rollback()
        return jsonify({'error': 'Database error'}), 500

    return jsonify({'message': 'Email captured successfully'}), 201


