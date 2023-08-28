import requests, json
from parser import main_async
from headers import headers


def catalog(cookies):
    '''собираем ссылки на весь каталог'''
    cat_id = {}
    response = requests.get('https://www.mvideo.ru/bff/settings/catalog', cookies=cookies, headers=headers).json()
    cat = response.get('body').get('categories')
    for item in cat:
        name = item['name']
        url = item.get('categories')
        cat_id[name] = url
    cat_id2 = {}
    for k, v in cat_id.items():
        cat_id2[k] = [{i['name']: f"https://www.mvideo.ru{i['url']}" for i in j['categories']} for j in v]

    with open('links.json', 'w') as file:
        json.dump(cat_id2, file, indent=4, ensure_ascii=False)
    print('Файл "links.json" успешно создан')

catalog(main_async.Cookies.cookies())