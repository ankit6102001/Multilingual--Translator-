import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

from .services.translation import translate_text, detect_language
from .services.audio_service import text_to_speech, speech_to_text

app = FastAPI(title="Multilingual Translator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)
    source_lang: Optional[str] = None
    target_lang: Optional[str] = None

class AudioTranscriptionRequest(BaseModel):
    audio_data: str

@app.post("/translate")
async def translate(request: TranslationRequest):
    try:
        source_lang = request.source_lang or detect_language(request.text)
        target_lang = request.target_lang or 'english'
        
        translated_text = translate_text(
            request.text, 
            source_lang, 
            target_lang
        )
        
        return {
            "original_text": request.text,
            "original_language": source_lang,
            "translated_text": translated_text,
            "target_language": target_lang
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/transcribe")
async def transcribe_audio(request: AudioTranscriptionRequest):
    try:
        transcribed_text = speech_to_text(request.audio_data)
        
        detected_lang = detect_language(transcribed_text)
        
        return {
            "transcribed_text": transcribed_text,
            "detected_language": detected_lang
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/text-to-speech")
async def generate_speech(request: TranslationRequest):
    try:
        audio_data = text_to_speech(
            request.text, 
            language=request.target_lang or request.source_lang
        )
        
        return {"audio_data": audio_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)