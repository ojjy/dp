import snowflake.connector
import os
import pandas as pd
import csv
import json
from sqlalchemy import create_engine

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

with open(f"{project_path}/secret.json", "r", encoding='utf-8') as fp:
    json_contents=json.loads(fp.read())


snowflake_conn = create_engine(f'snowflake://{json_contents["sf_user"]}:{json_contents["sf_pwd"]}@{json_contents["sf_host"]}/{json_contents["sf_db"]}/'
                       f'{json_contents["sf_schema"]}?warehouse={json_contents["sf_wh"]}&role={json_contents["sf_role"]}')

# snowflake_conn = snowflake.connector.connect(
#     user=json_contents['sf_user'],
#     password=json_contents['sf_pwd'],
#     account=json_contents['sf_host'],
#     warehouse=json_contents['sf_wh'],
#     database=json_contents['sf_db'],
#     schema=json_contents['sf_schema'],
#     cache_column_metadata=True
# )
# df = pd.read_sql_query(
#     sql=f"-- SELECT CNSL_CNTN, DIPS_CNTN FROM {json_contents['sf_db']}.ODS.O_CS_CNSL_HST;",
#     con=snowflake_conn)



df = pd.read_sql_query(
    sql=f"SELECT PRD_NM, REVIEW_DTL_CNTN  FROM {json_contents['sf_db']}.{json_contents['sf_schema']}.O_NAVER_STORE_COMMENT ORDER BY REV_REG_DD DESC;",
    con=snowflake_conn)
df = df.rename(columns={'CNSL_CNTN':'prompt', 'DIPS_CNTN':'completion'})
df.to_csv("input.csv", index=False, encoding='utf-8-sig')


def csv_to_json(csv_file_path, json_file_path):
    with open(csv_file_path, "r", encoding='UTF8') as csv_file:
        csv_reader = csv.DictReader(csv_file, fieldnames=["prompt", "completion"])
        json_data = json.dumps(list(csv_reader), ensure_ascii=False)

    with open(json_file_path, "w", encoding='UTF8') as json_file:
        json_file.write(json_data)

csv_to_json("input.csv", "output.jsonl")


# HOW TO DELETE MODEL BY USING API
#
# import openai
#
# openai.api_key = json_contents['chatgpt_apikey']
# openai.Model.delete('curie:ft-personal-2023-05-09-06-16-33')