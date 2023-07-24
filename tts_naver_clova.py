import os
import sys
import urllib.request
from naver_cloud_key import client_id, client_secret
import streamlit as st

def get_sound_with_naver_clova(text: str, 
                               speaker: str = 'nara', 
                               volume: int = 0, 
                               speed: int = 0, 
                               pitch: int = 0, 
                               format: str ='mp3',
                               client_id: str = client_id,
                               client_secret: str = client_secret
                               ) -> bytes:
    '''
    text를 입력으로 받아 Naver Clova Voice TTS API를 통해 음성을 반환하는 함수입니다.
    파라미터를 통해 목소리, 볼륨, 속도, 피치, 파일 형식 등을 바꿀 수 있습니다. 파라미터에 대한 추가 정보는 아래 주소를 참고하세요.
    https://api.ncloud-docs.com/docs/ai-naver-clovavoice-ttspremium
    요금 정보: 기본요금 9만원(1개월), 기본제공 1,000,000개 초과시 글자당 100원
    ## 불필요한 잦은 호출은 피해주시기 바랍니다. ##
    '''


    client_id = client_id # ncloud에서 받은 유료 키이므로 외부 공유 금지
    client_secret = client_secret # ncloud에서 받은 유료 키이므로 외부 공유 금지
    encText = urllib.parse.quote(text)
    data = f"speaker={speaker}&volume={volume}&speed={speed}&pitch={pitch}&format={format}&text=" + encText;
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    request.add_header("X-NCP-APIGW-API-KEY",client_secret)
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()
    if(rescode==200):
        print("TTS mp3 생성")
        response_body = response.read()
        ''' 로컬에 저장해서 mp3/wmv 파일로 듣고 싶을 때 '''
        path = './tts_test.mp3'        
        with open(path, 'wb') as f:
            f.write(response_body)
        audio_file = open(path, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/ogg')
        #return response_body
        #return path
    else:
        print("Error Code:" + rescode)

def get_sound(text: str, 
                               speaker: str = 'nara', 
                               volume: int = 0, 
                               speed: int = 0, 
                               pitch: int = 0, 
                               format: str ='mp3',
                               client_id: str = client_id,
                               client_secret: str = client_secret
                               ) -> bytes:
    path = './tts_test.mp3'   
    audio_file = open(path, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg')

if __name__=="__main__":
    get_sound_with_naver_clova('오늘은 날씨가 맑다')