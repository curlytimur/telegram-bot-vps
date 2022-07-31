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


BUTTONS = ["BTC", "ETH", "XRP"]
USER_DB = {}

# if USER_DB.get(chat_id, None) is None:
#     USER_DB[chat_id] = {}
# USER_DB[chat_id]["name"] = message.text


def telegram_bot(token):
    bot = telebot.TeleBot(token)
# name = int(input('What is you name?'))
# last_name = int(input('What is you last name?'))
# date_of_birth = int(input('When you HB'))


    @bot.message_handler(commands=["start"])
    def str_name(message):
        msg = bot.send_message(message.chat.id, "What is you name?")
        bot.register_next_step_handler(msg, str_last_name)


    def str_last_name(message):
        msg = bot.send_message(message.chat.id, "What is you last name?")
        bot.register_next_step_handler(msg, str_HB)

    def str_HB(message):
        msg = bot.send_message(message.chat.id, "When you birthday?")


    @bot.message_handler(commands=["price"])
    def str_pr(price):

        keyboard = types.ReplyKeyboardMarkup()
        for button_text in BUTTONS:
            button = types.KeyboardButton(text=f"price {button_text}")
            keyboard.add(button)
        # button_1 = types.KeyboardButton(text="price BTC")
        # keyboard.add(button_1)
        # button_4 = types.KeyboardButton(text="price BTC")
        # keyboard.add(button_4)
        # button_3 = types.KeyboardButton(text="price ETH")
        # keyboard.add(button_3)
        # button_2 = "help"
        # keyboard.add(button_2)
        bot.send_message(price.chat.id, "Hello friend! Write the 'price' to find out the cost of BTC or ETH", reply_markup=keyboard)



    def check_message(msg):
        msg_text = msg.text
        return msg_text[:6] == "price " and len(msg_text) == 9

    @bot.message_handler(content_types=["text"], func=check_message)
    def send_text(message):
        print(f"Received message: {message.text}")
        try:
            ticker = message.text.lower()[6:]
            url = f"https://yobit.net/api/3/ticker/{ticker}_usd"
            req = requests.get(url)
            response = req.json()
            sell_price = response[f"{ticker}_usd"]["sell"]
            bot.send_message(
                message.chat.id,
                f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nSell {ticker.upper()} price:{sell_price}"
            )
        except Exception as ex:
            print(ex)
            bot.send_message(
                message.chat.id,
                "Damn... Somthing was wrong..."
            )

    bot.polling()

if __name__ == '__main__':
    # get_data()
    telegram_bot(token)
