from flask import Flask, request, abort

from linebot import (
	LineBotApi, WebhookHandler
)
from linebot.exceptions import (
	InvalidSignatureError
)
from linebot.models import (
	MessageEvent, TextMessage, TextSendMessage,
)
import pandas as pd

app = Flask(__name__)

line_bot_api = LineBotApi('fSMwE33M/k8ghVDECft3OHmOMe/6hWYEfZLr8zO/NipaNlzhWG4Mp+sM9EhZZUBr5Qz9B1pDg/HA5QzeQRKPr9D4yODISelp28dzFvHdinGK7k8piNfUWYgbnUyCX5wLgchxkJ5f8mNp4G9SneyEAQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6fc5f6ff56b76e30f01331253b4cacd5')

@app.route("/callback", methods=['POST'])
def callback():
	signature = request.headers['X-Line-Signature']
	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)
	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		abort(400)
	return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    discount_df = pd.read_csv('discount info.csv')
	line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))
if __name__ == "__main__":
	app.run()
