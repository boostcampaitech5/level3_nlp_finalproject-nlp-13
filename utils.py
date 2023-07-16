import json
from sklearn.model_selection import train_test_split
import os
from tqdm.auto import tqdm
from collections import defaultdict
from pathlib import Path

def set_vocab_dict(path: str):
    # g2p로 변환된 문장으로 vocab.json 파일을 생성합니다.
    with open(path, "r", encoding="utf8") as f:
        f = json.load(f)
    
    vocab = []
    for k, v in f.items():
        for k2, v2 in  v.items():
            vocab.extend(v2)

    vocab_list = list(set(str(vocab).replace(" ", "")))
    vocab_dict = {v: k for k, v in enumerate(vocab_list)}

    vocab_dict["lg"] = len(vocab_dict)
    vocab_dict["br"] = len(vocab_dict)
    vocab_dict["n"] = len(vocab_dict)

    vocab_dict["[UNK]"] = len(vocab_dict)
    vocab_dict["[PAD]"] = len(vocab_dict)
    with open('vocab.json', 'w') as vocab_file:
        json.dump(vocab_dict, vocab_file)


def rearrange_data(data_path: str, wav_path: str):
    '''
    args
        path(str) : after_g2p_sentences.json의 경로
        wav_path(str) : wav 파일들이 들어있는 AI챗봇_원천 폴더의 경로

      after_g2p_sentences파일을 넣으면 학습에 돌릴 수 있는 dict 형태로 변환합니다.
    '''
    current_path = os.getcwd()
    path = current_path + '/AI_HUB/Validation/[라벨]1.AI챗봇'
    path_collection = []
    for path_of_folder in tqdm(Path(path).iterdir(), desc='Collecting path'):
        path_of_folder = path_of_folder.__str__()
        for path_of_file in Path(path_of_folder).iterdir():
            path_of_file = path_of_file.__str__()
            path_of_file = path_of_file.replace('[라벨]1.AI챗봇','AI챗봇_원천')
            path_of_file = path_of_file.replace('json','wav')
            path_collection.append(path_of_file)

    with open(path, "r", encoding="utf8") as f:
        f = json.load(f)
    
    sent = []
    for k, v in f.items():
        for k2, v2 in  v.items():
            sent.append(v2)

    vocab = {"audio": path_collection, "sentence" : sent}
    print(len(vocab['audio']))
    print(len(vocab['sentence']))

    with open('label.json', 'w', encoding='utf-8') as vocab_file:
        json.dump(vocab, vocab_file, ensure_ascii=False)

def train_test(path: str):
    with open(path, "r", encoding="utf8") as f:
        f = json.load(f)
    
    trainx, testx, trainy, testy = train_test_split(f['audio'], f['sentence'], test_size=0.2, shuffle=False, random_state=42)
    print(type(trainx))
    print(trainy[:5])
    print(testx[:5])


if __name__ == "__main__":
        # set_vocab_dict('text_data/after_g2p_sentences.json')
        rearrange_data('text_data/after_g2p_sentences.json')
        # train_test('label.json')
