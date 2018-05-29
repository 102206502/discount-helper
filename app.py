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
import pttcrawler
import urllib.parse

app = Flask(__name__)

line_bot_api = LineBotApi('fSMwE33M/k8ghVDECft3OHmOMe/6hWYEfZLr8zO/NipaNlzhWG4Mp+sM9EhZZUBr5Qz9B1pDg/HA5QzeQRKPr9D4yODISelp28dzFvHdinGK7k8piNfUWYgbnUyCX5wLgchxkJ5f8mNp4G9SneyEAQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6fc5f6ff56b76e30f01331253b4cacd5')
crawler = pttcrawler.PttBoardCrawleer()

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
    discount_info = discount_df[['date','title','link']]
    for i in range(len(discount_info)):
        info_meta = discount_info.iloc[i,:]
        link_str = urllib.parse.urljoin(crawler.domain, info_meta['link'])
        message = info_meta['date']+'\n'+info_meta['title']+'\n'+link_str
        line_bot_api.reply_message(
            event.reply_token, 
            TextSendMessage(text=str(message))
            # TextSendMessage(text=event.message.text)
        )

if __name__ == "__main__":
    app.run()
    crawler = pttcrawler.PttBoardCrawleer()
