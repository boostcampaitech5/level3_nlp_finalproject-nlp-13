from transformers import AutoFeatureExtractor, AutoTokenizer, Wav2Vec2CTCTokenizer, Wav2Vec2Processor, Wav2Vec2ForCTC, TrainingArguments, Trainer
import numpy as np
from train.datacollator import DataCollatorCTCWithPadding
from dataset import get_dataset
import nlptutti as metrics
import torch
import os
import json
from torch.nn.modules.linear import Linear
import wandb

user = 'PJY'
model_name = "krensik_noinit"
num = "3"
data = f"data/label{num}.json"
name = f"{user}_{num}_{model_name}"
wandb.init(project="huggingface", name=name)

# 나눠서 모델을 fine-tuning할 때에는 아래 코드로 save_model에 저장된 걸 불러옴
model_checkpoint = "./save_model/PJY_2_krensik_noinit"
model_dir = f'./save_model/{name}/'

# vocab adaptation 한 걸로 학습시키려면 tokenizer를 아래 코드로 사용하세요
# tokenizer = Wav2Vec2CTCTokenizer("vocab.json", unk_token="[UNK]", pad_token="[PAD]", word_delimiter_token="|")
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint, unk_token="[UNK]", pad_token="[PAD]", word_delimiter_token="|")
feature_extractor = AutoFeatureExtractor.from_pretrained(model_checkpoint)
processor = Wav2Vec2Processor(feature_extractor=feature_extractor, tokenizer=tokenizer)
vocab_size = len(processor.tokenizer)

train_dataset, test_dataset = get_dataset(processor, data)

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

model =  Wav2Vec2ForCTC.from_pretrained(model_checkpoint)
'''model.config.vocab_size = vocab_size
model.config.pad_token_id = processor.tokenizer.pad_token_id
model.lm_head = Linear(in_features=1024, out_features=vocab_size, bias=True)'''

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

if hasattr(model, "freeze_feature_extractor"):
  model.freeze_feature_extractor()

if hasattr(model, "gradient_checkpointing_enable"):
  model.gradient_checkpointing_enable()

training_args = TrainingArguments(
  output_dir=model_dir,
  group_by_length=True,
  per_device_train_batch_size=16,
  gradient_accumulation_steps=2,
  evaluation_strategy="epoch",
  logging_strategy='epoch',
  save_strategy='epoch',
  num_train_epochs=30,
  gradient_checkpointing=True,
  fp16=True,
  learning_rate=3e-4,
  warmup_steps=500,
  save_total_limit=1,
  push_to_hub=False,
  dataloader_pin_memory=False
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

trainer.save_model(model_dir)
tokenizer.save_pretrained(model_dir)