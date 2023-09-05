from webapp import app

@app.route('/api/review', methods=["POST"])
def review():
    return "Thanks for leaving a review"