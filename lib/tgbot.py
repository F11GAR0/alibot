import telebot

from telebot.async_telebot import AsyncTeleBot
from lib.easyali import EasyAli
from lib.db import DataBase

from config import TG_BOT_TOKEN, DOCKER, DATABASE_PATH, DATABASE_URI, DATABASE_PATH_NO_DOCKER


bot = AsyncTeleBot(TG_BOT_TOKEN, parse_mode="HTML")
ali = EasyAli(docker_is_used=DOCKER)
db = DataBase(DATABASE_PATH if DOCKER else DATABASE_PATH_NO_DOCKER)

def register_need(func):

    def wrap(*args, **kwargs):
        message = kwargs.get("message", None)
        if not message is None:
            if db.user_exists(message.from_user.id):
                return func(*args, **kwargs)
            else:
                bot.reply_to(message, "You need to register by enter /start")
        return func(*args, **kwargs)
    
    return wrap

def auto_register(func):

    def wrap(*args, **kwargs):
        message = kwargs.get("message", None)
        if not message is None:
            if not db.user_exists(message.from_user.id):
                db.register_user(message.from_user.id)
            return func(*args, **kwargs)
        return func(*args, **kwargs)
    
    return wrap

@bot.message_handler(commands=['start', 'help'])
@auto_register
async def send_start_message(message: telebot.types.Message):

    await bot.reply_to(message, "Usage: send file in .json format which is represents computer build.")

@bot.message_handler(content_types=['document'])
@register_need
async def upload_json(message: telebot.types.Message):

    if message.document:

        try:

            file_id_info = await bot.get_file(message.document.file_id)
            downloaded_file_data = await bot.download_file(file_id_info.file_path)
            str_data = downloaded_file_data.decode("utf-8")
            if db.build_exists(str_data):
                await bot.reply_to(message, "Build exists. Wait til check.")
            else:
                db.upload_build(message.from_user.id, str_data)
                await bot.reply_to(message, "Build uploaded. Wait til check.")

            price, errors = ali.calculate_from_json(str_data)
            
            await bot.reply_to(message, f"This computer build cost is: {price} RUB. Errors: {errors[:86]}")

        except Exception as e:

            await bot.reply_to(message, e.__str__())
    
    else:

        await bot.reply_to(message, "Does not see document! Check /help")