import json,csv

def convector():
    result = []

    with open('result.json')as file:
        data = json.load(file)
        for k,v in data.items():
            item = v['body']['products']
            result += [[i['productId'], i['name'] ,i['item_basePrice'],i['item_salePrice']
                       ,i['item_bonus'],i['item_link']] for i in item]

    columns = ['id', 'Наименование', 'Базовая цена', 'Цена со скидкой', 'Бонус', 'Ссылка']
    with open('result.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(columns)
        for row in result:
            writer.writerow(row)

    return 'result.csv'