import streamlit as st
from tts_naver_clova import *
from naver_cloud_key import *
from audiorecorder import audiorecorder
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
#from streamlit_extras.switch_page_button import switch_page

st.markdown("<h1 style='text-align: center; color: black;'>HYPE연어</h1>", unsafe_allow_html=True)

col1, col2, col3 , col4, col5 = st.columns(5)

with col1:
    pass
with col2:
    pass
with col4:
    pass
with col5:
    pass
with col3 :
    want_to_contribute = st.markdown("""
    <style>                 
    div.stButton > button:first-child {
        background-color: #FBEEAC;
        border:none;
    }
    </style>""", unsafe_allow_html=True)
    want_to_contribute = st.button("START")

if want_to_contribute:
    st.markdown("<h1 style='text-align: center; color: black;'>다음 문장을 듣고 따라해보세요</h1>", unsafe_allow_html=True)
    sen='오늘은 날씨가 맑다.'
    st.write(sen)
    #get_sound(sen)
    path = './tts_test.mp3'   
    audio_file = open(path, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg')
    #st.button('🎧',on_click=get_sound(sen))
    
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
        