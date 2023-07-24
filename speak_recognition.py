import streamlit as st
from audiorecorder import audiorecorder
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import librosa

st.title("Audio Recorder")
audio = audiorecorder("Click to record", "Recording...")

processor = AutoProcessor.from_pretrained("openai/whisper-medium", language="ko", task="transcribe")
model = AutoModelForSpeechSeq2Seq.from_pretrained("spow12/whisper-medium-ksponspeech")

# To play audio in frontend:
if len(audio) > 0:
    st.audio(audio.tobytes())

#To save audio to a file:
if st.button('save'):
    wav_file = open("./audio.mp3", "wb")
    wav_file.write(audio.tobytes())

# To print texts by stt model
if st.button('print'):
    speech_array, _ = librosa.load("./audio.mp3", sr=16000)
    inputs = processor(speech_array, return_tensors="pt")
    input_features = inputs.input_features
    print(input_features)
    generated_ids = model.generate(inputs=input_features)
    transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    st.write(transcription)