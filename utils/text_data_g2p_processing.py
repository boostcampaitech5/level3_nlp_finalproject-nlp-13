from g2pk import G2p
from collections import defaultdict
import json
from pathlib import Path
import os
from tqdm.auto import tqdm



def make_path_collection(path: str) -> 'dict[str:list]':
    '''
    입력값 : string (예시 - ./Validation/AI챗봇_라벨)
    반환값 : dict {'폴더명1':[파일경로1, 파일경로2...], '폴더명2':[파일경로2-1,...]}
    '''   
    path_collection = defaultdict(list)
    for path_of_folder in tqdm(Path(path).iterdir(), desc='Collecting path'):
        path_of_folder = path_of_folder.__str__()
        for path_of_file in Path(path_of_folder).iterdir():
            path_of_file = path_of_file.__str__()
            path_collection[path_of_folder].append(path_of_file)
    '''
    원할 경우 json 파일로 저장해서 확인 가능합니다.
    '''
    # save_path = './text_data'
    # with open(f"{save_path}/path_collection.json", "w", encoding='utf-8') as outfile:
    #     json.dump(path_collection, outfile, indent = 4, ensure_ascii=False)
    
    return path_collection



def extract_sentence_from_data(path_collection: 'dict[str:list]') -> 'dict[str:dict]':
    '''
    입력값: dict / 예시) {'폴더명1':[파일경로1, 파일경로2...], '폴더명2':[파일경로2-1,...]}
    반환값: dict / 예시) key=폴더명, value= {파일명1:문장1, 파일명2:문장2...}
    저장파일: json / 반환값을 json으로 저장. 
    
    '''    
    before_g2p_sentences = defaultdict(dict)
    for path_of_folder, file_path_collection in tqdm(path_collection.items(), desc='collecting sentences'):
        for file_path in file_path_collection:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_data = json.load(f)
                sentence = file_data['발화정보']['stt']
                file_name_for_audio = file_path.replace('AI챗봇_라벨', 'AI챗봇_원천')
                path_of_folder_for_audio = path_of_folder.replace('AI챗봇_라벨', 'AI챗봇_원천')
                
                before_g2p_sentences[path_of_folder_for_audio][file_name_for_audio] = sentence
    save_path = './text_data'
    with open(f"{save_path}/before_g2p_sentences.json", "w", encoding='utf-8') as outfile:
        json.dump(before_g2p_sentences, outfile, indent = 4, ensure_ascii=False)
    
    return before_g2p_sentences


def g2p_processing(before_g2p_sentences: 'dict[str:dict]', descriptive: bool =True, group_vowels: bool =True) -> None:
    
    '''
    입력값: dict / 예시) key=폴더명, value= {파일명1:문장1, 파일명2:문장2...}
    반환값: None
    저장 파일: json / 예시) key=폴더명, value= {파일명1:g2p 처리 문장1, 파일명2:g2p 처리 문장2...}
    
    파라미터 번경으로 여러 G2P기능 활용 가능
    descriptive - 
    예시) False 일 때: 계산이 -> 계사니 
          True 일 때: 계산이 -> 게사니 
    group_vowels
    예시) False 일 때: 얘기 -> 얘기 
          True 일 때: 얘기 -> 예기 
    '''
    g2p = G2p()
    after_g2p_sentences = defaultdict(dict)
    for folder_name, file_sentence_pairs in tqdm(before_g2p_sentences.items(), desc='g2p'):
        for file_name, sentence in tqdm(file_sentence_pairs.items(), desc='converting sents', ):
            g2p_processed_sentence = g2p(sentence, descriptive=descriptive, group_vowels=group_vowels)
            after_g2p_sentences[folder_name][file_name] = g2p_processed_sentence
    save_path = './text_data'
    with open(f"{save_path}/after_g2p_sentences.json", "w", encoding='utf-8') as outfile:
        json.dump(after_g2p_sentences, outfile, indent = 4, ensure_ascii=False)
        
        
if __name__ == "__main__":
    # 본인이 AI허브에서 Validation을 다운받아 압축해제 후 서버에 넣으시면 됩니다.
    current_path = os.getcwd()
    data_path = current_path + '/AI_HUB/Validation/AI챗봇_라벨'
    
    os.makedirs("text_data", exist_ok=True)
    path_collection = make_path_collection(data_path)
    before_g2p_sentences = extract_sentence_from_data(path_collection)
    g2p_processing(before_g2p_sentences)