from datasets import load_dataset
from transformers import WhisperForConditionalGeneration, WhisperProcessor
import torch
from evaluate import load
import re
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor, AutoFeatureExtractor, AutoTokenizer, AutoConfig
import soundfile as sf
import torch
import pandas as pd
from tqdm.auto import tqdm
from sklearn.model_selection import train_test_split
import nlptutti as metrics

def compute_metrics(pred: list, answer: list) -> 'dict':
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
  processor = WhisperProcessor.from_pretrained(model_checkpoint,tokenizer=tokenizer)
  model = WhisperForConditionalGeneration.from_pretrained(model_checkpoint).to("cuda")

  return model, processor

def inference(file_path, model_checkpoint, processor=None):
  if processor:
    model = model_checkpoint
    processor = processor
  else:
    model, processor = load_model(model_checkpoint)

  speech, _ = sf.read(file_path)

  input_features = processor(speech, sampling_rate = 16000,return_tensors="pt").input_features
  
  with torch.no_grad():
    predicted_ids = model.generate(input_features.to("cuda"))[0]
  transcription = processor.decode(predicted_ids)
  result = transcription.replace("[NO]", "")
  result = result.replace("[SN]", "")
  pattern = r'<.*?>'
  result = re.sub(pattern, '', result)

  #print(result)
  return result


def infer_output_with_metric(data, path, model):
  data = pd.read_csv(data)
  _, data = train_test_split(data, test_size=0.2, shuffle=False, random_state=42)
  file_path = data['path'].to_list()
  for i in range(len(file_path)):
    file_path[i] = path + file_path[i]
  answer = data['origin'].to_list()

  model, processor = load_model(model)
  
  output = []
  for audio in tqdm(file_path):
    output.append(inference(audio, model, processor))

  print(output)
  try:
    print(compute_metrics(output, answer))
  except:
    pass

  output = pd.DataFrame({'text':output, 'answer': answer})
  output.to_csv("output.csv", index=False)
  print("SUCCESSFULLY SAVED!")


if __name__ == "__main__":
  infer_output_with_metric("../foreign_audio.csv", "../", "seastar105/whisper-medium-ko-zeroth")#seastar105/whisper-medium-ko-zeroth , openai/whisper-large