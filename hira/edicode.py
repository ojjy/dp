import os.path
import time

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd

import re

from common.utils import project_path

# https://stackoverflow.com/questions/37090653/iterating-through-table-rows-in-selenium-python

url = "http://opendata.hira.or.kr/op/opc/olapDiagBhvPList.do"


chrome_options = webdriver.ChromeOptions()
# chrome_options.headless = True
chrome_options.add_argument("--headless=False")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.get(url=url)

time.sleep(5)

search_textarea = driver.find_element(By.XPATH, '//*[@id="searchWrd1"]')
search_textarea.send_keys('D')
time.sleep(3)

search_btn = driver.find_element(By.XPATH, '//*[@id="searchBtn1"]')
search_btn.click()
time.sleep(3)
edicode_arr = []
table = driver.find_element(By.CSS_SELECTOR, 'table.list-typeC')
# edicode_arr에 D로 검색한 모든 edicode 배열 생성
for row in table.find_elements(By.CSS_SELECTOR,  'tr'):
    for cell in row.find_elements(By.TAG_NAME, 'td'):
        print(cell.text)
        edicode_arr.append(cell.text)

pattern = '^D....$'
result = []
# 생성한 배열중 edicode가 D로 시작하는 데이터만 추출하여 csv파일 생성
for word in edicode_arr:
    if re.match(pattern, word):
        result.append(word)
df = pd.DataFrame(result, columns=['edicode'])
csv_download_path = os.path.join(project_path, "csv_file")
df.to_csv(f"{os.path.join(csv_download_path, 'csv_file/edicode_D.csv')}", index=False)
