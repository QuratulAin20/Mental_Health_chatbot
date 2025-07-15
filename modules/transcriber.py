import os
import sys
from dotenv import load_dotenv
from groq import Groq
from modules.logger import logging
from modules.exceptions import MentalHealthChatBotException

# Load environment variables
load_dotenv()

# Constants
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
STT_MODEL = "whisper-large-v3"

def transcribe_audio(audio_filepath: str, model: str = STT_MODEL) -> str:
    """
    Transcribe Arabic audio to text using Groq Whisper API.

    Args:
        audio_filepath (str): Path to audio file (WAV/MP3)
        model (str): Whisper model version (default: whisper-large-v3)

    Returns:
        str: Transcribed Arabic text
    """
    try:
        if not GROQ_API_KEY:
            raise EnvironmentError("Missing GROQ_API_KEY in .env")

        if not os.path.exists(audio_filepath):
            raise FileNotFoundError(f"Audio file not found: {audio_filepath}")

        client = Groq(api_key=GROQ_API_KEY)

        with open(audio_filepath, "rb") as audio_file:
            result = client.audio.transcriptions.create(
                model=model,
                file=audio_file,
                language="ar"
            )

        logging.info("Transcription successful.")
        return result.text

    except Exception as e:
        logging.exception(" Error during transcription")
        raise MentalHealthChatBotException(e, sys)


# Optional helper: record and transcribe (used for CLI/testing, not Flask)
def record_and_transcribe() -> str:
    """
    Record speech (via voice_input.py) and return the transcribed Arabic text.

    Returns:
        str: Transcription result
    """
    try:
        from modules.voice_input import record_audio_vad
        audio_file = record_audio_vad()
        return transcribe_audio(audio_file)
    except MentalHealthChatBotException:
        raise
    except Exception as e:
        raise MentalHealthChatBotException(e, sys)
