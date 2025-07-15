from flask import Flask, render_template, request, session, send_from_directory, redirect, url_for, after_this_request
import uuid
import os
import time
from threading import Thread
from modules import (
    voice_input,
    transcriber,
    emotion_intent,
    intent_classifier,
    safety,
    prompt_builder,
    response_generator,
    memory,
    tts_engine,
)

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Directory to save audio files
AUDIO_DIR = 'static/audio'
os.makedirs(AUDIO_DIR, exist_ok=True)

def get_privacy_policy():
    return """
    Your privacy is important to us. This policy explains how we collect, use, and protect your data:
    
    1. **Data Collection**: We collect information you provide directly to us, including voice input and related data.
    2. **Data Usage**: We use your information to provide responses and improve our services.
    3. **Data Security**: We implement appropriate security measures to protect your data.
    4. **User Rights**: You have the right to access and request corrections to your data.
    """

@app.route('/')
def index():
    if 'conversation_history' not in session:
        session['conversation_history'] = []
    return render_template('index.html', privacy_policy=get_privacy_policy(), history=session['conversation_history'])

@app.route('/process', methods=['POST'])
def process():
    session_id = str(uuid.uuid4())
    start_time = time.time()

    # Step 1: Record and transcribe audio
    audio_path = voice_input.record_voice("user_input.wav")  # 10–15s, 16kHz, mono
    transcript = transcriber.transcribe_audio(audio_path)

    # Step 2: Detect emotion and intent in parallel
    results = {}

    def run_emotion():
        results['emotion_result'] = emotion_intent.detect_emotion_and_intent(transcript)

    def run_intent():
        results['intent_result'] = intent_classifier.predict(transcript)

    t1, t2 = Thread(target=run_emotion), Thread(target=run_intent)
    t1.start(); t2.start(); t1.join(); t2.join()

    emotion_result = results['emotion_result']
    intent_result = results['intent_result']

    # Step 3: Safety check
    if safety.detect_risk(transcript):
        return "🚨 Suicidal intent detected! Escalation required."

    # Step 4: Prompt building and history
    prompt = prompt_builder.build_prompt(transcript, emotion_result, intent_result)
    session['conversation_history'].append({"role": "user", "content": transcript})
    
    recent_history = session['conversation_history'][-6:]
    conversation_history = recent_history + [{"role": "system", "content": prompt}]

    # Step 5: Generate LLM response
    response_text, model_used, model_latency = response_generator.generate_culturally_adapted_response(conversation_history)
    session['conversation_history'].append({"role": "system", "content": response_text})

    # Step 6: Text-to-Speech with caching
    voice_tone = emotion_result.get("voice_tone", "neutral")
    tts_filename = f"{session_id}.mp3"
    tts_path = os.path.join(AUDIO_DIR, tts_filename)

    if not os.path.exists(tts_path):
        tts_engine.speak_arabic_emotional(response_text, tone=voice_tone, output_path=tts_path)

    # Step 7: Log to memory DB after sending response
    @after_this_request
    def log_after_response(response):
        memory.remember_interaction(session_id, emotion_result.get('emotion'), prompt, response_text,
                                    transcript=transcript,
                                    input_audio_path=audio_path,
                                    output_audio_path=tts_path,
                                    intent=intent_result,
                                    model=model_used,
                                    latency=round(time.time() - start_time, 2))
        return response

    total_latency = round(time.time() - start_time, 2)

    return render_template('index.html',
                           response=response_text,
                           latency=total_latency,
                           model=model_used,
                           audio_file=tts_filename,
                           history=session['conversation_history'])

@app.route('/reset', methods=['POST'])
def reset():
    session.pop('conversation_history', None)
    return redirect(url_for('index'))

@app.route('/audio/<path:filename>')
def audio(filename):
    return send_from_directory(AUDIO_DIR, filename, mimetype='audio/mpeg')

if __name__ == "__main__":
    app.run(debug=True)
