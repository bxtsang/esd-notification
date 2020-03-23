from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy as alc
import json
import requests

from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root@localhost:3306/petrol"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = alc(app)

class Petrol(db.Model):
    __tablename__ = 'petrol'

    name = db.Column(db.String(20), primary_key = True)
    rating = db.Column(db.Integer, nullable = False)
    storage = db.Column(db.Float, nullable = False)
    cost = db.Column(db.Float, nullable = False)

    def __init__(self, name, rating, storage):
        self.name = name
        self.rating = rating
        self.storage = storage
        self.cost = cost

    def json(self):
        return {"name": self.name, "rating": self.rating, "storage": self.storage, "cost": self.cost}


@app.route("/petrol")
def get_all():
    return jsonify([petrol.json() for petrol in Petrol.query.all()]), 200

@app.route("/topup", methods = ['PUT'])
def topup():
    data = request.get_json()
    print(data)
    failures = {'failed': []}

    for x in data:
        petrol = Petrol.query.filter_by(name = x['name']).first()
        petrol.storage += x['amount']

        try:
            db.session.commit()
        except:
            failures['failed'].append(petrol.json())
    
    return jsonify(failures)

@app.route("/pump", methods = ['PUT'])
def pump():
    data = request.get_json()
    petrol = Petrol.query.filter_by(name = data['name']).first()

    if petrol.storage < data['amount']:
        return jsonify({"message": "Sorry, there is not enough petrol available."}), 400

    petrol.storage -= data['amount']

    try:
        db.session.commit()
    except:
        return jsonify({"message": "There was a problem deducting the amount to the database"}), 500
    
    return jsonify({"petrol": petrol.json(), "price": petrol.cost * data['amount']}), 200


if __name__ == "__main__":
    app.run(port=5200, debug=True)