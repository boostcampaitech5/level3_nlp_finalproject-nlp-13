from g2pk import G2p
import json
from tqdm.auto import tqdm
import re
import pandas as pd
from pathlib import Path

g2p = G2p()

def process_json(path):
    '''
    한국어 자유대화 스크립트 데이터를 전처리하여 토큰을 넣은 코드입니다.
    '''
    with open(path, 'r', encoding='utf-8') as f:
        f = json.load(f)

    for i in range(15):
        sent = []
        for path in tqdm(f['audio'][(i)*10000:(i+1)*10000], desc='g2p'):
            path = path.replace('wav', 'json')
            path = path.replace('원천', '라벨')
            with open(path, 'r', encoding='utf-8') as label:
                label = json.load(label)

            stt = label['발화정보']['stt']
            stt = g2p(stt, descriptive=True, group_vowels=True)
            stt = re.sub('[\[\]]', '', stt)
            stt = re.sub('\(노:\)', 'NO', stt)
            stt = re.sub('\(SN:\)', 'SN', stt)
            stt = re.sub('\(SP:', '', stt)
            stt = re.sub('\(FP:', '', stt)
            stt = re.sub('\(.*\)', '', stt)
            stt = re.sub('[^가-힣A-Z ]', '', stt)
            stt = re.sub('NO', '[NO]', stt)
            stt = re.sub('SN', '[SN]', stt)
            stt = re.sub('\s+', ' ', stt)
            sent.append(stt)
        result = {'audio': f['audio'][(i)*10000:(i+1)*10000], 'sentence': sent}
        with open(f'label{i+1}.json', 'w', encoding='utf-8') as output:
            json.dump(result, output, indent = 4, ensure_ascii=False)
            print(f"SUCCESSFULLY SAVED label{i+1}.json")

def process_csv(path):
    '''
    외국인 한국어 발화 음성 데이터 스크립트를 G2P를 진행 후 전처리를 한 코드입니다.
    '''
    data = pd.read_csv(path)
    sent = []
    for stt in tqdm(data['origin'], desc='G2P'):
        stt = re.sub('un/', 'UNK', stt)
        stt = re.sub('sn/', 'SN', stt)
        stt = re.sub('n/', 'NS', stt)
        stt = g2p(stt, descriptive=True, group_vowels=True)
        stt = re.sub('[^가-힣A-Z ]', '', stt)
        stt = re.sub('NS', '[NO]', stt)
        stt = re.sub('SN', '[SN]', stt)
        stt = re.sub('UNK', '[UNK]', stt)
        stt = re.sub('\s+', ' ', stt)
        sent.append(stt)
    data['sentence'] = sent

    data.to_csv(path, index=False)

def collect_path(path):
    path_collection = []
    for path_of_folder in tqdm(Path(path).iterdir(), desc='Collecting path'):
        path_of_folder = path_of_folder.__str__()
        for path_of_file in Path(path_of_folder).iterdir():
            path_of_file = path_of_file.__str__()
            path_collection.append([path_of_file, "string"])

    output = pd.DataFrame(sorted(path_collection),columns=['audio', 'sentence'])
    output.to_csv("tts_path.csv", index=False)

def reorder(data):
    data = pd.read_csv(data)
    data['path'] = data['path'].str.replace("\\", "/")
    data = data.sort_values(by=['path'])
    data.to_csv("data.csv", index=False)


if __name__ == "__main__":
    process_csv('test/foreign_audio.csv')
    # collect_path('/opt/ml/input/level3_nlp_finalproject-nlp-13/data/ncloud_tts_data')