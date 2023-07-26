from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor, AutoFeatureExtractor, AutoTokenizer, AutoConfig
import soundfile as sf
import torch
import pandas as pd
from tqdm.auto import tqdm
from sklearn.model_selection import train_test_split
import nlptutti as metrics

def compute_metrics(pred: list, answer: list) -> 'dict':
    '''
    입력값 : 예측값과 정답 문자열을 list 형태로 입력
    반환값 : cer 및 wer 을 계산하여 dict 형태로 반환
    '''
    wer_metric = 0
    cer_metric = 0
  
    for i in range(len(pred)):
        preds = pred[i].replace(" ", "")
        answers = answer[i].replace(" ", "")
        wer = metrics.get_wer(pred[i], answer[i])['wer']
        cer = metrics.get_cer(preds, answers)['cer']
        wer_metric += wer
        cer_metric += cer
        
    wer_metric = wer_metric/len(pred)
    cer_metric = cer_metric/len(pred)
    
    return {"wer": wer_metric, "cer": cer_metric}

def load_model(model_checkpoint: str):
  '''
  입력값 : model_checkpoint
  반환값 : model 과 processor
  '''
  config = AutoConfig.from_pretrained(model_checkpoint)

  tokenizer_type = config.model_type if config.tokenizer_class is None else None
  config = config if config.tokenizer_class is not None else None

  tokenizer = AutoTokenizer.from_pretrained(
    model_checkpoint,
    config=config,
    tokenizer_type=tokenizer_type,
    unk_token="[UNK]",
    pad_token="[PAD]",
    word_delimiter_token="|",
  )
  feature_extractor = AutoFeatureExtractor.from_pretrained(model_checkpoint)
  processor = Wav2Vec2Processor(feature_extractor=feature_extractor, tokenizer=tokenizer)

  model = Wav2Vec2ForCTC.from_pretrained(model_checkpoint)

  return model, processor


def inference(file_path, model_checkpoint, processor=None):
  if processor:
    model = model_checkpoint
    processor = processor
  else:
    model, processor = load_model(model_checkpoint)

  speech, _ = sf.read(file_path)

  inputs = processor(speech, sampling_rate = 16000, padding=True, return_tensors="pt")
  input_values = inputs.input_values

  with torch.no_grad():
    logits =  model(input_values).logits
          
  predicted_ids = torch.argmax(logits, dim = -1)
  transcription = processor.batch_decode(predicted_ids)
  result = transcription[0].replace("[NO]", "")
  result = result.replace("[SN]", "")

  return result


def infer_output_with_metric(data, path, model):
  '''
  입력값
    data : 오디오 경로 정보와 정답 레이블이 각각 path, sentence의 column으로 저장되어 있는 csv 파일 경로
    path : data의 path에 해당되는 폴더가 있는 경로

  '''
  data = pd.read_csv(data)
  _, data = train_test_split(data, test_size=0.2, shuffle=False, random_state=42)
  file_path = data['path'].to_list()
  for i in range(len(file_path)):
    file_path[i] = path + file_path[i]
  answer = data['sentence'].to_list()

  model, processor = load_model(model)
  
  output = []
  for audio in tqdm(file_path):
    output.append(inference(audio, model, processor))

  print(output)
  try:
    print(compute_metrics(output, answer))
  except:
    pass

  # output = pd.DataFrame({'text':output})
  output = pd.DataFrame({'text':output, 'answer': answer})
  output.to_csv("output.csv", index=False)
  print("SUCCESSFULLY SAVED!")
  # print(compute_metrics(output, answer))


if __name__ == "__main__":
  # file_info = ["오디오 경로 정보 파일", "원천데이터 폴더 경로", "모델 경로"]
  infer_output_with_metric("data/foreign_audio_shuffled.csv", "data/", "save_model/PJY_4_kresnik")
  # print(inference("data/ncloud_tts_data/jinho/1_가격_jinho.wav", "./save_model/PJY_4_tts_word"))