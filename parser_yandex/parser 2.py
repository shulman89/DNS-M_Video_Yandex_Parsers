from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import csv
from time import sleep

chrome_options = uc.ChromeOptions()
class Parser:

    def __init__(self,url):
        self.url = url

    def links(self):
        with uc.Chrome(main_version=112, crome_options=chrome_options, headless=False) as browser:
            lst = []
            for i in range(10):
                url = f'https://uslugi.yandex.ru/213-moscow/category?from=suggest&p={i}&text=организатор+мероприятия+москва'
                browser.get(url)
                sleep(2)
                els = browser.find_element(By.CSS_SELECTOR,'#app > div > div.Application-Body > div > div > main').\
                    find_elements(By.CLASS_NAME, 'WorkerCard-Main')
                els = [i.find_element(By.TAG_NAME,'a').get_attribute('href') for i in els]
                lst += els
            lst1 = set(lst)
            lst = list(lst1)
            print(len(lst))
            return lst

    def contacts(self):
        with uc.Chrome(main_version=112, crome_options=chrome_options, headless=True) as browser:
            lst = []
            for link in self.links():
                browser.get(link)
                sleep(5)
                try:
                    browser.find_element(By.CSS_SELECTOR,'.Button2_theme_actionYdo').click()
                    sleep(5)
                    info = browser.find_element(By.CSS_SELECTOR,
                                                'body > div.Modal.Modal_visible.Modal_hasAnimation.Modal_theme_normal.YdoModal.PhoneLoader-OuterModal > div.Modal-Wrapper > div > div > div > div.YdoModal-Content.PhoneLoader-Modal > div.PhoneLoader-PhoneContainer.Align.Align_center').text
                    name = info.split('\n')[1]
                    phone = info.split('\n')[0]
                    lst.append([name, phone, link])
                except Exception:
                    print(link)
                    pass

            print(len(lst))
            return lst

    def write_file(self):
        columns = ['Имя', 'Телефон', 'Ссылка']
        with open('result3.csv', 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(columns)
            for row in self.contacts():
                writer.writerow(row)



par = Parser('https://uslugi.yandex.ru/970-novorossiysk/category?from=suggest&text=%D0%BF%D0%BE%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0+%D0%BF%D0%B5%D1%80%D0%B2%D0%BE%D0%B3%D0%BE+%D1%82%D0%B0%D0%BD%D1%86%D0%B0+%D0%BC%D0%BE%D1%81%D0%BA%D0%B2%D0%B0')
par.write_file()