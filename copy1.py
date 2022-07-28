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
