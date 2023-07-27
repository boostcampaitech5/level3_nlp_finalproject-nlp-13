import json
from unicodedata import normalize
import pandas as pd

#json 파일 경로 변경
file_path = "./transfer_file.json"
with open(file_path, "r", encoding='utf-8') as file:
    data = json.load(file)
    
for i in range(0,len(data['audio'])):
    data['audio'][i]=data['audio'][i].replace('/opt/ml/level3_nlp_finalproject-nlp-13','.')
    data['audio'][i]=normalize('NFC',data['audio'][i])


# 기존 json 파일 덮어쓰기
with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent="\t")


#csv 파일 경로 변경 
df = pd.read_csv('./foreign_audio.csv', encoding='UTF-8')

for i in range(0,len(df)):
    df.iloc[i,0]=df.iloc[i,0].replace('\\','/')
    
#기존 csv 파일 덮어쓰기
df.to_csv('./foreign_audio.csv',index=False)