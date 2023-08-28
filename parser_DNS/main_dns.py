from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import csv
from parser.proxy import proxy
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from parser_DNS.cookies import cookies
from selenium.common.exceptions import NoSuchElementException
import multiprocessing

chrome_options = uc.ChromeOptions()


class Parser:

    @classmethod
    def cat_links(cls):
        url = 'https://www.dns-shop.ru/'
        with uc.Chrome(main_version=111, crome_options=chrome_options,
                       seleniumwire_options=proxy, headless=True) as browser:
            browser.get(url)
            browser.add_cookie(cookies)
            browser.refresh()
            sleep(1)
            # находим кнопку каталог и кликаем по ней
            button = browser.find_element(By.CLASS_NAME, 'header-bottom__catalog-spoiler')
            button.click()
            browser.implicitly_wait(5)
            # парсим названия всех категорий гланого каталог
            cat_list = browser.find_element(By.CSS_SELECTOR, '.catalog-menu-rootmenu').text.split('\n')
            sleep(2)
            # наводим курсор мыши на первую категорию главного каталога
            element = browser.find_element(By.CSS_SELECTOR,
                                           'div.catalog-menu__root-item:nth-child(1) > a:nth-child(1) > a:nth-child(2)')
            ActionChains(browser).move_to_element(element).perform()
            browser.implicitly_wait(5)
            sleep(1)
            # находим подкатегории категорий главного каталога
            submenus = browser.find_elements(By.CLASS_NAME, 'catalog-submenu__second-level-wrap')
            browser.implicitly_wait(5)
            # собираем словарь имя категории : ссылка на категорию
            links1 = [{} | x for x in [{i.find_element(By.TAG_NAME, 'span').text: i.get_attribute('href')
                                        for i in j.find_elements(By.TAG_NAME, 'a')} for j in submenus]]
            browser.implicitly_wait(5)
            # создаем словарь, где ключ - название категории товаров, значение - список ссылок на все подкатегории
            links = {}
            for dct in links1:
                links |= dct

            main_dict = {cat_list[0]: links}
            # наводим курсор на каждую категорию для выявления скрытых элементов
            for i in range(1, len(cat_list)):
                ActionChains(browser).move_by_offset(0, 36).perform()
                sleep(1)
                # собираем словарь имя категории : ссылка на категорию
                submenus = browser.find_elements(By.CLASS_NAME, 'catalog-submenu__second-level-wrap')
                browser.implicitly_wait(5)
                links2 = [{} | x for x in [{i.find_element(By.TAG_NAME, 'span').text: i.get_attribute('href')
                                            for i in j.find_elements(By.TAG_NAME, 'a')} for j in submenus]]

                # создаем словарь, где ключ - название категории товаров, значение - список ссылок на все подкатегории
                links = {}
                for dct in links2:
                    links |= dct
                main_dict.setdefault(cat_list[i], links)

            main_dict2 = {}
            for k, v in main_dict.items():
                d = {}
                for c, value in enumerate(v.values()):
                    d |= {c: value}
                main_dict2 |= {k: d}

            return cat_list, main_dict, main_dict2


