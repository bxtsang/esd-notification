from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy as alc
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root@localhost:3306/notifications"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = alc(app)

class Promotions(db.Model):
    __tablename__ = 'promotions'

    code = db.Column(db.String(12), primary_key = True)
    discount = db.Column(db.Integer, nullable = False)
    name = db.Column(db.String(50), nullable = False)
    redemptions = db.Column(db.Integer, nullable = True)
    start_date = db.Column(db.String(10), nullable = False)
    end_date = db.Column(db.String(10), nullable = False)
    message = db.Column(db.String(300), nullable = False)


    def __init__(self, code, discount, name, redemptions, start, end, message, **kwargs):
        self.code = code
        self.discount = discount
        self.name = name
        self.redemptions = redemptions
        self.start_date = start
        self.end_date = end
        self.message = message

    def json(self):
        return {"code": self.code, "discount": self.discount, "name": self.name, "redemptions": self.redemptions, "start": self.start_date, "end": self.end_date, "message": self.message}

class Applicability(db.Model):
    __tablename__ = 'applicability'

    code = db.Column(db.String(10), primary_key = True)
    customer_tier = db.Column(db.Integer, primary_key = True)

    def __init__(self, code, tier, **kwargs):
        self.code = code
        self.customer_tier = tier

    def json(self):
        return {"code": self.code, "customer_type": self.customer_type}

@app.route("/retrieve")
def retrieve_all():
    return jsonify({"promotions": [promotion.json() for promotion in Promotions.query.all()]})

@app.route("/create/<string:code>", methods = ['POST'])
def create_promotion(code):

    if Promotions.query.filter_by(code = code).first():
        return jsonify({"error": "A promotion with promo code '{}' already exists.".format(code)}), 400

    data = request.get_json()
    promo = Promotions(code, **data)
    try:
        db.session.add(promo)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred while creating the promotion"}), 500

    tiers = data["tiers"]
    for tier in tiers:
        app = Applicability(code, tier)

        try:
            db.session.add(app)
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify({"message": "An error occurred while creating the applicability."}), 500  

    return jsonify(promo.json()), 201


if __name__ == "__main__":
    app.run(port=5000, debug=True)