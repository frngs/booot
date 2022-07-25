import telebot
import currency_converter
from telebot import types
from currency_converter import CurrencyConverter, RateNotFoundError


bot = telebot.TeleBot('5532817406:AAHh3mu2Y0He3T4YhOpphX8Ljri6frIrPjg')
currency= CurrencyConverter()
dict={}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Посмотреть код своей валюты', url='https://www.iban.ru/currency-codes'))

    if message.from_user.username:
        hello = f'Приветствую {message.from_user.username}, тебя встречает ConvertBot,' \
                f'напиши буквенный код своей валюты для того чтобы с конвертировать ее!'
    else:
        hello = f'Приветствую {user_id}, тебя встречает ВалютаБот!'

    bot.send_message(user_id, hello, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def to_currency(message):
    user_id = message.from_user.id

    if message.text.upper() in currency.currencies:
        dict['from'] = message.text.upper()
        bot.send_message(user_id, 'В какую валюту хотите произвести конвертацию?')
        bot.register_next_step_handler(message, how_much)
    else:
        bot.send_message(user_id, 'Извиняюсь, я не могу найти такую валюту у себя в голове')


def how_much(message):
    user_id = message.from_user.id
    if message.text.upper() in currency.currencies:
        dict['to'] = message.text.upper()
        bot.send_message(user_id, 'Какую сумму? ')
        bot.register_next_step_handler(message, convert)
    else:
        bot.send_message(user_id, 'Извиняюсь, я не могу найти такую валюту у себя в голове')


def convert(message):
    user_id = message.from_user.id

    try:
        if message.text.isdigit():
            dict['summa'] = int(message.text)
            bot.send_message(user_id, f'Я с конвертировал и получилось: '
                                      f'{int(currency.convert(dict["summa"], dict["from"], dict["to"]))}')
        else:
            bot.send_message(user_id, 'Попробуйте снова')
    except RateNotFoundError:
        bot.send_message(user_id, 'Упс, произошла какая-то ошибка(')


bot.polling()
