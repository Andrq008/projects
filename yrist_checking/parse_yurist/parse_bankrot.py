# -*- coding: utf-8 -*-
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import gc
import create_xlsx
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import search_rm_xlsx

excel_data = pd.read_excel('/home/specit/data/table.xls')

INN = '7811464750'

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument('--disable-dev-shm-usage')
#chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.get('https://old.bankrot.fedresurs.ru/DebtorsSearch.aspx')
sleep(5)
for row in excel_data.itertuples():
    if 10 == len(str(row[1]).replace(' ', '')):
        if search_rm_xlsx.rm_xlsx('/home/specit/data/check.xlsx', row[1], False):
            print('\n\nОрганизация из списка налогой\n\n')
            continue
        if search_rm_xlsx.rm_xlsx('/home/specit/data/check.xlsx', row[1], 'bankrot'):
            print('\n\nОрганизация из списка\n\n')
            continue
        driver.find_element(By.ID, 'ctl00_cphBody_rblDebtorType_0').click()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'ctl00_cphBody_ibSroClear'))).click()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'ctl00_cphBody_OrganizationCode1_CodeTextBox'))).send_keys(row[1])
        driver.find_element(By.ID, 'ctl00_cphBody_btnSearch').click()
        sleep (5)
        element = driver.execute_script("return document.body.innerHTML;")
        soup = BeautifulSoup(element, 'lxml')
        num = soup.find(id="ctl00_cphBody_gvDebtors").find_all_next("a")
        for i in num:
            try:
                print(i.attrs["title"])
                with open('bankrot.txt', 'a') as f:
                    f.write(row[4] + '\n' + row[1] + '\n' + 'None' + '\n')
                gc.collect()
            except:
                gc.collect()
                continue
    elif 12 == len(str(row[1]).replace(' ', '')):
        driver.find_element(By.ID, 'ctl00_cphBody_rblDebtorType_1').click()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'ctl00_cphBody_ibSroClear'))).click()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'ctl00_cphBody_PersonCode1_CodeTextBox'))).send_keys(row[1].replace(' ', ''))
        driver.find_element(By.ID, 'ctl00_cphBody_btnSearch').click()
        sleep (5)
        element = driver.execute_script("return document.body.innerHTML;")
        soup = BeautifulSoup(element, 'lxml')
        num = soup.find(id="ctl00_cphBody_gvDebtors").find_all_next("a")
        for i in num:
            try:
                print(i.attrs["title"])
                with open('bankrot.txt', 'a') as f:
                    f.write(row[4] + '\n' + row[1] + '\n' + 'None\n')
                gc.collect()
            except:
                gc.collect()
                continue

driver.quit()
create_xlsx.xlsx('bankrot.txt', 'bankrot')
