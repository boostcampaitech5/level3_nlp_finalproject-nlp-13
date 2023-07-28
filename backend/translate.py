import requests
import yaml

with open('flask/api.yaml') as f:
    db_key = yaml.load(f, Loader=yaml.FullLoader)

def papago_translate(text: str, source_language: str, target_language: str) -> str:
    
    # 영어 = en , 중국어 = zh-CN, 일본어 = ja, 베트남어 = vi, 태국어 = th
    # Papago로 한 번에 번역할 수 있는 분량은 최대 5,000자이며, 하루 번역 처리 한도는 10,000자입니다.
    # reference = https://developers.naver.com/docs/papago/papago-nmt-overview.md
    
    
    
    client_id = db_key['ClientID']
    client_secret = db_key['ClientSecret']

    data = {'text' : text,
            'source' : source_language,
            'target': target_language}

    url = "https://openapi.naver.com/v1/papago/n2mt"

    header = {"X-Naver-Client-Id":client_id,
              "X-Naver-Client-Secret":client_secret}

    response = requests.post(url, headers=header, data=data)
    rescode = response.status_code

    if(rescode==200):
        send_data = response.json()
        trans_data = (send_data['message']['result']['translatedText'])
        return trans_data
    else:
        print("Error Code:" , rescode)