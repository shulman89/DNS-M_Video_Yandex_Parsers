from aiogram.utils.keyboard import InlineKeyboardBuilder
from parser_DNS import main_dns
from aiogram.types import Message
import json

#------------------здесь строим саму инлайн клавиатуру------------------------------------------------------------------

def get_inline_keyboard(index):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='json', callback_data=f'check_{index}_json')
    keyboard_builder.button(text='csv', callback_data=f'check_{index}_csv')
    keyboard_builder.adjust(1,1)
    return keyboard_builder.as_markup()

#-----------------Инлайн клавиатура номер 1-------для ДНС---------!!!!!--------------------------------------
async def DNS_inline_keyboard(index, message: Message):
    keyboard_builder = InlineKeyboardBuilder()
    await message.answer('Пожалуйста, подождите, идет построение категорий...')
    global categories
    try:
        categories, subcategories,enum_subcategories = main_dns.Parser.cat_links()
    except Exception as e:
        print(e)
        categories, subcategories,enum_subcategories = main_dns.Parser.cat_links()
    with open('links.json','w') as file:
        json.dump(enum_subcategories,file,indent=4, ensure_ascii=False)
    global TXT
    TXT= []
    for i in range(len(categories)):
        txt = '\n'.join([f'{count}) {value}.' for count, value in enumerate(subcategories[categories[i]].keys(), 1)])
        TXT.append(txt)
        nums = len(txt.split('\n'))
        keyboard_builder.button(text=f'{categories[i]}', callback_data=f'{index}_{categories[i]}_{nums}_{i}')#_{nums}')
        keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


#--------------------Инлайн клавиатура номер 2-------для ДНС---------!!!!!----------------------------------------------
async def DNS_inline_keyboard_2(index,n,message:Message):
    keyboard_builder = InlineKeyboardBuilder()
    await message.answer(TXT[int(n)])
    cut_name = categories[int(n)]
    subcat_name = list(map(lambda x: ' '.join(x.split()[1:]),TXT[int(n)].split('.')))
    del subcat_name[-1]
    print(subcat_name)
    print(len(subcat_name))
    for i in range(1,int(index)+1):
        sub = subcat_name[i-1]
        sub = ''.join(list(filter(lambda x : x!=',' ,list(sub))))
        print(sub)
        keyboard_builder.button(text=f'{i}', callback_data=f'subcats_{i-1}_{cut_name}')#_{cut_name}')#_{subcat_name}')
        keyboard_builder.adjust(8)
    return keyboard_builder.as_markup()


def get_TXT():
    return TXT






