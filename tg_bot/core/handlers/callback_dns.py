from aiogram.types import CallbackQuery,FSInputFile
from tg_bot.core.keyboards.inline import DNS_inline_keyboard_2
import json
from aiocsv import AsyncWriter
import aiofiles
from parser_DNS import main_dns



async def select_dns_cat(call: CallbackQuery):
    data = call.data.split('_')
    await call.message.answer(f'Строим разделы для категории: "{data[1]}".')
    await call.message.answer('Выберите,пожалуйста категорию товара.', reply_markup=await DNS_inline_keyboard_2(data[2],data[3],call.message))

async def select_dns_subcat(call: CallbackQuery):
    data = call.data.split('_')
    with open('links.json') as file:
        links_dict = json.load(file)
    link = links_dict[data[2]][data[1]]
    await call.message.answer(f'{link}')
    await call.message.answer(f'Пожалуйста, подождите, парсим выбранную категорию...')
    await file_writer(main_dns.main(link))
    #document = FSInputFile('result.csv')
    await call.message.answer_document(FSInputFile('result.csv'))


async def file_writer(table):
    columns = ['Продукт', 'Цена', 'Ссылка']
    async with aiofiles.open('result.csv', 'w', encoding='utf-8', newline='') as file:
        writer = AsyncWriter(file, delimiter=';')
        await writer.writerow(columns)
        for row in table:
            await writer.writerow(row)













