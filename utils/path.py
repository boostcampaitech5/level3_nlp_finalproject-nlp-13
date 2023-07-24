import json
from unicodedata import normalize

#경로 변경
file_path = "./transfer_file.json"
with open(file_path, "r", encoding='utf-8') as file:
    data = json.load(file)

for i in range(0,len(data['audio'])):
    data['audio'][i]=data['audio'][i].replace('/opt/ml/level3_nlp_finalproject-nlp-13','.')
    data['audio'][i]=normalize('NFC',data['audio'][i])


# 기존 json 파일 덮어쓰기
with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent="\t")