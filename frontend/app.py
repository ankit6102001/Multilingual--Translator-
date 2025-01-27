import streamlit as st
import requests
import base64
import io
import sounddevice as sd
import soundfile as sf
import numpy as np

BACKEND_URL = "http://localhost:8000"

def record_audio(duration=5, sample_rate=44100):
    """Record audio from microphone"""
    st.write(f"Recording audio for {duration} seconds...")
    recording = sd.rec(int(duration * sample_rate), 
                       samplerate=sample_rate, 
                       channels=1)
    sd.wait()
    
    audio_fp = io.BytesIO()
    sf.write(audio_fp, recording, sample_rate, format='wav')
    audio_fp.seek(0)
    return base64.b64encode(audio_fp.read()).decode('utf-8')

def translate_text(input_text, source_lang=None, target_lang=None):
    try:
        response = requests.post(f"{BACKEND_URL}/translate", json={
            "text": input_text,
            "source_lang": source_lang or None,
            "target_lang": target_lang or None
        })
        
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        st.error(f"Translation request failed: {e}")
        return None

def main():
    st.title("🌐 Multilingual Translator")
    
    st.header("Text Translation")
    input_text = st.text_area("Enter text to translate")
    
    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.text_input("Source Language (optional)", placeholder="Auto-detect")
    with col2:
        target_lang = st.text_input("Target Language", placeholder="English")
    
    if st.button("Translate"):
        if not input_text:
            st.warning("Please enter text to translate")
            return
        
        result = translate_text(input_text, source_lang, target_lang)
        
        if result:
            st.success(f"Translated Text: {result.get('translated_text', 'No translation')}")
            st.info(f"Detected Language: {result.get('original_language', 'Unknown')}")
            
            if st.button("Listen to Translation"):
                try:
                    speech_response = requests.post(f"{BACKEND_URL}/text-to-speech", json={
                        "text": result['translated_text'],
                        "target_lang": target_lang
                    })
                    speech_response.raise_for_status()
                    audio_data = speech_response.json()['audio_data']
                    
                    st.audio(base64.b64decode(audio_data), format='audio/mp3')
                except Exception as e:
                    st.error(f"Text-to-speech error: {e}")
    
    st.header("Speech Recognition")
    if st.button("Record Audio"):
        try:
            audio_base64 = record_audio()
            
            response = requests.post(f"{BACKEND_URL}/transcribe", json={
                "audio_data": audio_base64
            })
            result = response.json()
            
            st.success(f"Transcribed Text: {result['transcribed_text']}")
            st.info(f"Detected Language: {result['detected_language']}")
        
        except Exception as e:
            st.error(f"Transcription error: {e}")

if __name__ == "__main__":
    main()