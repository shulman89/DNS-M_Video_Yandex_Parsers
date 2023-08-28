from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_reply_keyboard():
    keyboard_builder=ReplyKeyboardBuilder()
    keyboard_builder.button(text="Телевизоры") #65
    keyboard_builder.button(text='Мобильные телефоны') #205
    keyboard_builder.button(text='Планшеты') #195
    keyboard_builder.button(text='Смарт-часы') #400
    keyboard_builder.button(text='Ноутбуки и компьютеры') #118
    keyboard_builder.button(text='Мониторы') #101
    keyboard_builder.adjust(3, 3)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)




