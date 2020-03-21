from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy as alc
import json
import requests
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root@localhost:3306/redemption"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = alc(app)

class Redemption(db.Model):
    __tablename__ = 'redemptions'

    code = db.Column(db.String(12), primary_key = True)
    user_id = db.Column(db.Integer, primary_key = True)

    def __init__(self, user_id, code):
        self.code = code
        self.user_id = user_id

    # represent in dict to prep for jsonify
    def json(self):
        return {"user_id": self.user_id, "code": self.code}

@app.route("/redeem/<string:code>")
def redeem(code):
    '''pass json data as follows:
    "cus
    data = request.get_json()

