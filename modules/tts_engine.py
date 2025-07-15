import os
import sys
from dotenv import load_dotenv
from elevenlabs import ElevenLabs
from modules.logger import logging
from modules.exceptions import MentalHealthChatBotException
from modules.dialect_handling import DialectDataProcessor 

# Load environment variables
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
# Constants
CUSTOM_ARABIC_VOICE_ID = "DANw8bnAVbjDEHwZIoYa"  
DEFAULT_OUTPUT_PATH = "static/audio/arabic_emotional_output.mp3"

# Initialize the DialectDataProcessor
data_processor = DialectDataProcessor('C:\\Users\\DELL\\Desktop\\mental_health_bot\\data\\dialect_data.xlsx')  
def speak_arabic_emotional(text: str, tone: str = "neutral", output_path: str = DEFAULT_OUTPUT_PATH) -> str:
    """
    Generate Arabic emotional TTS using ElevenLabs and return the path to the saved MP3.

    Parameters:
        text (str): The therapeutic response to synthesize.
        tone (str): Emotional tone (e.g., "neutral", "happy", "sad").
        output_path (str): File path to save the audio.

    Returns:
        str: Full path to the generated MP3 file.
    """
    try:
        if not ELEVENLABS_API_KEY:
            raise ValueError("ELEVENLABS_API_KEY is missing.")

        # Mapping tone to voice_id
        tone_to_voice_id = {
            "neutral": CUSTOM_ARABIC_VOICE_ID,  
            "happy": CUSTOM_ARABIC_VOICE_ID,    
            "sad": CUSTOM_ARABIC_VOICE_ID,      
        }
        voice_id = tone_to_voice_id.get(tone, CUSTOM_ARABIC_VOICE_ID)

        # Get the Omani Arabic term
        text = data_processor.get_omani_response(text)

        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

        audio_stream = client.text_to_speech.convert(
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",
            text=text,
            output_format="mp3_22050_32"
        )

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Save audio file
        with open(output_path, "wb") as f:
            for chunk in audio_stream:
                f.write(chunk)

        logging.info(f"[TTS] Arabic TTS saved to: {output_path}")
        return output_path

    except Exception as e:
        logging.exception("[TTS ERROR] Failed to generate Arabic TTS")
        raise MentalHealthChatBotException(e, sys)
