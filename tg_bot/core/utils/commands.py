from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command = 'categories',
            description = 'Открыть меню категорий'
        ),
        BotCommand(
            command='dns',
            description='Парсер DNS'
        ),

    ]
    await bot.set_my_commands(commands,BotCommandScopeDefault())