import telebot
import traceback
from config import TOKEN, keys
from utils import APIException, Convertor

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы получить цену валюты введите комманду в следующем формате:\n\n\
<имя валюты, в которую надо перевести> <имя переводимой валюты> <количество переводимой валюты>.\n\n\
Например: рубль доллар 1\n\n\
Используйте команду /values, чтобу узнать список доступных валют'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values',])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys:
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text',])
def get_price(message: telebot.types.Message):
    vars = message.text.split(' ')
    try:
        if len(vars) != 3:
            raise APIException('нашите 3 параметра формата: валюта валюта сумма')
        quote, base, amount = vars
        result = Convertor.get_price(quote, base, amount)
    except APIException as error:
        bot.reply_to(message, error)
    except Exception as error:
        traceback.print_tb(error.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{error}")
    else:
        bot.send_message(message.chat.id, result)


bot.polling(none_stop=True)