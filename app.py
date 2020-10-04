from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageMessage, AudioMessage, StickerMessage
)
import requests
import json
import re
import configparser

app = Flask(__name__)
#WEBサーバーの起動
if __name__ == "__main__":
    app.run()
#設定ファイルのロード
config = configparser.ConfigParser()
config.read('set.ini')
#設定ファイルセクション
SECTION = 'SECRETS'
#アクセストークン
ACCESS_TOKEN = LineBotApi(config.get(SECTION, 'ACCESS_TOKEN'))
#チャンネルシークレット
CHANNEL_SECRET = WebhookHandler(config.get(SECTION, 'CHANNEL_SECRET'))

"""
署名検証を行い、handleに定義されている関数を呼び出す。
"""
@app.route("/callback", methods=['POST'])
def callback():
    #リクエストヘッダーから署名検証のための値を取得
    signature = request.headers['X-Line-Signature']

    #リクエストボディを取得
    body = request.get_data(as_text=True)
    #app.logger.info("Request body: " + body)

    #署名を検証し、問題なければhandleに定義されている関数を呼び出す
    try:
        CHANNEL_SECRET.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

"""
個別handle関数
テキストメッセージが送られた場合、
返答メッセージを生成し、LINEに送る
"""
@CHANNEL_SECRET.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #ユーザからのメッセージを取得
    message = event.message.text
    #メッセージbody
    body = "Hello Your Message is " + message
    #生成したbodyをLINEに送る
    ACCESS_TOKEN.reply_message(event.reply_token,TextSendMessage(body))

"""
個別handle関数
音声・画像・スタンプが送られた場合、
返答メッセージを生成し、LINEに送る
"""
@CHANNEL_SECRET.add(MessageEvent, message=(StickerMessage, ImageMessage, AudioMessage))
def handle_other_messages(event):
    body = "this is other message"
    #生成したbodyをLINEに送る
    ACCESS_TOKEN.reply_message(event.reply_token,TextSendMessage(body))
