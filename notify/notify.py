from flask import Flask, request, jsonify
import json
import requests
app = Flask(__name__)

channels = ["Telegram", "E-Mail"]

class Telegram:
    api_token = '1072538370:AAH2EvVRZJUpoE0SfIXgD2KKrrsN8E8Flq4' # fill in your api token here 
    base_url = 'https://api.telegram.org/bot{}/'.format(api_token)
    send_url = base_url + 'sendMessage'

    def __init__(self):
        super().__init__()

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
                'Telegram': '396984878'}] #get list of customers

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