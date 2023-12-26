import asyncio
from lib.tgbot import bot


def main():

    asyncio.run(bot.infinity_polling())

if __name__ == '__main__':

    main()