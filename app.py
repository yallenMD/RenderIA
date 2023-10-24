from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


#======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import tempfile, os
import datetime
import time
import openai
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
# Twelve API Key
api_key = os.getenv('TWELVEDATA_API_KEY')
# Open AI API Key
openai.api_key = os.getenv('OPENAI_API_KEY')
#News API Key
news_key = os.getenv('NEWS_API_KEY')


# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'
    

def called_chat(message):
    # Convert the message to lowercase and strip any leading or trailing whitespace
    message = message.lower().strip()
    
    # Check if the message starts with "hey chat"
    if message.startswith("hey chat"):
        return True
    else:
        return False

def topic_classification(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "system", "content": 'You are a professional text decoder who can accurately determine the main request of an input. For each input, you will respond with one of the corresponding options: Quote, Price, News, Currency. Make sure to return ONLY the option, meaning only one word. Also, if there is a certain stock specified in the request such as Microsoft, also return the ticker symbol of the stock. Otherwise, return N/A. On the otherhand if two currencies are given for exchange rates, you will first return the amount of money in the original currency that is being exchanged, then return the symbol of the currency we are changin from and then the symbol of the currency we are changing to. So in summary you will return something following either this format: "Option Ticker" or this format: "Option Amount Currency1 Currency2'},
                    {"role": "user", "content": text}
                 ])
    # 重組回應
    answer = response['choices'][0]['message']['content']
    answer = answer.split(" ")
    return answer


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if called_chat(msg):
        message = TextSendMessage(text=GPT_message(msg))
        line_bot_api.reply_message(event.reply_token, message)

    elif  topic_classification(msg)[0] == 'Price' and topic_classification(msg)[1] != 'N/A':
        ticker = topic_classification(msg)[1]
        message = TextSendMessage(text=price(ticker, api_key))
        line_bot_api.reply_message(event.reply_token, message)

    elif topic_classification(msg)[0] == 'Currency':
        if topic_classification(msg)[1] != 'N/A':
            amount = topic_classification(msg)[1]
            currency1 = topic_classification(msg)[2]
            currency2 = topic_classification(msg)[3]
            message = TextSendMessage(text=currency_conversion(currency1,currency2,amount,api_key))

    elif topic_classification(msg)[0] == 'News':
        if topic_classification(msg)[1] == 'N/A':
            message = TextSendMessage(text=news('Stocks',news_key))
            line_bot_api.reply_message(event.reply_token, message)
        else:
            topic = topic_classification(msg)[1]
            message = news_carousel(topic,news_key)
            line_bot_api.reply_message(event.reply_token, message)


    elif '旋轉木馬' in msg:
        message = Carousel_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '圖片畫廊' in msg:
        message = test()
        line_bot_api.reply_message(event.reply_token, message)
    elif '功能列表' in msg:
        message = function_list()
        line_bot_api.reply_message(event.reply_token, message)
    else:
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token, message)

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'Hey, {name}! Welcome!')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
