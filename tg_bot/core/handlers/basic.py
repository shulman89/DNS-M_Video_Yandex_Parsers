from aiogram.types import Message
from tg_bot.core.keyboards.reply import get_reply_keyboard
from tg_bot.core.keyboards.inline import get_inline_keyboard,DNS_inline_keyboard


#---------------задаем показ клавиатуры в ответ на команды --------------------------------------------------------

async def select_format_tv(message:Message):
    await message.answer('Выберите, пожалуйста, формат таблицы', reply_markup=get_inline_keyboard('65'))

async def select_format_phone(message:Message):
    await message.answer('Выберите, пожалуйста, формат таблицы', reply_markup=get_inline_keyboard('205'))

async def select_format_tablet(message:Message):
    await message.answer('Выберите, пожалуйста, формат таблицы', reply_markup=get_inline_keyboard('195'))

async def select_format_smart(message:Message):
    await message.answer('Выберите, пожалуйста, формат таблицы', reply_markup=get_inline_keyboard('400'))

async def select_format_pc(message:Message):
    await message.answer('Выберите, пожалуйста, формат таблицы', reply_markup=get_inline_keyboard('118'))

async def select_format_monitors(message:Message):
    await message.answer('Выберите, пожалуйста, формат таблицы', reply_markup=get_inline_keyboard('101'))


async def get_start(message:Message):
    await message.answer(f'{message.from_user.full_name},'
                         f'Выберите,пожалуйста категорию товара.',
                         reply_markup=get_reply_keyboard())


#_______________________________отклик на команду 'dns'------показ клавиатуры-------------------------------------------
async def dns_category(message:Message):

    await message.answer('Выберите,пожалуйста категорию товара.', reply_markup=await DNS_inline_keyboard('dns',message))




