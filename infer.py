from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor, AutoFeatureExtractor, AutoTokenizer, AutoConfig
import soundfile as sf
import torch
import pandas as pd
from tqdm.auto import tqdm


def infer(data, model, answer=False):
  data = pd.read_csv(data)
  file_path = data['path'][6000:6050]
  # .str.replace("원천", "data/원천")
  # answer = data['sentence'][:20]

  model_checkpoint = model

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
  # print(model)

  output = []

  for file in tqdm(file_path):
    speech, _ = sf.read(file)

    inputs = processor(speech, sampling_rate = 16000, padding=True, return_tensors="pt")
    input_values = inputs.input_values

    with torch.no_grad():
      logits =  model(input_values).logits
          
    predicted_ids = torch.argmax(logits, dim = -1)
    transcription = processor.batch_decode(predicted_ids)
    output.append(transcription[0])

  print(output)

  # output = pd.DataFrame({'text':output})
  output = pd.DataFrame({'text':output, 'answer': file_path})
  output.to_csv("output.csv", index=False)


if __name__ == "__main__":
  # file_info = ["오디오 경로 정보 파일", "모델 경로"]
  infer("data/tts_path.csv", "./save_model/PJY_4_kresnik/wav2vec2-large-xlsr-korean")