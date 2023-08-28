from aiogram import Bot

async def send_message_time(bot: Bot):
    await bot.send_message(1163260613,'Это сообщение отправлено через несколько секунд после старта бота')

async def send_message_cron(bot: Bot):
    await bot.send_message(1163260613, 'Это сообщение будет отправляться каждый день в одно и тоже время')

async def send_message_interval(bot: Bot):
    await bot.send_message(1163260613, 'Будет отправляться с определенным интервалом времени')

async def send_message_middleware(bot: Bot,chat_id: int):
    await bot.send_message(chat_id,'данное сообщение отправлено пользователю с помощью сформированной middleware задачи')
