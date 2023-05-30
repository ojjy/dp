# coding=utf8
# REST API 호출에 필요한 라이브러리
import pandas as pd
import requests
import json
import pandas

# [내 애플리케이션] > [앱 키] 에서 확인한 REST API 키 값 입력
REST_API_KEY = '62a9501da452ac247ae00e100c20f8ef'

# KoGPT API 호출을 위한 메서드 선언
# 각 파라미터 기본값으로 설정
def kogpt_api(prompt, max_tokens = 1, temperature = 1.0, top_p = 1.0, n = 1):
    r = requests.post(
        'https://api.kakaobrain.com/v1/inference/kogpt/generation',
        json = {
            'prompt': prompt,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'top_p': top_p,
            'n': n
        },
        headers = {
            'Authorization': 'KakaoAK ' + REST_API_KEY,
            'Content-Type': 'application/json'
        }
    )
    # 응답 JSON 형식으로 변환
    response = json.loads(r.content)
    return response

df = pd.read_csv('input.csv', encoding='utf-8-sig')
print(df)

# KoGPT에게 전달할 명령어 구성
prompt = f'''prd_nm가 메타바이오틱스 신애라 유산균 1통+1통의 상품을 review_dtl_cntn을 이용하여 평가 합니다. 
{df}
'''

# 파라미터를 전달해 kogpt_api()메서드 호출
response = kogpt_api(
    prompt = prompt,
    max_tokens = 1024,
    temperature = 1.0,
    top_p = 1.0,
    n = 10
)

print(response['generations'])

values = response['generations']

df = pd.DataFrame.from_dict(values)
df.to_csv('result.csv', index=False, header=True, encoding='utf-8-sig')
for value in values:
    print(value)