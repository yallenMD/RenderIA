#Creating a function list

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

def function_list():
    message = TemplateSendMessage(
        alt_text='Function List',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    title='AI Consultant',
                    text='Receive top-notch AI powered stock trading consultation.',
                    actions=[
                        MessageTemplateAction(
                            label='Try it',
                            text='Should I invest in meme stocks?'
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
                            text='Can you please provide me some useful news articles about Apple Stock?'
                        )
                    ]
                )
            ]
        )
    )
    return message