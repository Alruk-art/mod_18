import telebot
from config18 import carrency, TOKEN
from extens18 import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Привет, я помогу узнать курс валют')
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n<Сколько (целое число)>  \
<из какой валюты> \
<в какую валюту> \ Увидеть список доступных валют:/values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in carrency.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        # values[0] = values[0].replace(',', ".")  # Замена запятой на точку для обработки <float>
        # bot.send_message(message.chat.id, {values[0]})
        if len(values) != 3:
            raise ConvertionException("Проверьте ввод данных, для справки введите команду /help.")

        values[0] = values[0].replace(',', ".")  # Замена запятой на точку для обработки <float>
        amount, quote, base = values
        total_base = round((CryptoConverter.convert(quote, base, amount))*int(amount),3)

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'не удалось обработать команду   \n(e)')
    else:
        text = f'Цена {amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()
