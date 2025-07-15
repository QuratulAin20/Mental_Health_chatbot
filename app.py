from flask import Flask, render_template, request, session, send_from_directory
import uuid
import os
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
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Directory to save audio files
AUDIO_DIR = 'static/audio'
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

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
    # Initialize session variables if they don't exist
    if 'conversation_history' not in session:
        session['conversation_history'] = []
    return render_template('index.html', privacy_policy=get_privacy_policy(), history=session['conversation_history'])

@app.route('/process', methods=['POST'])
def process():
    session_id = str(uuid.uuid4())
    audio_path = voice_input.record_voice("user_input.wav")  # Record audio
    transcript = transcriber.transcribe_audio(audio_path)

    emotion_result = emotion_intent.detect_emotion_and_intent(transcript)
    safety_flags = {"suicidal": safety.detect_risk(transcript)}

    if safety_flags.get("suicidal"):
        return "🚨 Suicidal intent detected! Escalation required."

    intent_result = intent_classifier.predict(transcript)
    prompt = prompt_builder.build_prompt(transcript, emotion_result, intent_result)

    # Update conversation history
    session['conversation_history'].append({"role": "user", "content": transcript})

    conversation_history = session['conversation_history'] + [{"role": "system", "content": prompt}]
    response_text, model_used, latency = response_generator.generate_culturally_adapted_response(conversation_history)

    # Save the response in the conversation history
    session['conversation_history'].append({"role": "system", "content": response_text})

    memory.remember_interaction(session_id, emotion_result.get('emotion'), prompt, response_text)

    voice_tone = emotion_result.get("voice_tone", "neutral")
    tts_filename = f"{session_id}.mp3"
    tts_path = os.path.join(AUDIO_DIR, tts_filename)
    tts_engine.speak_arabic_emotional(response_text, tone=voice_tone, output_path=tts_path)

    return render_template('index.html', response=response_text, latency=latency, model=model_used, audio_file=tts_filename, history=session['conversation_history'])

@app.route('/reset', methods=['POST'])
def reset():
    session.pop('conversation_history', None)  # Clear the conversation history
    return redirect(url_for('index'))

@app.route('/audio/<path:filename>')
def audio(filename):
    return send_from_directory(AUDIO_DIR, filename, mimetype='audio/mpeg')

if __name__ == "__main__":
    app.run(debug=True)
