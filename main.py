import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton
import settings
from random import randint, choice
import ephem
from dateutil.parser import parse
from handlers import greet_user,guess_number, talk_to_me, send_cat_picture, user_coordinates


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
    dp.add_handler(MessageHandler(Filters.regex('^(Прислать котика)$'), send_cat_picture))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Бот стартовал")

    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()