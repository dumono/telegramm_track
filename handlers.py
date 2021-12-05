import logging
from random import choice
from glob import glob
from utils import play_random_numbers, get_smile, main_keyboard


# приветствие /start
def greet_user(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    print('Вызван /start')
    update.message.reply_text("Привет, {}! Ты вызвал команду /start".format(update.message.from_user["username"]))
    update.message.reply_text(f"ты можешь со мной поболтать {context.user_data['emoji']}!", reply_markup=main_keyboard())
    logging.info("connect username: {}".format(update.message.from_user["username"]))
    print("connect username: {}".format(update.message.from_user["username"]))

def send_cat_picture(update, context):
    cat_photos_list =  glob('images/cat*.jp*g')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'), reply_markup=main_keyboard())



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

def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    username = update.effective_user.first_name
    text = update.message.text
    update.message.reply_text(f"Здравствуй, {username} {context.user_data['emoji']}! Ты написал: {text}")

def user_coordinates(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    coords = update.message.location
    update.message.reply_text(
        f"Ваши координаты {coords} {context.user_data['emoji']}!",
        reply_markup=main_keyboard()
    )