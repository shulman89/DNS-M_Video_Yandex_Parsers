from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha
import json, math, aiohttp
from parser.headers import headers
from aiohttp_retry import RetryClient, ExponentialRetry
import undetected_chromedriver as uc
from parser.proxy import proxy
from aiofiles import os
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import asyncio


class Cookies:
    solver = TwoCaptcha('18b70a6f54524d11639c92ce4ef89cac')
    dict_resut = {}
    img_name = 'img.png'
    text = 'Вы человек?'
    image = 'body > div > img'
    input = 'input.input:nth-child(2)'
    btn = '.btn-hover'

    chrome_options = uc.ChromeOptions()
    # options.add_argument("--disable-popup-blocking")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--incognito")
    # options.add_argument("--ignore-certificate-errors")
    # chrome_options.add_argument("--headless")
    url = 'https://www.mvideo.ru/noutbuki-planshety-komputery-8/noutbuki-118'

    @classmethod
    def sender_solve(cls):
        path = cls.img_name
        result = cls.solver.normal(path)
        cls.dict_resut.update(result)
        print(f"Проверяем шифр:{result['code']}")
        return result['code']

    @classmethod
    def solve_captcha(cls):
        browser.find_element(By.CSS_SELECTOR, cls.image).screenshot(cls.img_name)
        browser.implicitly_wait(10)
        browser.find_element(By.CSS_SELECTOR, cls.input).send_keys(cls.sender_solve())
        browser.implicitly_wait(10)
        print('Вставляем символы в окошко')
        element = browser.find_element(By.CSS_SELECTOR, cls.btn)
        browser.implicitly_wait(10)
        print("Нажимаем на кнопку")
        element.click()
        sleep(5)
        if 'Главная' in browser.page_source:
            return True

    @classmethod
    def cook(cls):
        while True:
            try:
                browser.get(cls.url)
                sleep(5)
                for _ in range(5):
                    ActionChains(browser).scroll_by_amount(0, 2000).perform()
                    sleep(1)
                cookies = {i['name']: i['value'] for i in browser.get_cookies()}
                print('Печеньки успешно собраны')
                return cookies
            except Exception:
                print("Ошибка сбора печенек.Пробуем еще раз")
                cls.cook()


    @classmethod
    def cookies(cls):
        try:
            global browser
            with uc.Chrome(main_version=109, crome_options=cls.chrome_options,
                           seleniumwire_options=proxy, headless='--headless', no_sandbox="--no-sandbox") as browser:
                browser.get(cls.url)
                if cls.text in browser.page_source:
                    print('Капча.Пробуем разгадать')
                    succes = cls.solve_captcha()
                    if succes:
                        print('Капча разгадана')
                        cls.solver.report(cls.dict_resut['captchaId'], True)
                        sleep(5)
                        for _ in range(5):
                            ActionChains(browser).scroll_by_amount(0, 2000).perform()
                            sleep(1)
                        cookies = {i['name']: i['value'] for i in browser.get_cookies()}
                        print('Печеньки успешно собраны')
                        return cookies
                    else:
                        print("Капча решена не верно, повторяем попытку")
                        browser.quit()
                        cls.cookies()
                else:
                    print('Капчи нет.Собираем печеньки')
                    return cls.cook()
        except Exception as ex:
            print(ex)
            print('Ошибка подключения.Пробуем еще раз...')
            browser.quit()
            cls.cookies()

    @staticmethod
    def browser_quit():
        browser.quit()


