"""
진료행위
http://opendata.hira.or.kr/op/opc/olapDiagBhvInfo.do
"""
import os.path
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import shutil


from common.utils import project_path, set_downloads_folder


def add_lst(code):
        global failed_lst
        failed_lst.append(code)

class OpendataCrawler(object):
    def __init__(self, url, md_code, data_btn ,directory , by):
        self.url = url
        self.md_code = md_code
        self.data_btn = data_btn
        #self.count = count
        self.directory = directory
        self.by = by


    def crawl_data(self):
        url = 'http://opendata.hira.or.kr/op/opc/olapDiagBhvInfo.do'
        system_name = "hira"
        table_name = "medical_practice"
        download_folder_fullpath = set_downloads_folder(system_name=system_name, table_name=table_name)
        chrome_options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': download_folder_fullpath}
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.headless = False
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)

        for code in self.md_code:
            try:
                print(code)
                driver.get(url)
                # main : 메인 창
                main = driver.current_window_handle
                driver.find_element(By.XPATH, '//*[@id="searchPopup"]').click()

                # popup : 팝업 창
                popup = driver.window_handles
                driver.switch_to.window(popup.pop())
                driver.implicitly_wait(20)

                # 코드명으로 데이터 조회
                driver.find_element(By.XPATH, '//*[@id="searchWrd1"]').send_keys(code)


                # 진료행위명칭 클릭
                driver.find_element(By.CSS_SELECTOR, 'a[id="searchBtn1"]').send_keys("\n")
                driver.implicitly_wait(20)
                driver.find_element(By.XPATH, '//*[@id="tab1"]/section[2]/table/tbody/tr/td[2]/a').click()

                # 메인 창으로 전환
                driver.switch_to.window(main)
                driver.find_element(By.XPATH, self.data_btn).click()

                # iframe : iframe 영역
                iframe = driver.find_element(By.CLASS_NAME, 'olapViewFrame')
                driver.switch_to.frame(iframe)
                driver.implicitly_wait(20)

                #iframe
                wait = WebDriverWait(driver, 20)
                ## 진료년월 라디오 버튼
                radio = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ext-gen1645"]/table/tbody/tr/td/div[2]/table/tbody/tr/td/ul/li[2]/label/input')))
                radio = driver.find_element(By.XPATH, '//*[@id="ext-gen1645"]/table/tbody/tr/td/div[2]/table/tbody/tr/td/ul/li[2]/label/input')
                driver.execute_script("arguments[0].click();", radio)
                time.sleep(3)

                ### 검색 시작 날짜 선택
                from_date = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='ext-gen1645']/table/tbody/tr/td/div[4]/div/input[1]")))
                from_date.click()

                # ## 정규표현식으로 id 찾기 (monthpicker 값이 페이지 로드 마다 계속해서 바뀜)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                mpid = soup.find_all(id=lambda x: x and x.startswith('monthpicker_'))
                # print(mpid[0].attrs['id'])
                # print(mpid[1].attrs['id'])

                # 수정사항 끝의 진료년월은 어차피 그 해당달로 변경되어 시작날짜만 조절하게 변경 시작년도월은 오늘달의 2년전의 1월
                ## 달력에서 년도 선택
                # //*[@id="monthpicker_03292706759513271"]/div/select/option[9]
                # //*[@id="monthpicker_0023860746457632996"]/div/select/option[12]
                from_year_xpath = f"//*[@id='{mpid[0].attrs['id']}']/div/select/option[12]"
                from_year = wait.until(EC.visibility_of_element_located((By.XPATH, from_year_xpath)))
                from_year.click()

                ## 달력에서 월 선택
                from_month_xpath = f"//*[@id='{mpid[0].attrs['id']}']/table/tbody/tr[1]/td[1]"
                from_month = wait.until(EC.visibility_of_element_located((By.XPATH, from_month_xpath)))
                from_month.click()
                #
                time.sleep(5)
                radio = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ext-gen1645"]/table/tbody/tr/td/div[2]/table/tbody/tr/td/ul/li[2]/label/input')))
                radio = driver.find_element(By.XPATH, '//*[@id="ext-gen1645"]/table/tbody/tr/td/div[2]/table/tbody/tr/td/ul/li[2]/label/input')
                driver.execute_script("arguments[0].click();", radio)

                ## 조회 버튼
                search_btn = driver.find_element(By.CLASS_NAME, "dt-btn-search")
                driver.execute_script("arguments[0].click();", search_btn)

                time.sleep(10)
                # print("try")
                # datagrid1 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ext-gen1018 > div.fullscreen_content')))
                # datagrid = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#panel-1184-body > div.dock_main > div.dock_inner div.m-datagrid-cell')))

                driver.implicitly_wait(30)
                ## 조회된 데이터가 없는 경우

                ## 엑셀파일 다운로드
                # download_excel : 엑셀 다운로드 하는 버튼

                print("excel downloads")
                                                               # //*[@id="panel-1184-body"]/div[2]/div[1]/div[1]/div[2]/div[1]
                download_excel = driver.find_element(By.XPATH, '//*[@id="panel-1184-body"]/div[2]/div[1]/div[1]/div[2]/div[1]')
                driver.execute_script("arguments[0].click();", download_excel)
                print(f"{code} 다운로드 완료")
                time.sleep(10)

                ## driver 종료
                driver.implicitly_wait(20)
            except Exception as e:
                print(f"error occur: {e} :: 다운로드 미완료 -> {code}")

        driver.close()



if __name__ == "__main__":
    # instiution_btn : 요양기관종별 , location_btn : 요양기관소재지별 , directory : csv_file 파일 다운로드 되는 위치 (수정 필요)
    institution_btn = '/html/body/section[1]/section[2]/div[1]/ul/li[4]'
    location_btn = '/html/body/section[1]/section[2]/div[1]/ul/li[5]'
    by_institution = '1_진료행위요양기관그룹별현황'
    by_location = '1_진료행위요양기관소재지별현황'
    url = 'http://opendata.hira.or.kr/op/opc/olapDiagBhvInfo.do'
    directory = os.path.join(project_path, 'csv_file')
    print(directory)
    # directory = 'C:\\Users\\sm\\Downloads\\'

    # mdfeeCd_lst : 진료행위 코드 리스트
    df = pd.read_csv(f"{os.path.join(directory, 'edicode_D.csv')}")
    print(df)
    mdfeeCd_lst = df['edicode']
    # url, md_code, data_btn , count , directory , by):
    ## crawler_ins1 : 요양기관종별 데이터 크롤링
    print ('crawling Data ..............')
    # crawler_ins1 = OpendataCrawler(url, mdfeeCd_lst, institution_btn, directory , by_institution)
    crawler_ins1 = OpendataCrawler(url, mdfeeCd_lst, location_btn, directory , by_location)
    crawler_ins1.crawl_data()