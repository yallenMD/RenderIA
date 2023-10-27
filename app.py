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
    

def topic_classification(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "system", "content": 'You are a professional text decoder who can accurately determine the main request of an input. For each input, you will respond with one of the corresponding options: Quote, Price, News, Currency, Functions, N/A,. Make sure to return ONLY the option, meaning only one word.'},
                    {"role": "user", "content": text}
                 ])
    answer = response['choices'][0]['message']['content']
    return answer

def stock_classification(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "system", "content": 'You are a professional text decoder who can accurately determine the ticker symbol of the relevant stock in subject. If there is no specified stock, return "Stocks." In summary, you will return one word, that being either "Stocks" or a ticker symbol. For example, if the input involves microsoft stock, you will return "MSFT"'},
                    {"role": "user", "content": text}
                 ])
    answer = response['choices'][0]['message']['content']
    return answer

def currency_classification(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "system", "content": 'You are a professional text decoder who can accurately determine the main request of an input. You will receive an input from a user asking to exchange a certain amount of money from one currency to another. You will determine the currency symbols of the relevant currencies. Based on the given information you will return something following this format: "CurrencySymbol1 CurrencySymbol2 Amount"'},
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
    if  topic_classification(msg) == 'Price':
        if stock_classification(msg) != 'N/A':
            ticker = stock_classification(msg)
            message = TextSendMessage(text=price(ticker, api_key))
            line_bot_api.reply_message(event.reply_token, message)
        else:
            ticker = 'NASDAQ'
            message = TextSendMessage(text=price(ticker, api_key))
            line_bot_api.reply_message(event.reply_token, message)

    elif topic_classification(msg) == 'Currency':
        amount = currency_classification(msg)[2]
        currency1 = currency_classification(msg)[0]
        currency2 = currency_classification(msg)[1]
        message = TextSendMessage(text=currency_conversion(currency1,currency2,amount,api_key))
        line_bot_api.reply_message(event.reply_token, message)
        
    elif topic_classification(msg) == 'News':
        if stock_classification(msg) == 'N/A':
            message = TextSendMessage(text=news('Stock Market',news_key))
            line_bot_api.reply_message(event.reply_token, message)
        else:
            topic = topic_classification(msg)
            message = news_carousel(topic,news_key)
            line_bot_api.reply_message(event.reply_token, message)

    elif topic_classification(msg) == 'Functions':
        message = function_list()
        line_bot_api.reply_message(event.reply_token, message)
    else:
        message = TextSendMessage(text=GPT_message(msg))
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
