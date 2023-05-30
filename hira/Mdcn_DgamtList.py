"""
개발자: 조예진
개발일: 20210621
함수명: DgamtList
테이블명: Mdcn_DgamtList
설명: 약가목록_약가기준정보조회서비스_건강보험심사평가원_공공데이터포털
약품코드, 품목명, 제조업체명을 통해 적용 중 인 약가의 적용시작일자, 규격, 투여경로, 급여구분, 상한가, 약품의 주성분코드 등을 조회하는 약가목록조회 기능
https://www.data.go.kr/data/15054445/openapi.do
==========  2022-01-03 21:40:43 Mdcn_DgamtList 실행시작 ==========
{'adtStaDd': 8, 'chgAfMdsCd': 9, 'chgbfmdscd': 9, 'expTpTxt1': 4, 'expTpTxt2': 4, 'expTpTxt3': 4, 'gnlNmCd': 9, 'injcPthNm': 2, 'itmNm': 231, 'lprcEssAddcCuprc': 4, 'lprcEssTpNm': 5, 'mdsCd': 9, 'meftDivNo': 3, 'mnfEntpNm': 52, 'mxCprc': 8, 'nomNm': 10, 'optCpmdImplTpNm': 8, 'payTpNm': 4, 'sbstPsblTpNm': 9, 'sellEptDd': 8, 'spcGnlTpNm': 4, 'unit': 12, 'REGT_ID': 7, 'REG_DTTM': 19}
Mdcn_DgamtList테이블 row총갯수: 89635개, 테이블용량:15.55MB, 테이블설명: 약가목록_약가기준정보조회서비스_건강보험심사평가원_공공데이터포털
==========  2022-01-03 21:59:09 Mdcn_DgamtList 실행완료 ==========
"""
import pandas as pd
import requests
import json
import os
from datetime import datetime
import math
from string import ascii_uppercase
from libs.dputils import nullify, get_max_length, set_db_connect, truncate_table, get_table_info
import A_SECRET
import urllib.parse
from sqlalchemy import create_engine



def Mdcn_DgamtList(url_prefix, url_parameters, numOfRows, table_name):
    """
    알파벳리스트와 숫자 리스트를 합쳐서 코드 리스트를 만들고 이 리스트만큼 for 문을 돌려서 코드에 맞는 약가 목록을 가져온다.
    :param table_name:
    :return:
    """
    input_list =  list(range(0,10))+list(ascii_uppercase)
    truncate_table(table_name)
    password = urllib.parse.quote_plus(f"{A_SECRET.MARIADB_PASSWORD}")
    engine = create_engine(
        f"mysql+pymysql://{A_SECRET.MARIADB_USER}:{password}@{A_SECRET.MARIADB_HOST}:{A_SECRET.MARIADB_PORT}/{A_SECRET.MARIADB_PDBNAME}")

    for input_params in input_list:
        url = f"{url_prefix}{url_parameters}&mdsCd={input_params}"
        print(url)
        res = requests.get(url=url, allow_redirects=False).text
        json_data = json.loads(res)
        totalCount = json_data['response']['body']["totalCount"]
        maxpageno = math.ceil(totalCount / numOfRows)
        print(totalCount, maxpageno)

        for pageno in range(1, maxpageno + 1):
            url = f"{url_prefix}{url_parameters}&mdsCd={input_params}&pageNo={pageno}"
            print(pageno, end=' ')
            res = requests.get(url=url, allow_redirects=False).text
            json_data = json.loads(res)
            items = json_data['response']['body']['items']['item']
            df = pd.DataFrame(items)
            df['REGT_ID'] = 'yejinjo'
            df['REG_DTTM'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # print(df)
            df.to_sql(name=f"{table_name}".lower(), con=engine, if_exists="append", index=False)
            with set_db_connect() as conn:
                conn.commit()
        print()

def main():
    table_name = os.path.basename(__file__).replace(".py", "")
    url_prefix = "http://apis.data.go.kr/B551182/dgamtCrtrInfoService/getDgamtList?"
    numOfRows = 100
    url_parameters = f"_type=json&numOfRows={numOfRows}&serviceKey={A_SECRET.ServiceKey}"
    print(f"==========  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {table_name} 실행시작 ==========")
    Mdcn_DgamtList(url_prefix, url_parameters, numOfRows, table_name)
    get_max_length(table_name)
    get_table_info(table_name)
    print(f"==========  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {table_name} 실행완료 ==========")

if __name__ == "__main__":
    main()


def DUR_UsjntTabooInfoList(url_prefix, url_parameters, numOfRows, table_name):
    url = f"{url_prefix}{url_parameters}"
    print(url)
    res = requests.get(url=url, allow_redirects=False).text
    json_data = json.loads(res)
    totalCount = json_data['body']["totalCount"]
    maxpageno = math.ceil(totalCount / numOfRows)
    print(totalCount, maxpageno)
    truncate_table(table_name)
    password = urllib.parse.quote_plus(f"{A_SECRET.MARIADB_PASSWORD}")
    engine = create_engine(
        f"mysql+pymysql://{A_SECRET.MARIADB_USER}:{password}@{A_SECRET.MARIADB_HOST}:{A_SECRET.MARIADB_PORT}/{A_SECRET.MARIADB_PDBNAME}")

    for pageno in range(1, maxpageno + 1):
        url = f"{url_prefix}{url_parameters}&pageNo={pageno}"
        print(pageno, end=' ')
        res = requests.get(url=url, allow_redirects=False).text
        json_data = json.loads(res)
        items = json_data["body"]["items"]
        df = pd.DataFrame(items)
        df['REGT_ID'] = 'yejinjo'
        df['REG_DTTM'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df.to_sql(name=f"{table_name}".lower(), con=engine, if_exists="append", index=False, chunksize=8000)
        with set_db_connect() as conn:
            conn.commit()
    print()


