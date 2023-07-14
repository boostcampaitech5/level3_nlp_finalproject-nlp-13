from datasets import load_dataset, Audio, Dataset

def get_dataset(processor):
    
    audio_dataset = Dataset.from_dict({"audio": ['/opt/ml/level3_nlp_finalproject-nlp-13/audio/1.wav', '/opt/ml/level3_nlp_finalproject-nlp-13/audio/2.wav'], "sentence" : ['요즘은 무선 청소기 안 쓰는 사람이 없더라', '현대인의 필수품이 됐구나']})
    audio_dataset_test = Dataset.from_dict({"audio": ['/opt/ml/level3_nlp_finalproject-nlp-13/audio/1.wav', '/opt/ml/level3_nlp_finalproject-nlp-13/audio/3.wav'], "sentence": ['요즘은 무선 청소기 안 쓰는 사람이 없더라', '정말 나만 모른거야']})

    dataset = audio_dataset.cast_column("audio", Audio(sampling_rate=16000))
    dataset_test = audio_dataset_test.cast_column("audio", Audio(sampling_rate=16000))
    
    def prepare_dataset(batch):
        audio = batch["audio"]

        # batched output is "un-batched"
        batch["input_values"] = processor(audio["array"], sampling_rate=audio["sampling_rate"]).input_values[0]
        batch["input_length"] = len(batch["input_values"])
        
        with processor.as_target_processor():
            batch["labels"] = processor(batch["sentence"]).input_ids
        return batch

    dataset = dataset.map(prepare_dataset, remove_columns = dataset.column_names)
    dataset_test = dataset_test.map(prepare_dataset, remove_columns = dataset_test.column_names)
    
    # 5초 이상인 오디오는 삭제
    # max_input_length_in_sec = 5.0
    # common_voice_train = common_voice_train.filter(lambda x: x < max_input_length_in_sec * processor.feature_extractor.sampling_rate, input_columns=["input_length"])

    return dataset, dataset_test