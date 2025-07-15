import sys
from modules.logger import logging
from modules.exceptions import MentalHealthChatBotException

def build_prompt(transcribed_text: str, emotion: str, intent: str, language: str = "ar") -> str:
    """
    Builds a culturally grounded therapeutic prompt in Arabic, with emotion, intent, and context.
    """
    try:
        logging.info(" Building culturally adapted prompt...")

        # Fallbacks
        emotion = emotion or "غير محدد"
        intent = intent or "غير معروف"
        user_text = transcribed_text.strip() or "..."

        base_arabic_prompt = f"""
أنت مستشار نفسي ناطق بالعربية، تفهم الثقافة العمانية جيدًا. 
مهمتك تقديم رد داعم عاطفيًا، محترم دينيًا، وآمن نفسيًا. 
المستخدم عبّر عن مشاعر تتعلق بـ **{emotion}** ونية **{intent}**.
النص الذي قاله المستخدم:

"{user_text}"

تعليمات الرد:
- كن متعاطفًا، لا تستخدم لغة حادة أو جافة.
- اربط الرد بالقيم الإسلامية عند الحاجة (مثلاً الصبر، الدعاء، الراحة بالله).
- لا تقدم تشخيصات، بل استخدم أساليب الدعم النفسي الإيجابي.
- إذا ظهرت علامات أزمة، وجه المستخدم للبحث عن دعم عاجل.
- استخدم لهجة رسمية خفيفة مفهومة لعُمانيين.

ابدأ الرد الآن:
        """.strip()

        if language in ["en", "mixed"]:
            english_overlay = f"""
You are a culturally-aware mental health assistant.
The user expressed the emotion: **{emotion}** and the intent: **{intent}**.
Their message was:
"{user_text}"

Please generate a response in Modern Standard Arabic that:
- Acknowledges their feelings empathetically.
- Uses gentle language aligned with Islamic values (e.g., patience, prayer).
- Avoids clinical diagnosis.
- Encourages them to seek help if in crisis.
- Sounds culturally natural to Gulf Arabic speakers (especially Omanis).

Start your response in Arabic now.
            """.strip()

            full_prompt = base_arabic_prompt + "\n\n# --- English Guidance ---\n" + english_overlay
        else:
            full_prompt = base_arabic_prompt

        logging.debug("Final prompt constructed.")
        return full_prompt

    except Exception as e:
        raise MentalHealthChatBotException("Failed to build therapeutic prompt", sys)
