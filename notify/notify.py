from flask import Flask, request, jsonify
import json
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

channels = ["Telegram", "E-Mail"]

class Telegram:
    

    def __init__(self):

        with open ('api_token.txt', 'rt') as file:
            api_token = file.read()

        self.base_url = 'https://api.telegram.org/bot{}/'.format(api_token)
        self.send_url = self.base_url + 'sendMessage'

    def send_msg(self, chat_id, message):

        params =  {'chat_id':chat_id, 'text':message}
        r = requests.post(url=self.send_url, params=params)

        return r.status_code

@app.route("/sendNotification", methods = ['POST'])
def send_notif():
    '''take in json request with following fields:
    {
        "channels":  [channel 1, channel 2 ...],
        "promo": {all promo details},
        "message": "promotion message to be sent"
    }
    '''
    data = request.get_json()
    channels = data['channels']
    promo = data['promo']
    tiers = promo['tiers']

    to_send = [{'user_id': 1,
                'Telegram': '396984878'},
                {'name': "bob", 'user_id': 2, 'Telegram': 'soewofijawof', 'E-Mail': "bxtsang.2018@sis.smu.edu.sg"}] #get list of customers

    details = "promo code: {} \n discount: {} \n valid period: {} - {} \n number of redemptions: {}".format(promo['code'], promo['discount'], promo['start'], promo['end'], promo['redemptions'])

    message = promo['name'] + '\n' + data['message'] + '\n' + details

    fail = {}

    if "Telegram" in channels:
        tele = Telegram()
        tele_fail = []

        for customer in to_send:
            r = tele.send_msg(customer['Telegram'], message)
            print(r)
            if r != 200:
                tele_fail.append(customer)
    
        fail["Telegram"] = tele_fail

    return jsonify(fail)


if __name__ == "__main__":
    app.run(port=5100, debug=True)