# 🕌 Mental Health Voice Bot

A culturally-sensitive, real-time Arabic voice chatbot built with Flask, designed to provide therapeutic-grade support in the **Omani dialect**. It includes speech recognition, emotional intelligence, spiritual integration, and Arabic emotional TTS output for fully voice-based therapy.

---

## 🚀 Features

- 🎙️ **Voice Capture** — Real-time audio input from users
- 🧠 **Emotion + Intent Detection** — Runs in parallel to reduce latency
- 🤖 **Dual-Model LLM Support** — GPT-4o + Claude Opus fallback or validation
- 🕌 **Cultural Prompting** — Islamic, Gulf-sensitive therapy responses
- 🗣️ **Arabic TTS** — Emotionally adaptive speech output in Omani Arabic
- 🛑 **Crisis Safety** — Suicide detection and escalation warnings
- ♻️ **Session Memory** — In-memory or SQLite for response recall
- ⏱️ **Latency Profiling** — Full turn-level latency tracking

---

## 📂 Project Structure

```bash
OMANI-Bot/
├── app.py                     # Main Flask App (latency-optimized)
├── static/audio/              # Input/output voice storage
├── templates/index.html       # Web UI
├── modules/
│   ├── voice_input.py         # Voice recording
│   ├── transcriber.py         # Whisper STT (Groq or local)
│   ├── emotion_intent.py      # Detect emotion & intent
│   ├── intent_classifier.py   # Predict user need
│   ├── prompt_builder.py      # CBT/Islamic prompt construction
│   ├── response_generator.py  # GPT-4o & Claude LLM responses
│   ├── tts_engine.py          # Emotional Arabic speech
│   ├── safety.py              # Suicide/harm filters
│   ├── memory.py              # Session interaction logging
│   ├── evaluator.py           # Claude vs GPT benchmark stub
│   └── dialect_handling.py    # (Planned) Arabic-English code switch

How It Works
-> User speaks → microphone input recorded

-> Whisper STT converts voice to text

-> Emotion + intent analyzed in parallel

-> Prompt constructed with cultural & spiritual layers

-> GPT-4o (or Claude) generates therapeutic reply

-> Arabic emotional TTS generates voice response

-> Response rendered on UI + audio output played

-> Session stored via in-memory session_memory

```
# Setup environment
pip install -r requirements.txt

# Run with Flask
python app.py

# OR: Run in production
gunicorn -w 2 -b 0.0.0.0:5000 app:app
```



