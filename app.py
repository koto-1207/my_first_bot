import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, send_messages
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(override=True)

line_bot_api = LineBotApi(os.environ["ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["CHANNEL_SECRET"])

app = Flask(__name__)


@app.route("/")
def index():
    return "You call index()"


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    recieved_message = event.message.text
    current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
    send_message = f"{recieved_message}\n今日はどうしたの\n\n受信時刻: {current_time}"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=send_message))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
