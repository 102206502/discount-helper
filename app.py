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

app = Flask(__name__)

line_bot_api = LineBotApi('EgAE1+QO5FI8HJyWGLRF1YnvR8QwxWllSTotRSNv5oKUupyCRaXYw29/X1T05lOAQGLxtQxmVXsnHV0qjylujvDxhzX6X8as5XJRW/uiOJMHmsN00C6q21rfTkQN0U2zxvLqyaH2UVZ1BvRIeNDrzgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('bfe31fc18c99304ae7d16c6da16c99df')

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
	line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text=event.message.text))
if __name__ == "__main__":
	app.run()
