from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy as alc
import json
import requests
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root@localhost:3306/promotions"
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

    code = db.Column(db.String(12), primary_key = True)
    tier = db.Column(db.Integer, primary_key = True)

    def __init__(self, code, tier, **kwargs):
        self.code = code
        self.tier = tier

    def json(self):
        return {"code": self.code, "tier": self.tier}



class Redeem(db.Model):
    __tablename__ = 'redeem'

    user_id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.String(12), primary_key = True)

    def __init__(self, user_id, code):
        self.code = code
        self.user_id = user_id

    # represent in dict to prep for jsonify
    def json(self):
        return {"user_id": self.user_id, "code": self.code}

@app.route("/retrieve")
def retrieve_all():
    promotions = [promotion.json() for promotion in Promotions.query.all()]
    for promotion in promotions:
        promotion["tiers"] = [app.tier for app in Applicability.query.filter_by(code = promotion['code']).all()]
    
    return jsonify(promotions)

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

@app.route("/getDiscount/<string:code>")
def get_discount(code):
    promo = Promotions.query.filter_by(code = code).first()
    # print(promo)

    return jsonify({"discount": promo.discount}),201

@app.route("/applyPromo/<string:code>", methods = ['POST'])
def apply_promo(code):

    promo = Promotions.query.filter_by(code = code).first()
    data = request.get_json()
    amount = data['amount']
    user_id = data['user_id']
    tier = data['tier']

    # check correct code
    if promo == None:
        return jsonify({"message": "No such code exists, please try again."})

    # check expiry
    now = datetime.now().date()

    # start = datetime.strptime(promo.start_date, '%Y-%m-%d')
    # end = datetime.strptime(promo.end_date, '%Y-%m-%d')

    start = promo.start_date
    end = promo.end_date

    if now > end:
        return jsonify({"message": "The promotion has expired!"}), 400
    
    if now < start:
        return jsonify({"message": "The promotion has not started!"})

    # check applicability
    valid = Applicability.query.filter_by(code = code, customer_tier = tier).first()

    if valid == None:
        return jsonify({"message": "Sorry! You are not eligible for this promotion!"}), 400

    # check redemptions left
    if promo.redemptions == 0:
        return jsonify({"message": "Sorry! This promotion has been fully redeemed."})

    # check if redeemed before
    if Redeem.query.filter_by(user_id = user_id, code = code).first():
        return jsonify({"message": "You have already redeemed this promotion! Thank you!"}), 400

    # add to redeem table
    redemption = Redeem(user_id, code)

    try:
        db.session.add(redemption)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred while redeeming."}), 500  
    
    new_amount = amount - amount * (promo.discount / 100)    

    return jsonify({"amount": new_amount, "message": "Promotion successfully redeemed!"}), 201

# force end a promo
@app.route("/end/<string:code>")
def end_promo(code):
    end_date = datetime.now().date()

    promo = Promotions.query.filter_by(code = code).first()

    if promo == None:
        return jsonify({"message": "Wrong code"}), 400
    
    promo.end_date = end_date

    try:
        db.session.commit()
    except:
        return jsonify({"message": "An error occured while updating the end_date"}), 500
    
    return jsonify(promo.json())



if __name__ == "__main__":
    app.run(port=5000, debug=True)