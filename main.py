import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
import platform


def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text("Привет, {}! Ты вызвал команду /start".format(update.message.from_user["username"]))
    update.message.reply_text("ты можешь со мной поболтать, либо узнать данные с датчика")
    update.message.reply_text("для этого используй команду /temp")
    logging.info("connect username: {}".format(update.message.from_user["username"]))
    print("connect username: {}".format(update.message.from_user["username"]))

def talk_to_me(update, context):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)

def get_temperature(update, context):
    if platform.node() != 'raspberrypi':
        logging.warning("Бот запущен не на raspberry pi")
        update.message.reply_text("Бот запущен не на rasbperrypi")
    else:
        humidity, temperature = Adafruit_DHT.read_retry(settings.DHT_TYPE, settings.DHT_PIN)
        if humidity is not None and temperature is not None:
            #print('Температура={0:0.1f}* Влажность={1:0.1f}%'.format(temperature,humidity))
            update.message.reply_text('Температура={0:0.1f}* Влажность={1:0.1f}%'.format(temperature,humidity))
        else:
            logging.error('Ошибка получения данных с датчика DHT{0} на пине GPIO{1}'.format(settings.DHT_TYPE, settings.DHT_PIN))
            update.message.reply_text("Ошибка получения данных с датчика DHT" + settings.DHT_TYPE)


def main():
    mybot = Updater(settings.API_KEY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("temp", get_temperature))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Бот стартовал")

    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()