import sys
from modules.logger import logging
from modules.exceptions import MentalHealthChatBotException

# Simple rule-based intent mapping
INTENT_KEYWORDS = {
    "seeking_help": ["أحتاج مساعدة", "ساعدني", "أحتاج دعم", "I need help", "please help"],
    "venting": ["أريد أن أتكلم", "فضفضة", "أريد أن أشارك", "I just need to talk", "vent"],
    "relationship_issue": ["مشاكل عائلية", "زواجي", "أمي", "أبي", "زوجي", "زوجتي", "my wife", "my husband", "parents"],
    "work_stress": ["العمل", "دوام", "مديري", "الضغط الوظيفي", "job", "work", "boss", "office"],
    "spiritual_struggle": ["بعيد عن الله", "أشعر بالذنب", "الدين", "الله", "أحتاج الدعاء", "spiritual", "God", "faith"],
    "existential": ["ما معنى الحياة", "لا أجد هدفًا", "I feel empty", "what is the point", "meaningless"],
    "crisis": ["أريد الموت", "انتحار", "ما الفائدة", "I want to die", "kill myself"]
}


def predict(user_input: str) -> str:
    """
    Predicts the intent behind the user input using simple keyword matching.
    
    Args:
        user_input (str): Arabic or English user message.

    Returns:
        str: Detected intent label.
    """
    try:
        normalized_text = user_input.lower().strip()

        for intent, keywords in INTENT_KEYWORDS.items():
            for phrase in keywords:
                if phrase.lower() in normalized_text:
                    logging.info(f"Intent detected: {intent}")
                    return intent

        logging.info("No specific intent matched. Defaulting to 'general_support'")
        return "general_support"

    except Exception as e:
        logging.error("Intent classification failed.")
        raise MentalHealthChatBotException("Intent classification error", sys)
