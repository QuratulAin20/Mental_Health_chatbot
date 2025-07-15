# utils/quran_emotion_mapper.py

# 📖 Quranic verses for English emotion labels
QURAN_VERSES_BY_EMOTION_EN = {
    "Anxiety": "Allah says: \"Verily, in the remembrance of Allah do hearts find rest\" (Surah Ar-Ra’d: 28)",
    "Depression": "Allah says: \"Indeed, with hardship comes ease\" (Surah Ash-Sharh: 6)",
    "Sadness": "Allah says: \"So patience is beautiful, and Allah is the one sought for help\" (Surah Yusuf: 18)",
    "Fear": "Allah says: \"Do not grieve; indeed Allah is with us\" (Surah At-Tawbah: 40)",
    "Anger": "Allah says: \"Those who restrain anger and pardon people\" (Surah Aal Imran: 134)",
    "Isolation": "Allah says: \"And rely upon Allah; sufficient is Allah as Disposer of affairs\" (Surah An-Nisa: 81)",
    # Add more as needed...
}

# 📖 Quranic verses for Arabic emotion labels
QURAN_VERSES_BY_EMOTION_AR = {
    "قلق": "قال الله تعالى: \"ألا بذكر الله تطمئن القلوب\" (الرعد: 28)",
    "اكتئاب": "قال الله تعالى: \"إن مع العسر يسرا\" (الشرح: 6)",
    "حزن": "قال الله تعالى: \"فَصَبْرٌ جَمِيلٌ وَاللَّهُ الْمُسْتَعَانُ\" (يوسف: 18)",
    "خوف": "قال الله تعالى: \"لا تَحْزَنْ إِنَّ اللَّهَ مَعَنَا\" (التوبة: 40)",
    "أرق": "قال الله تعالى: \"وَإِنَّكَ لَتُحْشَرُ إِلَى رَبِّكَ\" (الانشقاق: 6)",
    "غضب": "قال الله تعالى: \"والكاظمين الغيظ\" (آل عمران: 134)",
    "إحباط": "قال الله تعالى: \"لَا تَحْسَبُوا أَنَّمَا أَمْوَالُكُمْ وَأَوْلَادُكُمْ فِتْنَةٌ\" (الأنفال: 28)",
    "فرح": "قال الله تعالى: \"وَأَمَّا بِنِعْمَةِ رَبِّكَ فَحَدِّثْ\" (الضحى: 11)",
    "حيرة": "قال الله تعالى: \"فَإِنَّ مَعَ الْعُسْرِ يُسْرًا\" (الشرح: 5)",
    "شغف": "قال الله تعالى: \"إِنَّ اللَّهَ يُحِبُّ الْمُتَوَكِّلِينَ\" (آل عمران: 159)",
    "ملل": "قال الله تعالى: \"إِنَّمَا الْمُؤْمِنُونَ إِخْوَةٌ\" (الحجرات: 10)",
    "خجل": "قال الله تعالى: \"لَا تَخْشَوْهُمْ وَاخْشَوْنِ\" (المائدة: 44)",
    "عزلة": "قال الله تعالى: \"وَتَوَكَّلْ عَلَى اللَّهِ وَكَفَىٰ بِاللَّهِ وَكِيلًا\" (النساء: 81)",
    "قلق اجتماعي": "قال الله تعالى: \"وَلَا تَقْنَطُوا مِن رَّحْمَةِ اللَّهِ\" (الزمر: 53)",
    "شعور بالذنب": "قال الله تعالى: \"إِنَّ اللَّهَ غَفُورٌ رَّحِيمٌ\" (الزمر: 53)",
    "شعور بالفشل": "قال الله تعالى: \"وَلا تَحْزَنْ عَلَيْهِمْ\" (المطففين: 15)",
    "قلق حول المستقبل": "قال الله تعالى: \"وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ\" (الطلاق: 3)",
    "سعادة مؤقتة": "قال الله تعالى: \"إِنَّمَا الْحَيَاةُ الدُّنْيَا لَهْوٌ وَلَعِبٌ\" (الحديد: 20)",
    "استرخاء": "قال الله تعالى: \"ادْخُلُوا فِي سِلْمٍ كَافَّةً\" (البقرة: 208)"
}

def get_quranic_reference_by_emotion(emotion: str, language: str = "en") -> str:
    if language == "en":
        return QURAN_VERSES_BY_EMOTION_EN.get(emotion, "")
    elif language == "ar":
        return QURAN_VERSES_BY_EMOTION_AR.get(emotion, "")
    return ""
