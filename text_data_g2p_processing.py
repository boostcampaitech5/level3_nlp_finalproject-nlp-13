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

