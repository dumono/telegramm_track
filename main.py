import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
import settings
from random import randint, choice
from glob import glob
from emoji import emojize
import ephem
from dateutil.parser import parse


def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']

# приветствие /start
def greet_user(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    print('Вызван /start')
    my_keyboard = ReplyKeyboardMarkup([['/cat']])
    update.message.reply_text("Привет, {}! Ты вызвал команду /start".format(update.message.from_user["username"]))
    update.message.reply_text(f"ты можешь со мной поболтать {context.user_data['emoji']}!", reply_markup=my_keyboard)
    logging.info("connect username: {}".format(update.message.from_user["username"]))
    print("connect username: {}".format(update.message.from_user["username"]))

def play_random_numbers(user_number):
    bot_number =  randint(user_number - 10, user_number+10)
    if user_number > bot_number:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, ты выиграл!"
    elif user_number == bot_number:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, ничья!"
    else:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, я выиграл!"
    return message

# игра загадай число
def guess_number(update, context):
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите целое число"
    update.message.reply_text(message)

def send_cat_picture(update, context):
    cat_photos_list =  glob('images/cat*.jp*g')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))

#болтушка
def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    username = update.effective_user.first_name
    text = update.message.text
    update.message.reply_text(f"Здравствуй, {username} {context.user_data['emoji']}! Ты написал: {text}")

#счетчик слов в предложении
def wordcount(update, context):
    separators = '.,:;!?'
    count = 0
    if context.args:
        for word in context.args:
            #но это меделенный кусок
            for separator in separators:
                word = word.replace(separator, "")
            if word:
                count += 1
        update.message.reply_text(f"Слов в строке: {count}")
    else:
        update.message.reply_text("Вы не ввели строку")

#Вывод полнолуния
def next_full_moon(update, context):
    if len(context.args) != 1:
        update.message.reply_text("Надо ввести дату")
    else:
        try:
            param = parse(context.args[0])
            update.message.reply_text(f"Следующее полнолуние:{ephem.next_full_moon(param)}")
        except(ValueError):
            update.message.reply_text("Вы ввели строку, не являющуюся датой")

def calc(b, a = 0, math_operation="+"):
    if math_operation == "+":
        return a + b
    elif math_operation == "-":
        return a - b
    elif math_operation == "*":
        return a * b
    else:
        if b == 0:
            return "Делить на 0 нельзя"
        else:
            a / b

def is_number(number):
    try:
        number = float(number)
    except ValueError:
        return False
    return True
def is_operation(operation):
    operations = "+-*/"
    if operation in operations:
        return True
    else:
        return False

def calc_bot(update, context):
    list_numbers = ['0']
    list_operations = ['+']
    for n in range(len(context.args)):
        a = str(context.args[n]).replace(" ","")
        if is_number(a):
            list_numbers.append(float(a))
        elif is_operation(a):
            list_operations.append(a)
    print(list_numbers)
    print(list_operations)




def main():
    mybot = Updater(settings.API_KEY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("cat", send_cat_picture))
    dp.add_handler(CommandHandler("wordcount", wordcount))
    dp.add_handler(CommandHandler("next_full_moon", next_full_moon))
    dp.add_handler(CommandHandler("calc", calc_bot))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Бот стартовал")

    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()