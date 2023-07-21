from datasets import load_dataset, Audio, Dataset
from sklearn.model_selection import train_test_split
import json
import torch

def get_dataset(processor, data):
    with open(data, "r", encoding="utf8") as f:
        f = json.load(f)
    
    trainx, testx, trainy, testy = train_test_split(f['audio'], f['sentence'], test_size=0.1, shuffle=False, random_state=42)
    
    audio_dataset = Dataset.from_dict({"audio": trainx, "sentence" : trainy})
    audio_dataset_test = Dataset.from_dict({"audio": testx, "sentence": testy})

    dataset = audio_dataset.cast_column("audio", Audio(sampling_rate=16000))
    dataset_test = audio_dataset_test.cast_column("audio", Audio(sampling_rate=16000))
    
    def prepare_dataset(batch):
        audio = batch["audio"]

        # batched output is "un-batched"
        batch["input_values"] = processor(audio["array"], sampling_rate=audio["sampling_rate"]).input_values[0]
        #batch["input_length"] = len(batch["input_values"])
        
        with processor.as_target_processor():
            batch["labels"] = processor(batch["sentence"]).input_ids
        return batch

    dataset = dataset.map(prepare_dataset, remove_columns = dataset.column_names)
    dataset_test = dataset_test.map(prepare_dataset, remove_columns = dataset_test.column_names)
    
    # 5초 이상인 오디오는 삭제
    # max_input_length_in_sec = 5.0
    # common_voice_train = common_voice_train.filter(lambda x: x < max_input_length_in_sec * processor.feature_extractor.sampling_rate, input_columns=["input_length"])

    return dataset, dataset_test