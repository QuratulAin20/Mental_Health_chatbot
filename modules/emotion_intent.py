import os
import sys
from dotenv import load_dotenv
from groq import Groq
from modules.logger import logging
from modules.exceptions import MentalHealthChatBotException
from utils.timers import Timer 
timer = Timer()


# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
try:
    groq_client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    raise MentalHealthChatBotException("Failed to initialize Groq client", sys)


def detect_emotion_and_intent(transcribed_text: str) -> dict:
    """
    Uses Groq LLaMA3-70B to detect emotion and intent in Arabic + Omani dialect.
    
    Returns:
        {
            "emotion": "قلق",
            "intent": "استشارة نفسية"
        }
    """
    try:
        if not transcribed_text.strip():
            raise ValueError("Empty transcription passed for analysis.")

        logging.info("Running emotion and intent classification...")
        timer.start("emotion_intent")

        # Dual-language system prompt (Arabic + English)
        system_prompt = (
            "أنت مساعد تحليل نفسي يفهم اللهجة العمانية.\n"
            "عند إعطائك نصًا، حدّد المشاعر (مثل القلق، الحزن، الغضب...) والنوايا (مثل استشارة، تفريغ، أزمة...)\n"
            "الرد يجب أن يكون بصيغة JSON:\n"
            '{\n  "emotion": "القلق",\n  "intent": "استشارة نفسية"\n}\n\n'
            "You are an Arabic-speaking emotional support assistant.\n"
            "Your job is to extract the user's **emotion** and **intent** from a given utterance (often in Omani dialect).\n"
            "Return a JSON with Arabic labels for emotion and intent, like:\n"
            "{\n \"emotion\": \"قلق\",\n  \"intent\": \"استشارة نفسية\"\n}"
        )

        user_prompt = f"النص:\n{transcribed_text.strip()}"

        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5,
            max_tokens=200
        )

        timer.stop("emotion_intent")

        reply = response.choices[0].message.content.strip()
        logging.debug(f"LLM raw response: {reply}")

        # Safe parsing
        result = eval(reply, {"__builtins__": {}})
        assert "emotion" in result and "intent" in result

        logging.info(f"Emotion: {result['emotion']} | Intent: {result['intent']}")
        return result

    except Exception as e:
        raise MentalHealthChatBotException("Failed to detect emotion and intent", sys)

