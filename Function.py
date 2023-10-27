#Creating a function list

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

def function_list():
    message = TemplateSendMessage(
        alt_text='Here is what I can do',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    title='AI Consultant',
                    text='Receive top-notch AI powered stock trading consultation.',
                    actions=[
                        MessageTemplateAction(
                            label='Try it',
                            text='What is the S&P 500 and how does it work?????'
                        )
                    ]
                ),
                CarouselColumn(
                    title='Real-time market information',
                    text='Stock Quotes, Prices, Exchange rates etc. I can do it all!',
                    actions=[
                        MessageTemplateAction(
                            label='Try it',
                            text='What is the current price of Tesla stock?'
                        )
                    ]
                ),
                CarouselColumn(
                    title='Top Headlines',
                    text='Receive the latest news headlines relevant to any topic.',
                    actions=[
                        MessageTemplateAction(
                            label='Try it',
                            text='Can you please provide me some useful news articles about Gamestop Stock?'
                        )
                    ]
                )
            ]
        )
    )
    return message