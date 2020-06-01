# -*- coding: utf-8 -*-
import telebot
import random
from telebot import types

TOKEN = '1283121145:AAH4zBmWYVSyp1N8OYgkkndGjabD6UoVqK0'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🎲Сыграем в игру?")
    item2 = types.KeyboardButton("Узнать погоду")

    markup.add(item1, item2)

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>,  робот созданный "
                                      "что-бы передать масло".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == '☀️Узнать погоду🎲':
            bot.send_message(message.chat.id, str(random.randint(0,100)))


        elif message.text == '🎲Сыграем в игру?':


                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("Камень", callback_data='3')
                item2 = types.InlineKeyboardButton("Ножницы ", callback_data='1')
                item3 = types.InlineKeyboardButton("Бумага", callback_data='2')
                item4 = types.InlineKeyboardButton("Ящерица", callback_data='4')
                item5 = types.InlineKeyboardButton("Спок", callback_data='5')
                item6 = types.InlineKeyboardButton("ПРАВИЛА", callback_data='6')

                markup.add(item1, item2, item3, item4, item5, item6)

                bot.send_message(message.chat.id, 'Сделай свой выбор!', reply_markup=markup)

        else:
            bot.send_message(message.chat.id, message.text + '😊')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            compliance = {'1': 'scissors', '2': 'paper', '3': 'rock', '4': 'lizard', '5': 'Spock', '6': 'stop'}
            win = {'scissors': ('paper', 'lizard'), 'paper': ('rock', 'Spock'), 'rock': ('scissors', 'lizard'),
                   'lizard': ('Spock', 'paper'), 'Spock': ('scissors', 'rock')}

            option = ['scissors', 'paper', 'rock', 'lizard', 'Spock']
            rus = {'scissors' : '✂', 'paper' : '📄', 'rock' : '🗿', 'lizard' : '🦎', 'Spock' : '🖖', 'stop' : '❌'}

            random.shuffle(option)  # shuiffle
            computer_choise = random.choice(option)  # choise

            user_input = compliance.get(call.data)

            if user_input != 'stop' and user_input != "6":
                rus_user_input = rus.get(user_input)
                rus_bot_input = rus.get(computer_choise)
                bot.send_message(call.message.chat.id, 'Твой выбор ')  # print('You chose is', user_input + "!")
                bot.send_message(call.message.chat.id, rus_user_input)
                bot.send_message(call.message.chat.id, 'Мой выбор ')
                bot.send_message(call.message.chat.id, rus_bot_input)
                win_combination = win.get(user_input)  # dict.get(key[, default])
                if computer_choise == user_input:
                # print('There is a draw', computer_choise)
                    bot.send_message(call.message.chat.id, 'Это НИЧЬЯ 👋')
                    # show alert
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="ЭТО НИЧЬЯ!!!!!")
                elif computer_choise in win_combination:
                    #print('Well done. Computer chose ' + computer_choise, 'and failed! :)')
                # show alert
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="ЭТО ПОБЕДА!!11")
                    bot.send_message(call.message.chat.id, 'Ты ПОБЕДИЛ! 💥')
                # show alert
                else:
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text="ЭТО ПОРАЖЕНИЕ!!11")
                    bot.send_message(call.message.chat.id, 'Ты проиграл! ☃️')
                #print('I liked it, come again, bye!')
                # remove inline buttons

            else:

                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text="Да кому нужны эти правила!")
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Правила простые: Ножницы режут бумагу. Бумага "
                                           "заворачивает камень. Камень давит ящерицу, а ящерица травит Спока, в то "
                                           "время как Спок ломает ножницы, которые, в свою очередь, отрезают голову "
                                           "ящерице, которая ест бумагу, на которой улики против Спока. Спок испаряет "
                                           "камень, а камень, разумеется, затупляет ножницы. Всё просто. Дерзай.)) ", reply_markup=None)

    except Exception as e:
        print(repr(e))







# RUN
bot.polling(none_stop=True)
