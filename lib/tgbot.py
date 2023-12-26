import telebot

from telebot.async_telebot import AsyncTeleBot
from lib.easyali import EasyAli

from config import TG_BOT_TOKEN
from config import DOCKER


bot = AsyncTeleBot(TG_BOT_TOKEN, parse_mode="HTML")
ali = EasyAli(docker_is_used=DOCKER)

@bot.message_handler(commands=['start', 'help'])
async def send_start_message(message: telebot.types.Message):

    await bot.reply_to(message, "Usage: send file in .json format which is represents computer build.")

@bot.message_handler(content_types=['document'])
async def upload_json(message: telebot.types.Message):

    if message.document:

        try:
            await bot.reply_to(message, "Loading json...")

            file_id_info = await bot.get_file(message.document.file_id)
            downloaded_file_data = str(await bot.download_file(file_id_info.file_path))

            await bot.reply_to(message, "Uploaded. Wait til check.")

            result = ali.calculate_from_json(downloaded_file_data)
            
            await bot.reply_to(message, f"This computer build cost is: {result} ₽")

        except Exception as e:
            
            await bot.reply_to(message, e.__str__())
    
    else:

        await bot.reply_to(message, "Does not see document! Check /help")