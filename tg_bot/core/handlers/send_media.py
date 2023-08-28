from aiogram.types import Message, FSInputFile
from aiogram import Bot
from parser import main_async

text='Пожалуйста, подождите. Для обхода капчи, сбора cookie и парсинга данных может потребоваться пара минут.'

async def get_tv(message: Message, bot: Bot):
    match message.text:
        case 'Телевизоры':
            await bot.send_message(message.chat.id, text=text)
            document = FSInputFile(await main_async.data('65'))
            await bot.send_document(message.chat.id, document=document)
        case 'Мобильные телефоны':
            await bot.send_message(message.chat.id, text=text)
            document = FSInputFile(await main_async.data('205'))
            await bot.send_document(message.chat.id, document=document)
        case 'Планшеты':
            await bot.send_message(message.chat.id, text=text)
            document = FSInputFile(await main_async.data('195'))
            await bot.send_document(message.chat.id, document=document)
        case 'Смарт-часы':
            await bot.send_message(message.chat.id, text=text)
            document = FSInputFile(await main_async.data('400'))
            await bot.send_document(message.chat.id, document=document)
        case 'Ноутбуки и компьютеры':
            await bot.send_message(message.chat.id, text=text)
            document = FSInputFile(await main_async.data('118'))
            await bot.send_document(message.chat.id, document=document)
        case 'Мониторы':
            await bot.send_message(message.chat.id, text=text)
            document = FSInputFile(await main_async.data('101'))
            await bot.send_document(message.chat.id, document=document)



