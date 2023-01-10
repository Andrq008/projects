# -*- coding: utf-8 -*-
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from pathlib import Path
import PyPDF2
import create_xlsx
import search_rm_xlsx
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

excel_data = pd.read_excel('/home/specit/data/table.xls')

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("window-size=1280,800")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.get('https://egrul.nalog.ru/index.html')
for row in excel_data.itertuples():
    if 8 > len(str(row[1])):
        continue
    if 'nan' in str(row[4]):
        print("Отсутвует название компании")
        with open('nalog.txt', 'a') as f:
            f.write('Отсутвует название компании\n' + row[1] + '\n' + 'None\n')
        continue
    if search_rm_xlsx.rm_xlsx('/home/specit/data/check.xlsx', row[1], 'nalog'):
        print('\n\nОрганизация из списка налогой\n\n')
        continue
    driver.find_element(By.ID, 'query').clear()
    driver.find_element(By.ID, 'query').send_keys(row[1])
    driver.find_element(By.ID, 'btnSearch').click()
    sleep(2)
    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//div[@id="noDataFound"]')))
        with open('nalog.txt', 'a') as f:
            f.write('Компания отсутствует в ЕГРЮЛ/ЕГРИП:\n' + row[1] + '\n' + 'None\n')
        print('Организация отсутствует\n', row[4])
        continue
    except:
        pass

    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//div[@class="res-rownum"]')))
        driver.find_element(By.XPATH, '//div[@id="resultContent"]/div/div[3]/button').click()
    except:
        driver.find_element(By.ID, 'frmCaptcha')
        img = driver.find_element(By.XPATH, '//img[@id="capchaVisual"]').get_attribute('src')
        print(img)
        driver.quit()
        break
    sleep (5)
    files = Path("/home/specit/Загрузки").glob("*.pdf")
    latest_file = max([f for f in files], key=lambda item: item.stat().st_ctime)
    print(latest_file)
    with open(rf'{latest_file}', 'rb') as PDF:
        pdfReader = PyPDF2.PdfFileReader(PDF)
        for PAGE in range(pdfReader.numPages):
            pdfPage = pdfReader.getPage(PAGE)
            if 'БАНКРОТ' in pdfPage.extract_text():
                print('Банкротство\n', row[4])
                with open('nalog.txt', 'a') as f:
                    f.write('Банкротство: ' + row[4] + '\n' + row[1] + '\n' + 'None\n')
                break
#            elif 'ЛИКВИДАЦ' in pdfPage.extract_text():
            elif 'Ликвидация юридического лица' in pdfPage.extract_text():
                print('Ликвидация\n', row[4])
                with open('nalog.txt', 'a') as f:
                    f.write('Ликвидация: ' + row[4] + '\n' + row[1] + '\n' + 'None\n')
    latest_file.unlink()
driver.quit()
create_xlsx.xlsx('nalog.txt', 'nalog')
