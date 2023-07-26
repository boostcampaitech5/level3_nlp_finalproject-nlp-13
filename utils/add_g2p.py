import csv
import json
import pandas as pd

df = pd.read_csv('../foreign_audio_shuffled.csv', encoding='UTF-8')
df2 = pd.read_csv('../foreign_audio.csv', encoding='UTF-8')
print(df)
df2['sen']='hi'
for i in range(0,len(df)):
    tmp=df[df['path']==df2.iloc[i,0]]
    df2.iloc[i,3]=tmp['sentence']
print(df2)
df2.to_csv('../foreign_audio.csv',index=False)