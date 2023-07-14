from g2pk import G2p
from collections import defaultdict
import json
from pathlib import Path
import os



def make_path_collection(path: str) -> dict[str:list]:
    '''
    입력값 : string (예시 - ./Validation/AI챗봇_라벨)
    반환값 : dict {'폴더명1':[파일경로1, 파일경로2...], '폴더명2':[파일경로2-1,...]}
    '''   
    path_collection = defaultdict(list)
    for path_of_folder in Path(path).iterdir():
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



def extract_sentence_from_data(path_collection: dict[str:list]) -> dict[str:dict]:
    '''
    입력값: dict / 예시) {'폴더명1':[파일경로1, 파일경로2...], '폴더명2':[파일경로2-1,...]}
    반환값: dict / 예시) key=폴더명, value= {파일명1:문장1, 파일명2:문장2...}
    저장파일: json / 반환값을 json으로 저장. 
    
    '''    
    before_g2p_sentences = defaultdict(dict)
    for path_of_folder, file_path_collection in path_collection.items():
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
