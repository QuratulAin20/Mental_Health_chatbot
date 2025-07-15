import streamlit as st
import uuid
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

# Function to display the privacy policy
def display_privacy_policy():
    policy = """
    ### Privacy Policy
    Your privacy is important to us. This policy explains how we collect, use, and protect your data:
    
    1. **Data Collection**: We collect information you provide directly to us, including voice input and related data.
    2. **Data Usage**: We use your information to provide responses and improve our services.
    3. **Data Security**: We implement appropriate security measures to protect your data.
    4. **User Rights**: You have the right to access and request corrections to your data.
    
    If you have any questions, please contact us.
    """
    st.markdown(policy)

# Main app logic
st.title("OMANI Mental Health Voice Bot")

# Consent Section
if 'consent' not in st.session_state:
    st.warning("Please read our privacy policy before proceeding.")
    
    # Dropdown for Privacy Policy
    if st.selectbox("Select to view Privacy Policy:", ["Select", "View Privacy Policy"]) == "View Privacy Policy":
        display_privacy_policy()
    
    if st.checkbox("I consent to the processing of my information according to the privacy policy."):
        st.session_state.consent = True
    else:
        st.stop()  # Stop further processing until consent is given

# User Rights Information
st.write("You have the right to access your information and request corrections.")

# Security Measures Notification
st.write("Your information is stored securely and is protected with encryption.")

# Crisis Disclaimer
st.warning("If you are in crisis or need immediate support, please contact a mental health professional or emergency services.")

# Start session
session_id = str(uuid.uuid4())

if st.button("Record Voice Input"):
    audio_path = voice_input.record_voice("user_input.wav")
    st.success("Recording complete!")

    transcript = transcriber.transcribe_audio(audio_path)
    st.write("Transcription:", transcript)

    emotion_result = emotion_intent.detect_emotion_and_intent(transcript)

    safety_flags = {"suicidal": safety.detect_risk(transcript)}
    if safety_flags.get("suicidal"):
        st.error("🚨 Suicidal intent detected! Escalation required.")
        st.stop()

    intent_result = intent_classifier.predict(transcript)
    prompt = prompt_builder.build_prompt(transcript, emotion_result, intent_result)

    conversation_history = [
        {"role": "user", "content": transcript},
        {"role": "system", "content": prompt}
    ]

    response_text, model_used, latency = response_generator.generate_culturally_adapted_response(conversation_history)

    # Display the final response with latency
    final_response = f"🤖 ({model_used}) Response ({latency:.2f}s): {response_text}"
    st.markdown(f"🧠 Final Therapeutic Response: {final_response}")

    memory.remember_interaction(session_id, emotion_result.get('emotion'), prompt, response_text)

    voice_tone = emotion_result.get("voice_tone", "neutral")
    tts_path = tts_engine.speak_arabic_emotional(response_text, tone=voice_tone)

    st.write(f"🔊 Audio response saved at: {tts_path}")

    # Play the audio response
    st.audio(tts_path)
