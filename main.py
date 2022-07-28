import requests
from datetime import datetime
import telebot
from telebot import types
from auth_data import token


def get_data():
    req = requests.get("https://yobit.net/api/3/ticker/btc_usd")
    response = req.json()

    sell_price = response["btc_usd"]["sell"]
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nSell BTC price:{sell_price}")

def telegram_bot(token):
    bot = telebot.TeleBot(token)


    @bot.message_handler(commands=["start"])
    def str_hi(hi):

        keyboard = types.ReplyKeyboardMarkup()
        button_1 = types.KeyboardButton(text="price BTC")
        keyboard.add(button_1)
        button_3 = types.KeyboardButton(text="price ETH")
        keyboard.add(button_3)
        button_2 = "help"
        keyboard.add(button_2)
        bot.send_message(hi.chat.id, "Hello friend! Write the 'price' to find out the cost of BTC or ETH", reply_markup=keyboard)

    @bot.message_handler(content_types=["text"])
    def send_text(message):
        if message.text.lower() == "price btc":
            try:
                req = requests.get("https://yobit.net/api/3/ticker/btc_usd")
                response = req.json()
                sell_price = response["btc_usd"]["sell"]
                bot.send_message(
                    message.chat.id,
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nSell BTC price:{sell_price}"
                )
            except Exception as ex:
                print(ex)
                bot.send_message(
                    message.chat.id,
                    "Damn... Somthing was wrong..."
                )
        else:
            bot.send_message(message.chat.id, "What???")

    bot.polling()

if __name__ == '__main__':
    get_data()
    telegram_bot(token)
