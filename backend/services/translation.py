import google.generativeai as genai

def translate_text(text, source_lang=None, target_lang=None):
    """Direct translation using Gemini AI"""
    try:
        api_key = 'GEMINI_API_KEY'
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')

        prompt = f"""
        Translate the word or text '{text}' to {target_lang or 'the target language'}.
        Translate precisely. Provide ONLY the translated text.
        If translating to Hindi, use Devanagari script.
        """
        response = model.generate_content(prompt)
        translated = response.text.strip()
        return translated if translated else text
    
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def detect_language(text: str) -> str:
    """Detect language using Gemini AI"""
    try:
        api_key = 'GEMINI_API_KEY'
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')

        prompt = f"""
        Detect the language of this text precisely:
        '{text}'
        
        Return ONLY the language name in lowercase.
        If unsure, return 'english'.
        """
        
        response = model.generate_content(prompt)
        
        detected_lang = response.text.strip().lower()
        
        return detected_lang if detected_lang else 'english'
    
    except Exception as e:
        print(f"Language detection error: {e}")
        return 'english'