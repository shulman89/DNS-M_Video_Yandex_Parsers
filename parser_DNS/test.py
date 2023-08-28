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
url = 'https://www.dns-shop.ru/catalog/17a8d0b816404e77/varochnye-paneli-elektricheskie/'
url = 'https://www.dns-shop.ru/catalog/17a8d0b816404e77/varochnye-paneli-elektricheskie/?f%5Bogi%5D=qgkot&virtual_category_uid=ee6c49112b2ce5e5'
url = 'https://www.dns-shop.ru/catalog/17a9fce216404e77/varochnye-paneli-gazovye/'
#url = 'https://www.dns-shop.ru/catalog/17a9fd1716404e77/varochnye-paneli-kombinirovannye/'
#url = 'https://www.dns-shop.ru/catalog/751e6ecd3ecb7fd7/aksessuary-k-varochnym-panelyam/'
#url1 = 'https://www.dns-shop.ru/catalog/d18cc20db23e2c90/aksessuary-dlya-podklyucheniya-plit/?virtual_category_uid=1b2de8f7e5a01d05'


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
                    print('1й сценарий: ссылка обработана', len(res), 'ссылок')
                    print(res)
                    return res
                else:
                    print([url])
                    return [url]
            else:
                urls1 = browser.find_element(By.CLASS_NAME,
                                             'subcategory__item-container ').find_elements(
                    By.TAG_NAME, 'a')
                urls2 = [i.get_attribute('href') for i in urls1]
                print(urls2)
                result = []
                for href in urls2:
                    browser = uc.Chrome(main_version=111, crome_options=chrome_options,
                    seleniumwire_options=proxy, headless=False)
                    browser.get(href)
                    browser.set_page_load_timeout(15)
                    browser.add_cookie(cookies)
                    browser.refresh()
                    sleep(2)
                    for _ in range(3):
                        ActionChains(browser).scroll_by_amount(0, 300).perform()
                        sleep(1)
                    if 'Сортировка:' in browser.page_source:
                        print('сортировка нашлась')
                        if 'pagination-widget__pages' in browser.page_source:
                            lst = browser.find_element(By.CLASS_NAME,
                                                       'pagination-widget__pages').find_elements(
                                By.TAG_NAME, 'a')
                            link = [l.get_attribute('href') for l in lst][-1]
                            pagen_last = link.split('=')[-1]
                            res = [f'{href}?p={i}' for i in range(1, int(pagen_last) + 1)]
                            result += res
                            print('2й сценарий: ссылка обработана', len(res), 'ссылок')
                            print(res)
                        else:
                            print(href)
                            result.append(href)
                    browser.quit()
                print(result)
                return result

url_pagen(url)
