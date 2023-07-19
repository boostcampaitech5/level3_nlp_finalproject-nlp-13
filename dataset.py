from datasets import load_dataset, Audio, Dataset
from sklearn.model_selection import train_test_split
import json
import re

def get_dataset(processor):

    def remove_special_characters(batch):
        batch["sentence"] = re.sub(r'\([^)]*\)', lambda x: re.sub(r'[^가-힣\s]', '', x.group()), batch["sentence"]).rstrip() + " "
        return batch

    def load_json_file(file_path):
        with open(file_path, "r", encoding='utf-8') as file:
            data = json.load(file)
        return data

    json_file_path = "./transfer_file1.json"

    dict_dataset = load_json_file(json_file_path)
    #print(dict_dataset)
    split_idx = int(len(dict_dataset["audio"]) * 0.8)
    dict_dataset_train = {
        "audio": dict_dataset["audio"][:split_idx],
        "sentence": dict_dataset["sentence"][:split_idx]
    }
    dict_dataset_test = {
        "audio": dict_dataset["audio"][split_idx:],
        "sentence": dict_dataset["sentence"][split_idx:]
    }
    
    audio_dataset_train = Dataset.from_dict(dict_dataset_train)
    audio_dataset_test = Dataset.from_dict(dict_dataset_test)
    # audio_dataset = Dataset.from_dict({"audio": ['/opt/ml/level3_nlp_finalproject-nlp-13/audio/1.wav', '/opt/ml/level3_nlp_finalproject-nlp-13/audio/2.wav'], "sentence" : ['요즘은 무선 청소기 안 쓰는 사람이 없더라', '현대인의 필수품이 됐구나']})
    # audio_dataset_test = Dataset.from_dict({"audio": ['/opt/ml/level3_nlp_finalproject-nlp-13/audio/1.wav', '/opt/ml/level3_nlp_finalproject-nlp-13/audio/3.wav'], "sentence": ['요즘은 무선 청소기 안 쓰는 사람이 없더라', '정말 나만 모른거야']})

    audio_dataset_train = audio_dataset_train.map(remove_special_characters)
    audio_dataset_test = audio_dataset_test.map(remove_special_characters)
    
    dataset_train = audio_dataset_train.cast_column("audio", Audio(sampling_rate=16000))
    dataset_test = audio_dataset_test.cast_column("audio", Audio(sampling_rate=16000))
    
    def prepare_dataset(batch):
        audio = batch["audio"]

        # batched output is "un-batched"
        batch["input_values"] = processor(audio["array"], sampling_rate=audio["sampling_rate"]).input_values[0]
        batch["input_length"] = len(batch["input_values"])
        
        with processor.as_target_processor():
            batch["labels"] = processor(batch["sentence"]).input_ids
        return batch

    dataset_train = dataset_train.map(prepare_dataset, remove_columns = dataset_train.column_names)
    dataset_test = dataset_test.map(prepare_dataset, remove_columns = dataset_test.column_names)
    
    # 5초 이상인 오디오는 삭제
    # max_input_length_in_sec = 5.0
    # common_voice_train = common_voice_train.filter(lambda x: x < max_input_length_in_sec * processor.feature_extractor.sampling_rate, input_columns=["input_length"])
   
    return dataset_train, dataset_test