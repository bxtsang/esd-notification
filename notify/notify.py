from flask import Flask, request, jsonify
import json
import requests
from flask_cors import CORS
import smtplib, ssl

app = Flask(__name__)
CORS(app)


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
    tiers_str = ''.join([str(tier) for tier in tiers])
    
    r = requests.get("http://127.0.0.1:5001/ESDproject/view?tier={}".format(tiers_str))
    to_send = r.json()

    details = "promo code: {} \ndiscount: {} \nvalid period: {} - {} \nnumber of redemptions: {}".format(promo['code'], promo['discount'], promo['start'], promo['end'], promo['redemptions'])

    message = promo['name'] + '\n' + data['message'] + '\n' + details

    fail = {}

    if "telegram" in channels:
        tele = Telegram()
        tele_fail = []

        for customer in to_send:
            r = tele.send_msg(customer['tele_id'], message)
            print(r)
            if r != 200:
                tele_fail.append(customer)
    
        fail["telegram"] = tele_fail


    if "email" in channels:
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "jpiswatchingyou@gmail.com"  # Enter your address
        password = "jiapengiswatchingyou123"
        email_fail = []

        context = ssl.create_default_context()
        for customer in to_send:

            if customer["email"]:
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, customer["email"], "Subject:" + message)
            else:
                email_fail.append(customer)

        fail["email"] = email_fail

    return jsonify(fail), 200


if __name__ == "__main__":
    app.run(port=5200, debug=True)