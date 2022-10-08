#web app

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

line_bot_api = LineBotApi('qBvHAIDqX1fDaas1lKCjYJ1lG60CyATpEGf2FWtkhd4froVIJe1RocJnZVf4h6F3kOMTgF5K9vK4D8GDO5ndpz/GHVGdN1YqwUW0URractIVt9Ipv6Hp6SUHnDQa8/tqTw9jTyrgNaKA/rxVQzxTzQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('468cbf6c57a3b025d87d1c5c082c0074')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = 'Sorry I do not know what you mean'

    if msg in ['hi','Hi']:
        r = 'hi'
    elif msg == 'Have you had dinner?':
        r = 'Not yet.'
    elif msg == 'Who are you?':
        r = 'I am bot.'
    elif 'love' in msg:
        r = 'i love you'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()