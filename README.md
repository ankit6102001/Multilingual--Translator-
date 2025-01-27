Multilingual Translation Application
A real-time translation application with speech recognition capabilities, built using Streamlit for the frontend and FastAPI for the backend. The application supports text translation and speech-to-text functionality across multiple languages.

Features

Text translation between multiple languages
Automatic language detection
Speech recognition and transcription
Real-time audio recording
Clean and intuitive user interface



Installation

Clone the repository:

git clone https://github.com/yourusername/multilingual-translator.git
cd multilingual-translator

Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

Install required packages:

pip install -r requirements.txt    

Set Gemini API key

Run Backend: uvicorn backend.main:app --reload
Run Frontend: streamlit run frontend/app.py







Contributing

Fork the repository
Create a feature branch
Commit your changes
Push to the branch
Create a Pull Request
