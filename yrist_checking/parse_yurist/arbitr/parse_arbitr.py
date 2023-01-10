# -*- coding: utf-8 -*-
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth
import pandas as pd
import gc
import mail_smtp
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

excel_data = pd.read_excel('/home/specit/data/table.xls')

# INN = '4909084414'

#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#caps = DesiredCapabilities().CHROME
#caps['pageLoadStrategy'] = 'eager'

chrome_options = Options()
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--enable-javascript")
#chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36")
#chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#chrome_options.add_experimental_option('useAutomationExtension', False)

#driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=chrome_options, desired_capabilities=caps)
driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(30)
#driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
driver.get('https://kad.arbitr.ru/')
sleep (5)
try:
    driver.find_element(By.CLASS_NAME, 'b-promo_notification-popup-window').find_element(By.TAG_NAME, 'a').click()
except:
    print('Всплывающего окна нет')
#sleep (0.5)
for row in excel_data.itertuples():
    sleep(5)
    if 8 > len(str(row[1])):
        continue
#    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'reset-link')))
#    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'reset-link')))
    LINK = driver.find_element(By.XPATH, "//a[@href='#']")
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((LINK))).click()
#    LINK.click()
    hoverable = driver.find_element(By.XPATH, '//textarea[@class="g-ph"]')
    ActionChains(driver).move_to_element(hoverable).perform()
    clicpast = driver.find_element(By.XPATH, '//textarea[@class="g-ph"]')
    ActionChains(driver).click(clicpast).send_keys(row[1]).perform()
    sleep (0.3)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'b-button-container'))).click()
    sleep (5)

    element = driver.execute_script("return document.body.innerHTML;")
    soup = BeautifulSoup(element, 'html.parser')
    for i in soup.find_all(class_="js-rolloverHtml"):
        try:
            if row[1] in i.div.span.string:
                print(i.strong.string)
                print(i.div.span.string)
                mail_smtp.smtp('Картотека Арбитражных дел\n' + i.strong.string + '\n' + 'ИНН: ' + row[1])
#                gc.collect()
                break
        except:
#            gc.collect()
            continue

driver.quit()
