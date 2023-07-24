import csv
import json
import pandas as pd

#csv file to json file

df = pd.read_csv('foreign_audio_shuffled.csv', encoding='UTF-8')
print(df)

data={
    'audio':[],
    'sentence':[]
}

for i in range(0,len(df)):
    data['audio'].append(df.iloc[i,0])
    data['sentence'].append(df.iloc[i,2])

with open('data.json', 'w') as json_file:
    json.dump(data, json_file)