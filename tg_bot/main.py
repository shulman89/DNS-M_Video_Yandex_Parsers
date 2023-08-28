from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup
from aiogram.filters import Text
from aiogram import Bot, Dispatcher, F
from aiogram.types import KeyboardButton
from aiogram.types import Message
from aiogram.filters import Command
from core.settings import settings
import asyncio
import logging
from tg_bot.core.handlers.send_media import get_tv
from core.handlers.basic import get_start,dns_category, select_format_tv, select_format_monitors,select_format_pc,select_format_phone,select_format_smart,select_format_tablet
from core.utils.commands import set_commands
from core.handlers import callback
from core.handlers.callback_dns import select_dns_cat,select_dns_subcat
from core.midlwares.example_chat_action_middleware import ExampleChatActionMiddleware

dp = Dispatcher()

async def start_bot(bot:Bot):
    await set_commands(bot)

# async def error(bot: Bot):
#     await bot.send_message('Произошла непредвиденная ошибка. Пожалуйста обратитесь к ...')


async def start():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
#-------------------------регистрируем__________________________________________________________________________________
    dp.startup.register(start_bot)
    #dp.message.register(error)
    dp.message.register(get_start, Command(commands=['categories','start']))
    dp.message.register(dns_category, Command('dns'))
    dp.message.register(select_format_tv,Text('Телевизоры'))
    dp.message.register(select_format_phone, Text('Мобильные телефоны'))
    dp.message.register(select_format_tablet, Text('Планшеты'))
    dp.message.register(select_format_smart, Text('Смарт-часы'))
    dp.message.register(select_format_pc, Text('Ноутбуки и компьютеры'))
    dp.message.register(select_format_monitors, Text('Мониторы'))
    dp.callback_query.register(callback.send_file, F.data.startswith('check'))
    dp.callback_query.register(select_dns_cat, F.data.startswith('dns'))
    dp.callback_query.register(select_dns_subcat, F.data.startswith('subcat'))
#-----------------------------------------------------------------------------------------------------------------------
    try:
        await dp.start_polling(bot)
    except Exception as ex:
        print(ex)
        # await error(bot)
        # await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
