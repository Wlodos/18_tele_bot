import telebot
from config import TOKEN, keys
from extensions import APIException, MoneyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def send_help(message: telebot.types.Message):
    text = "Чтобы начать работу, введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> <количество переводимой валюты>\nУвидеть список всех доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def send_types_of_currency(message: telebot.types.Message):
    text = "Доступные валюты:"

    for k in keys:
        text += f"\n{k}"
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text"])
def convert(message: telebot.types.Message):
    try:

        values = message.text.split(" ")
        if len(values) != 3:
            raise APIException("Слишком много/мало параметров.")

        quote, base, amount = values
        price = MoneyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка ввода.\n{e}")
    else:
        text = f"Цена {amount} {quote} в {base} - {price}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
