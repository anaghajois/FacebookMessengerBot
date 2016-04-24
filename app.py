from flask import Flask, request
import os
import requests

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'top-secret!'
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == os.environ['VERIFY_TOKEN']:
            return request.args.get("hub.challenge")
        else:
            return "Error, wrong validation token"
    else:
        try:
            output = request.json
            event = output['entry'][0]['messaging']
            for x in event:
                if x.get('message') and x['message'].get('text'):
                    message = x['message']['text']
                    recipient_id = x['sender']['id']
                    print message
                    send_message(recipient_id, message)
                else:
                    pass
        except Exception, e:
            print e
        return "failure"


def send_message(recipient_id, message):
    payload = {'recipient': {'id': recipient_id},
               'message': {'text': message}
               }
    url = 'https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(os.environ['PAGE_ACCESS_TOKEN'])
    result = requests.post(url, json=payload)
    print result.json()
    return result.json()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host = '0.0.0.0',port=port)