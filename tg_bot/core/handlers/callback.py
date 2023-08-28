from aiogram.types import CallbackQuery,FSInputFile
from tg_bot.json_to_csv import convector
from parser import main_async
from aiofiles import os
from aiogram.utils.chat_action import ChatActionSender

#--------------здесь мы отвечаем на нажатие инлайн кнопок--------------------------------------------------------------

async def cleaner(*args):
    await os.remove('1_ids.json')
    await os.remove('2_items.json')
    await os.remove('3_prices.json')
    await os.remove('result.json')
    await os.remove('img.png')
    await os.remove(*args)
    print('Файл успешно отправлен')



async def send_file(call: CallbackQuery):
    data = call.data.split('_')
    if data[-1] == 'json':
        await call.message.answer('Пожалуйста, подождите. '
                                  'Может потребоваться несколько минут.')
        await main_async.data(data[1])
        async with ChatActionSender.upload_document(chat_id=call.message.chat.id):
            document = FSInputFile('result.json')
            await call.message.answer_document(document=document)
        await cleaner()
    else:
        await call.message.answer('Пожалуйста, подождите. '
                                  'Может потребоваться несколько минут.')
        await main_async.data(data[1])
        async with ChatActionSender.upload_document(chat_id=call.message.chat.id):
            await main_async.data(data[1])
            document = FSInputFile(convector())
            await call.message.answer_document(document=document)
        await cleaner('result.csv')
    await call.answer()




