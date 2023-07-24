from datasets import Audio, Dataset
from sklearn.model_selection import train_test_split
import json
import pandas as pd

def get_dataset(processor, data):
    if "csv" in data:
        f = pd.read_csv(data)
        
        train, test = train_test_split(f, test_size=0.2, shuffle=False, random_state=42)
        
        audio_dataset = Dataset.from_pandas(train).remove_columns(['__index_level_0__'])
        audio_dataset_test = Dataset.from_pandas(test).remove_columns(['__index_level_0__'])

    if "json" in data:
        with open(data, 'r', encoding='utf-8') as f:
            f = json.load(f)

        dataset = Dataset.from_dict({'audio': f['audio'], 'sentence': f['sentence']}).train_test_split(test_size=0.2, shuffle=False, seed=42)
        audio_dataset = dataset['train']
        audio_dataset_test = dataset['test']


    dataset_train = audio_dataset.cast_column("audio", Audio(sampling_rate=16000))
    dataset_test = audio_dataset_test.cast_column("audio", Audio(sampling_rate=16000))

    print(dataset)
    
    def prepare_dataset(batch):
        audio = batch["audio"]

        # batched output is "un-batched"
        batch["input_values"] = processor(audio["array"], sampling_rate=audio["sampling_rate"]).input_values[0]
        batch["input_length"] = len(batch["input_values"])
        
        with processor.as_target_processor():
            try:
                batch["labels"] = processor(batch["sentence"]).input_ids
            except:
                print(batch["sentence"])
        return batch

    dataset_train = dataset_train.map(prepare_dataset, remove_columns = dataset_train.column_names)
    dataset_test = dataset_test.map(prepare_dataset, remove_columns = dataset_test.column_names)
    
    # 5초 이상인 오디오는 삭제
    # max_input_length_in_sec = 5.0
    # common_voice_train = common_voice_train.filter(lambda x: x < max_input_length_in_sec * processor.feature_extractor.sampling_rate, input_columns=["input_length"])
   
    return dataset_train, dataset_test