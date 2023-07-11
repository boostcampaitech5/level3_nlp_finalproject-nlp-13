import streamlit as st
from audiorecorder import audiorecorder
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq

st.title("Audio Recorder")
audio = audiorecorder("Click to record", "Recording...")

processor = AutoProcessor.from_pretrained("byoussef/whisper-large-v2-Ko")
model = AutoModelForSpeechSeq2Seq.from_pretrained("byoussef/whisper-large-v2-Ko")

# To play audio in frontend:
if len(audio) > 0:
    st.audio(audio.tobytes())

#To save audio to a file:
if st.button('save'):
    wav_file = open("./FinalProject/audio.mp3", "wb")
    wav_file.write(audio.tobytes())

# To print texts by stt model
if st.button('print'):
    inputs = processor(audio, return_tensors="pt")
    input_features = inputs.input_features

    generated_ids = model.generate(inputs=input_features)

    transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    st.write(transcription)
    print(transcription)