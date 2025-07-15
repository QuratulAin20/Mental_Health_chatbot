import time
import uuid  # For generating unique session IDs
from modules.exceptions import handle_exceptions
from utils.timers import Timer
from modules.logger import logging
from modules.exceptions import MentalHealthChatBotException
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

@handle_exceptions
def main():
    logging.info("Starting OMANI Mental Health Voice Bot Session")

    # Start latency tracking
    timer = Timer()
    timer.start("total_session")

    # Generate a unique session ID
    session_id = str(uuid.uuid4())  # Create a unique session ID for this interaction

    # Step 1: Record voice input
    audio_path = voice_input.record_voice("user_input.wav")

    # Step 2: Transcribe voice using Groq Whisper
    transcript = transcriber.transcribe_audio(audio_path)

    # Step 3: Analyze emotion & intent
    emotion_result = emotion_intent.detect_emotion_and_intent(transcript)

    # Step 4: Run safety checks (suicidal, harmful, crisis)
    safety_flags = {"suicidal": safety.detect_risk(transcript)}

    if safety_flags.get("suicidal"):
        logging.critical("Suicidal intent detected! Escalation required.")
        print(safety.handle_risk_response("ar"))
        return
    
    # Step 5: Intent classifier
    intent_result = intent_classifier.predict(transcript)
    
    # Step 6: Build culturally informed therapy prompt
    prompt = prompt_builder.build_prompt(transcript, emotion_result, intent_result)
    
    # Step 7: Define conversation history
    conversation_history = [
        {"role": "user", "content": transcript},
        {"role": "system", "content": prompt}
    ]

    # Step 8: Generate response from LLM
    response_text, model_used, latency = response_generator.generate_culturally_adapted_response(conversation_history)
    print(f"\n({model_used}) Response ({latency:.2f}s):\n{response_text}")
    
    # Step 9: Save interaction to memory
    memory.remember_interaction(
        session_id,
        emotion_result.get('emotion'),
        prompt,  # Assuming you want to store the prompt as the Quran verse
        response_text
    )

    # Step 10: Convert text to voice (emotional tone-aware)
    voice_tone = emotion_result.get("voice_tone", "neutral")
    tts_path = tts_engine.speak_arabic_emotional(response_text, tone=voice_tone)

    # Stop the timer and log the total session duration
    timer.stop("total_session")
    print("\n Final Therapeutic Response:")
    print(response_text)
    print(f"\n Audio response saved at: {tts_path}")
    print(f"Total session latency: {timer.get_duration('total_session'):.2f} sec")

if __name__ == "__main__":
    main()