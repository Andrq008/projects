# -*- coding: utf-8 -*-
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import parse_img
import Optical_Character
import pandas as pd
import gc
import create_xlsx
import search_rm_xlsx
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

excel_data = pd.read_excel('/home/specit/data/table.xls')

caps = DesiredCapabilities().CHROME
caps['pageLoadStrategy'] = 'eager'

chrome_options = Options()
chrome_options.add_argument("start-maximized")

chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--enable-javascript")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

print('Ввод данных')
driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=chrome_options, desired_capabilities=caps)
driver.implicitly_wait(30)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.get('https://fssp.gov.ru/iss/iP')
ERR_CAPCHA = False
BY = 0
for row in excel_data.itertuples():
    if 10 == len(str(row[1]).replace(' ', '')):
        if search_rm_xlsx.rm_xlsx('/home/specit/data/check.xlsx', row[1], False):
            print('\n\nОрганизация из списка налогой\n\n')
            continue
        try:
            if search_rm_xlsx.rm_xlsx('/home/specit/data/check.xlsx', row[1], 'fssp'):
                print('\n\nОрганизация из списка\n\n')
                continue
        except:
            pass
        while [True]:
            BY += 1
            if 11 == BY:
                BY = 0
                gc.collect()
                driver.quit()
                sleep(600)
                driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=chrome_options, desired_capabilities=caps)
                driver.implicitly_wait(30)
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                driver.get('https://fssp.gov.ru/iss/iP')
            print('Проход: ', BY)
            if ERR_CAPCHA:
                ERR_CAPCHA = False
                continue
            try:
                WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH, "//form/div/div/div[2]/label"))).click()
            except:
                driver.refresh()
                with open('not_search.txt', 'a') as f:
                    f.write('\n' + row[1] + '\n')
                continue
            sleep (0.5)
            # select_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "chosen-search-input"))).clear()
            try:
                select_element = driver.find_element(By.CLASS_NAME, "chosen-search-input").clear()
                select_element = driver.find_element(By.CLASS_NAME, "chosen-search-input").send_keys('Все регионы')
                select_element = driver.find_element(By.CLASS_NAME, "chosen-search-input").send_keys(Keys.ENTER)
                sleep (0.3)
                driver.find_element(By.ID, 'input03').clear()
                driver.find_element(By.ID, 'input03').send_keys(row[4])
                driver.find_element(By.ID, 'input07').clear()
                sleep (0.3)
                driver.find_element(By.ID, 'input07').send_keys(row[6])
                # driver.find_element(By.ID, 'input10').send_keys(INN)
                # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'input10'))).send_keys(INN)
                sleep (0.3)
                driver.find_element(By.ID, 'btn-sbm').click()
                print('Начало поиска')
            except:
                continue

            # try:
                # WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//input[@id="ncapcha-submit"]')))
                # TOCKER = False
            # except:
                # pass
            TOCKER = False
            j = 0
            while [True]:
                if TOCKER:
                    break
                j = j + 1
                if j > 18:
                    print('Произошла ошибка')
                    driver.refresh()
                    ERR_CAPCHA = True
                    break
                print(j)
                try:
                    sleep (0.5)
                    WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, '//input[@id="ncapcha-submit"]')))
                    print('Загрузка изображения')
                    sleep (0.5)
                    img = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//img[@id="capchaVisual"]'))).get_attribute('src')
                    parse_img.down_img(img)
                    print('Распознование изображения')
                    capcha = Optical_Character.optical_img()
                    if len(capcha) < 2:
                        capcha = 'not'
                        print('Не распознано')
                    print(capcha)
                    print(capcha.replace("|", ""))
                    sleep (0.5)
                    print('Проверка Капчи')
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//input[@id="captcha-popup-code"]'))).send_keys(capcha.replace("|", ""))
                    sleep (0.5)
                    driver.find_element(By.XPATH, '//input[@id="ncapcha-submit"]').click()
                except:
                    print('Есть совпадение')
                    break

            print('Ожидание загрузки страницы')
            try:
                WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="results"]')))
                print('Проверяется, сформирована ли таблица')
                TOCKER = True
                WebDriverWait(driver, 25).until(EC.visibility_of_element_located((By.XPATH, '//html/body/div/main/section/div/div/div/div/div/div/table')))
            except:
                print('Произошла ошибка, страница не загрузиась')
                print('Нет результат')
                element = driver.execute_script("return document.body.innerHTML;")
                soup = BeautifulSoup(element, 'html.parser')
                page_pass = soup.find(class_="results")
                if page_pass:
                    try:
                        if 'перегружена' in page_pass.div.div.next_element.string:
                            with open('not_search.txt', 'a') as f:
                                f.write('\n' + row[1] + '\n')
                            continue
                        print(page_pass.div.div.next_element.string)
                        result = page_pass.div.div.next_element.string
                        print(result)
                        gc.collect()
                        break
                    except:
                        with open('not_search.txt', 'a') as f:
                            f.write('\n' + row[1] + '\n')
                        driver.refresh()
                        gc.collect()
                        continue
                with open('not_search.txt', 'a') as f:
                    f.write('\n' + row[1] + '\n')
                driver.refresh()
                gc.collect()
                continue
            
            print('Готовится результат')
            element = driver.execute_script("return document.body.innerHTML;")
            soup = BeautifulSoup(element, 'html.parser')
            attr = soup.find('table', class_="alt-p05")
            if attr:
                for i in attr.tbody.tr.find_all_next("td"):
                    try:
                        if row[1] in i:
                            print(i.next_element.replace(",", ""))
                            result = i.next_element.replace(",", "")
                            with open('fssp.txt', 'a') as f:
                                f.write(row[4] + '\n' + row[1] + '\n' + 'None\n')
                            print(result)
                            gc.collect()
                            break
                    except:
                        continue
                break
driver.quit()
create_xlsx.xlsx('fssp.txt', 'fssp')