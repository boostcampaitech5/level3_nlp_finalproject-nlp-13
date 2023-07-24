from transformers import AutoFeatureExtractor, Wav2Vec2CTCTokenizer, Wav2Vec2Processor, Wav2Vec2ForCTC, TrainingArguments, Trainer

## repo
MODEL_SAVE_HUB_PATH = 'wav2vec2-large-xlsr-korean-4' # ex) 'my-bert-fine-tuned'
HUGGINGFACE_AUTH_TOKEN = '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' # https://huggingface.co/settings/token
model_checkpoint = "./save_model/PJY_4_kresnik/wav2vec2-large-xlsr-korean"
model =  Wav2Vec2ForCTC.from_pretrained(model_checkpoint)
## Push to huggingface-hub
model.push_to_hub(
			MODEL_SAVE_HUB_PATH, 
			use_temp_dir=True, 
			use_auth_token=HUGGINGFACE_AUTH_TOKEN
)
