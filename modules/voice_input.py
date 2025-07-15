import os
import sys
import uuid
import speech_recognition as sr
from modules.logger import logging
from modules.exceptions import MentalHealthChatBotException

# Directory to store recorded files
AUDIO_DIR = "static/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)


def record_voice(filename: str = None, timeout: int = 10, phrase_time_limit: int = 20) -> str:
    """
    Records voice input from microphone and saves as a WAV file.

    Args:
        filename (str): Optional custom filename
        timeout (int): Max seconds to wait for speech
        phrase_time_limit (int): Max speech duration in seconds

    Returns:
        str: Path to the saved WAV file
    """
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    if filename is None:
        filename = f"audio_{uuid.uuid4().hex[:8]}.wav"

    audio_path = os.path.join(AUDIO_DIR, filename)

    try:
        with mic as source:
            print("Please start speaking... (Recording)")
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            print("Recording complete.")

            with open(audio_path, "wb") as f:
                f.write(audio_data.get_wav_data())

            logging.info(f"Voice input saved: {audio_path}")
            return audio_path

    except sr.WaitTimeoutError:
        logging.warning("Timeout: No speech detected.")
        raise MentalHealthChatBotException("Voice input timeout", sys)

    except sr.RequestError as e:
        raise MentalHealthChatBotException(f"Speech Recognition service error: {e}", sys)

    except Exception as e:
        raise MentalHealthChatBotException("Unexpected error during voice recording", sys)


