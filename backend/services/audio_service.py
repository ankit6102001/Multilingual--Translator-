import base64
import io
import speech_recognition as sr
from gtts import gTTS

def speech_to_text(audio_base64: str) -> str:
    """Convert base64 audio to text using speech recognition"""
    try:
        audio_data = base64.b64decode(audio_base64)
        
        recognizer = sr.Recognizer()
        
        with io.BytesIO(audio_data) as audio_file:
            with sr.AudioFile(audio_file) as source:
                audio = recognizer.record(source)
                
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError:
            return "Speech recognition service unavailable"
    except Exception as e:
        print(f"Speech to text conversion error: {e}")
        return "Audio processing failed"

def text_to_speech(text: str, language: str = 'en') -> str:
    """Convert text to speech, return base64 encoded audio"""
    try:
        mp3_fp = io.BytesIO()
        tts = gTTS(text=text, lang=language)
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        
        audio_base64 = base64.b64encode(mp3_fp.read()).decode('utf-8')
        return audio_base64
    except Exception as e:
        print(f"Text to speech conversion error: {e}")
        return ""