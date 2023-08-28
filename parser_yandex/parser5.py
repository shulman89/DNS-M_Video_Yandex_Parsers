from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import csv
from proxy import proxy
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains



chrome_options = uc.ChromeOptions()
class Parser:


    @staticmethod
    def table_info():
        url = 'https://yandex.ru/maps/15/tula/search/%D1%82%D1%83%D0%BB%D0%B0%20%D1%81%D1%82%D1%80%D0%BE%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D1%81%D1%82%D0%B2%D0%BE%20%D0%B4%D0%BE%D0%BC%D0%BE%D0%B2/?ll=37.589622%2C54.181173&sll=37.618551%2C54.181173&sspn=0.660107%2C0.237033&z=11.13'
        with uc.Chrome(main_version=111, crome_options=chrome_options,
                       seleniumwire_options=proxy, headless=True) as browser:
            browser.get(url)
            sleep(5)
            action = ActionChains(browser)
            for _ in range(40):
                sleep(3)
                action.scroll(150, 300, 0, 5000,1).perform()

            url_list = browser.find_elements(By.CLASS_NAME,'search-snippet-view')
            url_list = [i.find_element(By.TAG_NAME,"a").get_attribute('href') for i in url_list]

            res_list = []
            for url in url_list:
                browser.get(url)
                sleep(3)
                name = browser.find_element(By.CLASS_NAME,'orgpage-header-view__header').text
                try:
                    link = browser.find_element(By.CLASS_NAME,'business-urls-view__text').text
                except Exception:
                    link = 'Сайта нет'
                try:
                    browser.find_element(By.CLASS_NAME,'card-phones-view__more').click()
                except Exception:
                    pass
                try:
                    phone = browser.find_element(By.CLASS_NAME,'card-phones-view__phone-number').text
                except Exception:
                    phone = 'Номера нет'
                try:
                    adress = browser.find_element(By.CLASS_NAME,'business-contacts-view__address-link').text
                except Exception:
                    adress = 'Адреса нет'
                res_list.append([name,adress,phone,link])


            print(res_list)
            return res_list

    @classmethod
    def write_file(cls):
        columns = ['Название', 'Адрес', 'Телефон', 'Ссылка']
        with open('Tula2.csv', 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(columns)
            for row in Parser.table_info():
                writer.writerow(row)


def main():
    Parser.write_file()

if __name__ == '__main__':
    main()




