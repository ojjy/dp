import shutil

from common.utils import set_downloads_folder
import pandas as pd
import os
import glob
import openpyxl
import pyexcel as p

def convert_xls_xlsx(xlsfullpath, system_name, table_name, **kwargs):
    """
    xlsfullpath를 입력값으로 받아 pyexcel라이브러리를 이용하여 xls를 xlsx로 바꾼다음, pandas라이브러리를 이용하여 xlsx를 csv로 변환한다.
    :param xlsfullpath:
    :param table_name:
    :param kwargs:
    :return:
    """
    if 'from_date' in kwargs:
        target_filename = f"{table_name}_{kwargs['from_date']}_{kwargs['to_date']}_{kwargs['to_time']}.xlsx"
    else:
        target_filename = f"{table_name}_{kwargs['data_date']}.xlsx"
    target_filefullpath = os.path.join(set_downloads_folder(system_name=system_name, table_name=table_name), target_filename)
    print(f"source xls full path: {xlsfullpath} -> target xlsx full path: {target_filefullpath}")

    # 아래 save_as를 하지 않으면 bigint의 경우 짤려서 E+10형태로 데이터가 select된다.이를 방지하기 위해 save_book_as
    p.save_book_as(file_name=xlsfullpath,
                   dest_file_name=target_filefullpath)
    print(f"target_filefullpath: {target_filefullpath}, type(target_filefullpath): {type(target_filefullpath)}")
    csv_filefullpath = target_filefullpath.replace(".xlsx", ".csv")
    print(f"csv_filefullpath: {csv_filefullpath}")
    df = pd.read_excel(target_filefullpath)
    df.to_csv(csv_filefullpath, encoding='utf-8-sig', index=False)
    return csv_filefullpath

if __name__ =="__main__":
    system_name = "hira"
    table_name = "medical_practice"
    download_path = set_downloads_folder(system_name=system_name, table_name=table_name)
    print(download_path)
    for filefullpath in glob.glob(os.path.join(download_path, '1_진료행위요양기관소재지별현황(진료년월)*.xls')):
        p.save_book_as(file_name=filefullpath,
                       dest_file_name=filefullpath.replace('xls', 'xlsx'))
        df = pd.read_excel(filefullpath.replace('xls', 'xlsx'), engine='openpyxl', index_col=False)
        try:
            print(df['1. 진료행위 요양기관소재지별 현황(진료년월)'][9])
            print(f"{filefullpath}")
            stat_df = pd.read_excel(filefullpath.replace('xls', 'xlsx'), engine='openpyxl', index_col=False, header=6)
            # print(stat_df)
            index = stat_df.columns.tolist()
            print(f" start_dd :: {index[3].split('.')[0].replace(' ', '')}, end_dd:: {index[-1].split('.')[0].replace(' ', '')}, filename: {table_name}_{stat_df['Unnamed: 0'][1]}_{index[3].split('.')[0].replace(' ', '')}_{index[-1].split('.')[0].replace(' ', '')}.xlsx")
            # shutil.copyfile(src=filefullpath.replace('xls', 'xlsx'), dst=os.path.join(download_path, f"{table_name}_{stat_df['Unnamed: 0'][1]}_{index[3].split('.')[0].replace(' ', '')}_{index[-1].split('.')[0].replace(' ', '')}.xlsx"))
            stat_df.drop(index=[0,6], inplace=True)
            # print(stat_df)
            convert_filename = f"{table_name}_{stat_df['Unnamed: 0'][1]}_{index[3].split('.')[0].replace(' ', '')}_{index[-1].split('.')[0].replace(' ', '')}.csv"
            stat_df.to_csv(os.path.join(set_downloads_folder(system_name="hira", table_name=table_name), convert_filename), index=False, encoding='utf-8-sig')
        except Exception as e:
            print(f"{filefullpath} is empty file")