class Items:

    def __init__(self, url):
        self.url = url

    @staticmethod
    def url_pagen(url):
        with uc.Chrome(main_version=111, crome_options=chrome_options,
                       seleniumwire_options=proxy, headless=True) as browser:
            if '?' not in url:
                browser.get(url)
                browser.add_cookie(cookies)
                browser.refresh()
                sleep(3)
                for i in range(5):
                    ActionChains(browser).scroll_by_amount(0, 300).perform()
                sleep(1)
                if 'Сортировка' in browser.page_source:
                    if 'pagination-widget__pages' in browser.page_source:
                        lst = browser.find_element(By.CLASS_NAME, 'pagination-widget__pages').find_elements(
                            By.TAG_NAME, 'a')
                        link = [l.get_attribute('href') for l in lst][-1]
                        pagen_last = link.split('=')[-1]
                        res = [f'{url}?p={i}' for i in range(1, int(pagen_last) + 1)]
                        return res
                    else:
                        return [url]
                else:
                    urls1 = browser.find_element(By.CLASS_NAME,
                                                 'subcategory__item-container ').find_elements(
                        By.TAG_NAME, 'a')
                    urls2 = [i.get_attribute('href') for i in urls1]
                    result = []
                    for href in urls2:
                        browser = uc.Chrome(main_version=111, crome_options=chrome_options,
                                            seleniumwire_options=proxy, headless=True)
                        browser.get(href)
                        browser.set_page_load_timeout(15)
                        browser.add_cookie(cookies)
                        browser.refresh()
                        sleep(2)
                        for _ in range(3):
                            ActionChains(browser).scroll_by_amount(0, 300).perform()
                            sleep(1)
                        if 'Сортировка:' in browser.page_source:
                            if 'pagination-widget__pages' in browser.page_source:
                                lst = browser.find_element(By.CLASS_NAME,
                                                           'pagination-widget__pages').find_elements(
                                    By.TAG_NAME, 'a')
                                link = [l.get_attribute('href') for l in lst][-1]
                                pagen_last = link.split('=')[-1]
                                res = [f'{href}?p={i}' for i in range(1, int(pagen_last) + 1)]
                                result += res
                            else:
                                result.append(href)
                        browser.quit()
                    print("функция url_pagen отработала")
                    return result




    def item_pages(self):
        with uc.Chrome(main_version=111, crome_options=chrome_options,
                       seleniumwire_options=proxy, headless=True) as browser:
            browser.get(self.url)
            browser.add_cookie(cookies)
            browser.refresh()
            sleep(3)
            for _ in range(2):
                ActionChains(browser).scroll_by_amount(0, 500).perform()
            sleep(1)
            if 'Сортировка' in browser.page_source:
                lst = browser.find_element(By.CLASS_NAME, 'pagination-widget__pages').find_elements(By.TAG_NAME, 'a')
                pagen_last = [l.get_attribute('href') for l in lst][-1].split('=')[-1]
                urls = [f'{self.url}?p={i}' for i in range(1, int(pagen_last) + 1)]
                print(urls)
                print('0й сценарий:', len(urls), 'cсылок')
                return urls
            else:
                urls1 = browser.find_element(By.CLASS_NAME, 'subcategory__item-container ').find_elements(By.TAG_NAME, 'a')
                urls2 = [i.get_attribute('href') for i in urls1]
                print(urls2)
                urls = []
                for url in urls2:
                    try:
                        res = self.url_pagen(url)
                    except:
                        res = self.url_pagen(url)
                    if res != None:
                        urls += res
                print(urls)
                return urls


    @staticmethod
    def check(browser, id):
        try:
            info = browser.find_element(By.CSS_SELECTOR, id)
            browser.implicitly_wait(3)
            return info
        except NoSuchElementException:
            pass


    @staticmethod
    def url_open(link):
        with uc.Chrome(main_version=111, crome_options=chrome_options,
                       seleniumwire_options=proxy, headless=True) as browser:
            try:
                browser.get(link)
                print(f'cсылка {link} открыта')
            except Exception as ex:
                print(f"ссылка {link} не открылась, пробуем еще раз ")
                browser.get(link)
                print(f'cсылка {link} открыта')
            browser.add_cookie(cookies)
            browser.refresh()
            browser.set_page_load_timeout(15)
            for _ in range(45):
                ActionChains(browser).scroll_by_amount(0, 100).perform()
            info_lst = [
                Items.check(browser, 'div.catalog-products:nth-child(2)'),
                Items.check(browser, 'div.catalog-products:nth-child(4)')
            ]
            names = []
            prices = []
            links = []
            for info in info_lst:
                if info:
                    names += list(filter(lambda x: len(x) > 60, info.text.split('\n')))
                    prices += list(filter(lambda x: '₽' in x and '₽/ мес.' not in x and 'Рассрочка' not in x and
                                                    'Скидка' not in x and 'скидка' not in x, info.text.split('\n')))
                    hrefs = [i.get_attribute('href') for i in info.find_elements(By.TAG_NAME, 'a')]
                    for i in hrefs:
                        if i != None and len(i.split('/')) == 7:
                            if i not in links:
                                links.append(i)
            print(f"функция url_open {link} отработала")

            return list(map(list, zip(names, prices, links)))


    def items(self):
        lst = self.item_pages()
        with multiprocessing.Pool(2) as pool:
            info = pool.map(self.url_open, lst)
        print('info собрано')
        return info[0]



class File:
    def __init__(self, lst):
        self.lst = lst

    def file(self):
        columns = ['Продукт', 'Цена', 'Ссылка']
        with open('result.csv', 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(columns)
            for row in self.lst:
                writer.writerow(row)


def main(link):
    items = Items(link)
    file = File(items.items())
    file.file()


#main('https://www.dns-shop.ru/catalog/17aa74ec16404e77/varochnye-paneli/')

