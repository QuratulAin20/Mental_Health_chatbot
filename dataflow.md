1. Voice Input (microphone) 
   ↓
2. Transcription (Groq Whisper) 
   ↓
3. Emotion & Intent Detection (emotion_intent.py with few-shot prompt templates)
   ↓
4. Response Generation 
   - Prompt Templates (CBT + Spiritual + Cultural)
   - Dual LLM (OpenAI + Claude fallback)
   ↓
5. Safety Mechanism & Filtering
   - Suicide risk detection
   - Harmful intent filtering
   - Escalation + Referral protocols
   ↓
6. Response Evaluation (openai vs claude)
   ↓
7. Voice Output (TTS: Arabic-Omani dialect)
   ↓
8. Session Logging + Consent + Emergency Trigger + HIPAA Compliance