class Parser:

    def __init__(self, session, cookies, categoryId):
        self.session = session
        self.cookies = cookies
        self.categoryId = categoryId

    async def get_data(self):
        params = {
            'categoryId': self.categoryId,
            'offset': '0',
            'limit': '24',
            'filterParams': 'WyJ0b2xrby12LW5hbGljaGlpIiwiLTEyIiwiZGEiXQ==',
            'doTranslit': 'true',
        }
        retry_options = ExponentialRetry(attempts=5)
        retry_client = RetryClient(raise_for_status=False, retry_options=retry_options, client_session=self.session,
                                   start_timeout=0.5)
        response = await retry_client.get('https://www.mvideo.ru/bff/products/listing', params=params,
                                          cookies=self.cookies,
                                          headers=headers)
        total_items = await response.json()
        total_items = total_items.get('body').get('total')
        if total_items is None:
            return 'No items!'
        limit = int(params['limit'])
        pages_count = math.ceil(total_items / limit)
        print(f'всего товаров: {total_items}, всего страниц: {pages_count}')
        products_ids = {}
        products_descr = {}
        products_prices = {}
        for i in range(pages_count):
            offset = (f'{i * limit}')
            params = {
                'categoryId': self.categoryId,
                'offset': offset,
                'limit': '24',
                'filterParams': 'WyJ0b2xrby12LW5hbGljaGlpIiwiLTEyIiwiZGEiXQ==',
                'doTranslit': 'true',
            }
            response = await retry_client.get('https://www.mvideo.ru/bff/products/listing', params=params,
                                              cookies=self.cookies,
                                              headers=headers)
            ids_list = await response.json()
            ids_list = ids_list.get('body').get('products')
            products_ids[i] = ids_list
            json_data = {
                'productIds': ids_list,
                'mediaTypes': [
                    'images',
                ],
                'category': True,
                'status': True,
                'brand': True,
                'propertyTypes': [
                    'KEY',
                ],
                'propertiesConfig': {
                    'propertiesPortionSize': 5,
                },
                'multioffer': False,
            }
            items = await retry_client.post('https://www.mvideo.ru/bff/product-details/list', cookies=self.cookies,
                                            headers=headers,
                                            json=json_data)
            items = await items.json()
            products_descr[i] = items
            ids_str = ','.join(ids_list)
            params = {
                'productIds': ids_str,
                'addBonusRubles': 'true',
                'isPromoApplied': 'true',
            }
            response = await retry_client.get('https://www.mvideo.ru/bff/products/prices', params=params,
                                              cookies=self.cookies,
                                              headers=headers)
            material_prices = await response.json()
            material_prices = material_prices.get('body').get('materialPrices')
            for item in material_prices:
                item_id = item.get('price').get('productId')
                item_base_price = item.get('price').get('basePrice')
                item_sale_price = item.get('price').get('salePrice')
                item_bonus = item.get('bonusRubles').get('total')
                products_prices[item_id] = {
                    'item_basePrice': item_base_price,
                    'item_salePrice': item_sale_price,
                    'item_bonus': item_bonus
                }
        with open('1_ids.json', 'w') as file:
            json.dump(products_ids, file, indent=4, ensure_ascii=False)
        print("Файл '1_ids.json' с id товаров создан")
        with open('2_items.json', 'w') as file:
            json.dump(products_descr, file, indent=4, ensure_ascii=False)
        print("Файл '2_items.json' с id товаров создан")
        with open('3_prices.json', 'w') as file:
            json.dump(products_prices, file, indent=4, ensure_ascii=False)
        print("Файл '3_prices.json' с id товаров создан")

    def get_result(self):
        with open('2_items.json') as file:
            products_data = json.load(file)

        with open('3_prices.json') as file:
            products_prices = json.load(file)

        for items in products_data.values():
            products = items.get('body').get('products')

            for item in products:
                product_id = item.get('productId')

                if product_id in products_prices:
                    prices = products_prices[product_id]

                item['item_basePrice'] = prices.get('item_basePrice')
                item['item_salePrice'] = prices.get('item_salePrice')
                item['item_bonus'] = prices.get('item_bonus')
                item['item_link'] = f'https://www.mvideo.ru/products/{item.get("nameTranslit")}-{product_id}'

        with open('result.json', 'w') as file:
            json.dump(products_data, file, indent=4, ensure_ascii=False)
        print(f"Файл 'result.json' с результатом создан")


async def cleaner():
    await os.remove('1_ids.json')
    await os.remove('tg_2_items.json')
    await os.remove('3_prices.json')
    await os.remove('result.json')
    print('Файл успешно отправлен')


async def data(cat):
    try:
        async with aiohttp.ClientSession() as session:
            cookies = Cookies.cookies()
            parser = Parser(session, cookies, cat)
            await parser.get_data()
            Cookies.browser_quit()
            parser.get_result()
            return 'result.json'
    except Exception as ex:
        print(ex)
        Cookies.browser_quit()
        await data(cat)

asyncio.run(data('65'))
