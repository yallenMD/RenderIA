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
                    text='Receive top-notch AI powered stock trading consultation',
                    actions=[
                        MessageTemplateAction(
                            label='Try it',
                            text='Hey chat, what is a 401k and do I need it？'
                        )
                    ]
                ),
                CarouselColumn(
                    title='Real-time market information',
                    text='Stock Quotes, Prices, Currency Exchange rates etc. I can do it all!',
                    actions=[
                        MessageTemplateAction(
                            label='Try it',
                            text='What is the current price of Tesla stock?'
                        )
                    ]
                ),
                CarouselColumn(
                    title='Top Headlines',
                    text='Receive the the hottest news headlines about the topic of your choice',
                    actions=[
                        MessageTemplateAction(
                            label='Try it',
                            text='Can you please provide me some useful news articles about Gamestop Stock?'
                           )
                    ]
            ]
        )
    )
    return message