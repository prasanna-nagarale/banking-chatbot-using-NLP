# app.py
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile
import uuid
from pygame import mixer
import time
import shutil

# Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Initialize pygame mixer
mixer.init()

# Ensure static and templates folders exist
os.makedirs('static', exist_ok=True)
os.makedirs('templates', exist_ok=True)

# Load corpus (keeping existing implementation)
def load_corpus(file_path):
    corpus = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            entries = content.strip().split('\n\n')
            for entry in entries:
                lines = entry.split('\n')
                question = None
                answer = None
                for line in lines:
                    if line.startswith('Q:'):
                        question = line[2:].strip()
                    elif line.startswith('A:'):
                        answer = line[2:].strip()
                if question and answer:
                    corpus.append((question, answer))
    except FileNotFoundError:
        print(f"Warning: Corpus file not found at {file_path}")
        # Add some default responses
        corpus = [
            ("hello", "Hello! How can I help you today?"),
            ("hi", "Hi there! How can I assist you?")
        ]
    return corpus

CORPUS_PATH = 'S:/pro/chatbot.txt'
corpus = load_corpus(CORPUS_PATH)

def get_best_answer(query):
    for question, answer in corpus:
        if query.lower() in question.lower():
            return answer
    return "I'm sorry, I couldn't find an answer to your question."

def greet_with_time(sentence):
    current_hour = datetime.now().hour
    GREET_INPUTS = (
        "hello", "hii", "hey", "hi", "hey there", "hii bot", "what's up",
        "good morning", "good afternoon", "good evening", "howdy"
    )
    
    if 5 <= current_hour < 12:
        time_based_greeting = "Good morning"
    elif 12 <= current_hour < 18:
        time_based_greeting = "Good afternoon"
    elif 18 <= current_hour < 22:
        time_based_greeting = "Good evening"
    else:
        time_based_greeting = "Hello"

    for word in sentence.lower().split():
        if word in GREET_INPUTS:
            return f"{time_based_greeting}! How can I assist you?"
    return None

def translate_text(text, src_lang, dest_lang):
    try:
        return GoogleTranslator(source=src_lang, target=dest_lang).translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def cleanup_old_files():
    """Clean up audio files older than 5 minutes"""
    current_time = time.time()
    static_dir = 'static'
    for file in os.listdir(static_dir):
        if file.startswith('response_') and file.endswith('.mp3'):
            file_path = os.path.join(static_dir, file)
            if current_time - os.path.getctime(file_path) > 300:  # 5 minutes
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error cleaning up {file}: {e}")

def generate_voice_response(text, language):
    try:
        # Clean up old files
        cleanup_old_files()
        
        # Create unique filename
        unique_id = str(uuid.uuid4())
        filename = f"response_{unique_id}.mp3"
        filepath = os.path.join('static', filename)
        
        # Language mapping for gTTS
        language_map = {
            'en': 'en',
            'hi': 'hi',
            'kn': 'kn',
            'te': 'te',
            'ta': 'ta',
            'mr': 'mr'
        }
        
        # Get appropriate language code
        tts_lang = language_map.get(language, 'en')
        
        # Generate audio using gTTS
        tts = gTTS(text=text, lang=tts_lang, slow=False)
        tts.save(filepath)
        
        return filename
        
    except Exception as e:
        print(f"Voice generation error: {e}")
        return None

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_query = data.get('message', '').strip()
        language = data.get('language', 'en')
        mode = data.get('mode', 'T')

        if not user_query:
            return jsonify({"error": "Query cannot be empty"}), 400

        # Get response
        bot_response = greet_with_time(user_query) or get_best_answer(user_query)

        # Translate if needed
        if language != 'en':
            bot_response = translate_text(bot_response, "en", language)

        # Handle text-only mode
        if mode == 'T':
            return jsonify({"response": bot_response})

        # Generate voice response
        audio_filename = generate_voice_response(bot_response, language)
        
        if audio_filename:
            return jsonify({
                "response": bot_response,
                "audio_file": f"/static/{audio_filename}"
            })
        else:
            return jsonify({
                "response": bot_response,
                "error": "Voice generation failed"
            })

    except Exception as e:
        print(f"Chat endpoint error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)