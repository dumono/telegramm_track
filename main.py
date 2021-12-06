import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
import ephem
from dateutil.parser import parse
from handlers import greet_user,guess_number, talk_to_me, send_cat_picture, user_coordinates

OPERATIONS = "+-*/"

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

def calc(a, b, math_operation):
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
            return a / b

def is_number(number):
    try:
        number = float(number)
    except ValueError:
        return False
    return True

#калькулятор в боте
def calc_bot(update, context):
    list_numbers = []
    list_operations = ['+'] #для удобства и упрощения
    # рассматриваю пока два варианта - все пишется слитно или все пишется через пробел
    if len(context.args) != 1:
        #здесь просто - если через пробел - просто загоняем в нужные списки все аргументы
        for n in range(len(context.args)):
            a = str(context.args[n]).replace(" ","")
            print(a)
            if is_number(a):
                list_numbers.append(float(a))
            elif a in OPERATIONS:
                list_operations.append(a)
            else:
                #если нет последнего аргумента (т.е. после мат.операции ересь, то просто удаляем ее из списка
                list_operations.pop(-1)
    else:
        # во втором случае бьем строку через разделители
        last_c = 0
        arg = context.args[0]
        for i in range(len(arg)):
            if arg[i] in OPERATIONS:
                num = arg[last_c:i]
                if is_number(num):
                    list_numbers.append(float(num))
                list_operations.append(arg[i])
                last_c = i + 1
        last_arg = arg[last_c:len(arg)]
        #я решил, что если не будет в конце второго операнда, то мы все равно посчитаем, но по правилам
        #ну или как вариант выкинем пользователю предупреждение
        # через ValueExeption специально не пошел, потому что можно вполне четко обойтись проверкой
        if is_number(last_arg):
            list_numbers.append(float(last_arg))
        elif list_operations[-1] == "+" or list_operations[-1] == "-":
            list_numbers.append(0)
        elif list_operations[-1] == "*" or list_operations[-1] == "/":
            list_numbers.append(1)
        else:
            update.message.reply_text("Вы тут что-то совсем не то написали...")
    b = 0
    for index, operation in enumerate(list_operations):
        b = calc(b, list_numbers[index], operation)
        if not is_number(b):
            break
    update.message.reply_text(b)





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