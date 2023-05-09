import snowflake.connector
import os
import pandas as pd
import csv
import json

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

with open(f"{project_path}/secret.json", "r", encoding='utf-8') as fp:
    json_contents=json.loads(fp.read())

snowflake_conn = snowflake.connector.connect(
    user=json_contents['sf_user'],
    password=json_contents['sf_pwd'],
    account=json_contents['sf_host'],
    warehouse=json_contents['sf_wh'],
    database=json_contents['sf_db'],
    schema=json_contents['sf_schema'],
    cache_column_metadata=True
)

df = pd.read_sql_query(
    sql=f"SELECT CNSL_CNTN, DIPS_CNTN FROM {json_contents['sf_db']}.ODS.O_CS_CNSL_HST;",
    con=snowflake_conn)
df = df.rename(columns={'CNSL_CNTN':'prompt', 'DIPS_CNTN':'completion'})
# df['CNSL_CNTN'] = df['CNSL_CNTN'].rename
# df['DIPS_CNTN'] = df['DIPS_CNTN'].apply(lambda x: f'"completion": "{x}"')
# print(df)
df.to_csv("input.csv", index=False, encoding='utf-8-sig')


def csv_to_json(csv_file_path, json_file_path):
    with open(csv_file_path, "r", encoding='UTF8') as csv_file:
        csv_reader = csv.DictReader(csv_file, fieldnames=["prompt", "completion"])
        json_data = json.dumps(list(csv_reader), ensure_ascii=False)

    with open(json_file_path, "w", encoding='UTF8') as json_file:
        json_file.write(json_data)

csv_to_json("input.csv", "output.jsonl")