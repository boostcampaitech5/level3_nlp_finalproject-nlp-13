from transformers import AutoConfig, AutoTokenizer, AutoFeatureExtractor, Wav2Vec2CTCTokenizer, Wav2Vec2Processor, AutoModelForCTC, TrainingArguments, Trainer
import numpy as np
from datacollator import DataCollatorCTCWithPadding
from dataset import get_dataset
import nlptutti as metrics

model_checkpoint = "kresnik/wav2vec2-large-xlsr-korean" 

# 나눠서 모델을 fine-tuning할 때에는 아래 코드로 save_model에 저장된 걸 불러옴
# model_checkpoint = "./save_model/"

config = AutoConfig.from_pretrained(model_checkpoint)

tokenizer_type = config.model_type if config.tokenizer_class is None else None
config = config if config.tokenizer_class is not None else None

#vocab adaptation 한 걸로 학습시키려면 tokenizer를 아래 코드로 사용하세요
#tokenizer = Wav2Vec2CTCTokenizer("vocab.json", unk_token="[UNK]", pad_token="[PAD]", word_delimiter_token="|")

tokenizer = AutoTokenizer.from_pretrained(
  model_checkpoint, #"./"
  config=config,
  tokenizer_type=tokenizer_type,
  unk_token="[UNK]",
  pad_token="[PAD]",
  word_delimiter_token="|",
)

feature_extractor = AutoFeatureExtractor.from_pretrained(model_checkpoint)

processor = Wav2Vec2Processor(feature_extractor=feature_extractor, tokenizer=tokenizer)

train_dataset, test_dataset = get_dataset(processor)

data_collator = DataCollatorCTCWithPadding(processor=processor, padding=True)

def compute_metrics(pred):
    wer_metric = 0
    cer_metric = 0
    pred_logits = pred.predictions
    pred_ids = np.argmax(pred_logits, axis=-1)

    pred.label_ids[pred.label_ids == -100] = processor.tokenizer.pad_token_id

    pred_str = processor.batch_decode(pred_ids)
    # we do not want to group tokens when computing the metrics
    label_str = processor.batch_decode(pred.label_ids, group_tokens=False)
    print(pred_str, label_str)
    
    for i in range(len(pred_str)):
        preds = pred_str[i].replace(" ", "")
        labels = label_str[i].replace(" ", "")
        wer = metrics.get_wer(pred_str[i], label_str[i])['wer']
        cer = metrics.get_cer(preds, labels)['cer']
        wer_metric += wer
        cer_metric += cer
        
    wer_metric = wer_metric/len(pred_str)
    cer_metric = cer_metric/len(pred_str)
    
    return {"wer": wer_metric, "cer": cer_metric}

from transformers import Wav2Vec2ForCTC

model =  Wav2Vec2ForCTC.from_pretrained(model_checkpoint)

if hasattr(model, "freeze_feature_extractor"):
  model.freeze_feature_extractor()

training_args = TrainingArguments(
  './',
  group_by_length=True,
  per_device_train_batch_size=16,
  gradient_accumulation_steps=2,
  evaluation_strategy="steps",
  num_train_epochs=30,
  gradient_checkpointing=True,
  fp16=True,
  save_steps=400,
  eval_steps=400,
  logging_steps=400,
  learning_rate=3e-4,
  warmup_steps=500,
  save_total_limit=2,
  push_to_hub=False,
)

trainer = Trainer(
    model=model,
    data_collator=data_collator,
    args=training_args,
    compute_metrics=compute_metrics,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    tokenizer=processor.feature_extractor,
)

trainer.train()

trainer.evaluate()

model_dir = './save_model'
trainer.save_model(model_dir)
tokenizer.save_pretrained(model_dir)