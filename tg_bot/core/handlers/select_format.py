from aiogram.utils.keyboard import InlineKeyboardBuilder
from tg_bot.core.utils.callbackdata import MacInfo

def get_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='JSON', callback_data=MacInfo(model='air',size=13,chip='ml',year=2020))
    keyboard_builder.button(text='CSW', callback_data=MacInfo(model='pro',size=14,chip='ml',year=2021))
    keyboard_builder.adjust(1,1)
    return keyboard_builder.as_markup()