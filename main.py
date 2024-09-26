import telebot
from telebot import types
import sqlite3
TOKEN = '7766672191:AAEko0FKCD1EN8UunekEREqc8hXH15YQMrk'
bot = telebot.TeleBot(TOKEN)
hi_message = 'hi, its korea bot'
manager_id = 0
shop_list = ['zara https://www.zara.com/kr/en/',
            'h&m https://www2.hm.com/ko_kr/index.html',
            'the skinfood https://en.theskinfood.com/',
            'holika holika https://holikaholika.co.id/'
             ]
d = {i+1: shop_list[i] for i in range(len(shop_list))}
shop_message = d.__str__()
# отправляем челу список магазинов
# кидает номер магазина либо сообщение про вход в корзину
# 1.
# 2.

def add_user(message):
    # если нет в бдшке то добавляем
    pass


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print(message)
    if message.chat.type == 'private':
        if message.text[0] == '/':
            if message.text == '/start':
                # bot.send_message(message.from_user.id, hi_message)
                # bot.send_message(message.from_user.id, shop_message)
                add_user(message)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Начать покупки")
                btn2 = types.KeyboardButton("Открыть корзину")
                markup.add(btn1, btn2)
                bot.send_message(message.from_user.id, text=hi_message, reply_markup=markup)
                bot.register_next_step_handler(message, get_shop_or_basket)
            elif message.text == '/help':
                bot.send_message(message.from_user.id, "Задай свой вопрос\nЕсли передумал задавать - напиши Отмена")
                bot.register_next_step_handler(message, get_help)
            else:
                bot.send_message(message.from_user.id, 'Неизвестная команда')
        else:
            bot.send_message(message.from_user.id, "Для помощи напиши /help")

def get_help(message):
    if message.text.lower().strip() != 'отмена':
        try:
            bot.send_message(manager_id, f'message from user @{message.from_user.username}\n' + message.text)
            bot.send_message(message.from_user.id, 'Спасибо за вопрос, с тобой свяжутся, жди ответа')
        except:
            bot.send_message(message.from_user.id, 'Произошла ошибка, напиши еще раз')
            bot.register_next_step_handler(message, get_help)
    else:
        bot.send_message(message.from_user.id, 'Диалог прерван')
        return

def get_shop_or_basket(message):
    if message.text == 'Начать покупки':
        # выбор магазина

        bot.send_message(message.from_user.id, shop_message, reply_markup=None)
        # bot.register_next_step_handler(message, shop_order)
    elif message.text == 'Открыть корзину':
        # открытие корзины
        # отправляем его корзину
        pass
    else:
        pass

def shop_order(message):
    pass


bot.polling()
