import re
import sys
from modules.logger import logging
from modules.exceptions import MentalHealthChatBotException

# High-risk Arabic and English phrases indicating self-harm or suicide
SUICIDE_KEYWORDS = [
    "أريد أن أنهي حياتي", "أفكر في الانتحار", "ما الفائدة من حياتي", "لا أستطيع التحمل", 
    "أريد أن أختفي", "أشعر أن لا أحد يهتم", "أريد الموت", "خلاص تعبت", "ودي أنتحر",
    "I want to end my life", "thinking about suicide", "I want to die", 
    "I can't go on", "I feel hopeless", "no reason to live", "kill myself"
]

def detect_risk(user_input: str) -> bool:
    """
    Detects high-risk language (suicidal ideation, self-harm).

    Args:
        user_input (str): Transcribed or typed input.

    Returns:
        bool: True if risk detected, False otherwise.
    """
    try:
        normalized_text = user_input.lower().strip()

        for keyword in SUICIDE_KEYWORDS:
            if re.search(re.escape(keyword.lower()), normalized_text):
                logging.warning(f"High-risk input detected: '{keyword}' matched.")
                return True

        return False

    except Exception as e:
        logging.error("Failed to check for suicide risk.")
        raise MentalHealthChatBotException("Safety layer failed", sys)


def handle_risk_response(language: str = "ar") -> str:
    """
    Returns an emergency response if suicide/self-harm risk detected.

    Args:
        language (str): "ar" (Arabic) or "en" (English fallback).

    Returns:
        str: Escalation message.
    """
    try:
        if language == "ar":
            return (
                "أشعر بأهمية ما تمر به الآن. من فضلك، لا تتردد في طلب المساعدة العاجلة. "
                "اتصل بخدمة الطوارئ أو تحدث مع مختص نفسي فورًا. لست وحدك، وهناك من يهتم بك."
            )
        else:
            return (
                "It sounds like you're going through a very difficult time. "
                "Please reach out to a professional or emergency service right away. You are not alone."
            )
    except Exception as e:
        raise MentalHealthChatBotException("Failed to generate crisis response", sys)
