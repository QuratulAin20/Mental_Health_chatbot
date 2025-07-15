import os
import sys
import time
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic
from modules.logger import logging
from modules.exceptions import MentalHealthChatBotException
from utils.timers import Timer
from typing import List, Tuple

timer = Timer()

# Load API keys securely from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Initialize API clients
openai_client = OpenAI(api_key=OPENAI_API_KEY)
claude_client = Anthropic(api_key=ANTHROPIC_API_KEY)

# Therapist prompt: culturally sensitive, code-switch capable
THERAPIST_SYSTEM_PROMPT = (
    "أنت معالج نفسي محترف متخصص في الصحة النفسية والثقافة الخليجية. "
    "ردك يجب أن يكون حساسًا، داعمًا، يتجنب التشخيص المباشر، "
    "ويتحدث باللهجة الخليجية قدر الإمكان. "
    "يمكنك التبديل بين العربية والإنجليزية إذا شعرت أن ذلك سيدعم المستخدم."
)

def generate_culturally_adapted_response(
    conversation_history: List[dict],
    model: str = "gpt-4o",
    attempt: int = 1,
    max_attempts: int = 2
) -> Tuple[str, str, float]:
    start = time.time()
    try:
        if model == "gpt-4o":
            messages = [{"role": "system", "content": THERAPIST_SYSTEM_PROMPT}] + conversation_history
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.5,
                max_tokens=200
            )
            reply = response.choices[0].message.content.strip()
            latency = time.time() - start
            logging.info(f"GPT-4o responded in {latency:.2f}s")
            return reply, "gpt-4o", latency

        elif model == "claude-sonnet":
            response = claude_client.messages.create(
                model="claude-3-sonnet-20250514",
                system=THERAPIST_SYSTEM_PROMPT,
                messages=conversation_history,
                max_tokens=200
            )
            reply = response.content[0].text.strip()
            latency = time.time() - start
            logging.info(f"Claude Sonnet responded in {latency:.2f}s")
            return reply, "claude-sonnet", latency

        else:
            raise ValueError(f"Unsupported model: {model}")

    except Exception as e:
        logging.error(f"{model} failed: {str(e)}")
        if attempt < max_attempts:
            fallback_model = "claude-sonnet" if model == "gpt-4o" else "gpt-4o"
            logging.info(f"Falling back to {fallback_model}")
            return generate_culturally_adapted_response(conversation_history, model=fallback_model, attempt=attempt + 1)
        else:
            raise MentalHealthChatBotException(e, sys)