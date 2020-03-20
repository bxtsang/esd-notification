from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy as alc
import json
import requests

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

@app.route("/notify/<string:code>")
def send_notification(code):
    api_token = '1072538370:AAH2EvVRZJUpoE0SfIXgD2KKrrsN8E8Flq4' # fill in your api token here 
    base_url = 'https://api.telegram.org/bot{}/'.format(api_token)
    send_url = base_url + 'sendMessage'
    # get a list of telegram handles by requesting from customer db
    to_send = ['396984878', '30663580', '495618700', '109345204'] #simulated

    promo = Promotions.query.filter_by(code = code).first()

    if promo:
        msg = promo.message + '\npromo code: {}'.format(code)
    else:
        return jsonify({"message": "No promotion with the code {} exists.".format(code)}), 500

    for chat_id in to_send:
        params =  {'chat_id':chat_id, 'text':msg, 'parse_mode':'MarkdownV2'}
        r = requests.post(url=send_url, params=params)

    if r.status_code == 200:
        return jsonify({"message": "Successfully sent notification for promotion with code {}!".format(code)}), 200

    return jsonify({"message": "An error occurred while sending the notification."}), 500

@app.route("/getDiscount/<string:code>")
def get_discount(code):
    promo = Promotions.query.filter_by(code = code).first()
    # print(promo)

    return jsonify({"discount": promo.discount}),200

@app.route("/applyPromo/<string:code>", methods = ['POST'])
def apply_promo(code):
    # need to adjust redemptions
    

    promo = Promotions.query.filter_by(code = code).first()
    # print(promo)
    data = request.get_json()
    amount = data['amount']
    user_id = data['user_id']
    tier = data['tier']

    # check applicability
    valid = Applicability.query.filter_by(code = code, tier = tier)
    if valid == None:
        return jsonify({"message": "Sorry! You are not eligible for this promotion!"}), 400

    # check redemptions left
    if promo.redemptions == 0:
        return jsonify({"message": "Sorry! This promotion has been fully redeemed."})

    
    new_amount = amount - amount * (promo.discount / 100)    

    return jsonify({"amount": new_amount}), 200

# delete promo




if __name__ == "__main__":
    app.run(port=5000, debug=True)