import json
import wave

file_path = "./label1.json"
total=0.0
with open(file_path, "r", encoding='utf-8') as file:
    data = json.load(file)

for i in range(0,len(data['audio'])):
    audio = wave.open(data['audio'][i])
    frames = audio.getnframes()
    rate = audio.getframerate()
    duration = frames / float(rate)
    total+=duration
    
print(total//60) #초 -> 분으로 전환