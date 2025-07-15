"""
setup.py — Create OMANI Mental Health Voice Bot structure in current folder
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent  # ← use current folder

# Folders to create (relative to current folder)
folders = [
    "modules",
    "utils",
    "utils/prompts",
    "static",
    "templates",
    "logs"
]

# Files to create with stub content
files = {
    "app.py": "# Flask entry point\n",
    "requirements.txt": "# Project dependencies\n-e .\n",
    "README.md": "# OMANI Mental Health Voice Bot\n",
    "modules/__init__.py": "",
    "utils/__init__.py": "",
    "templates/index.html": "<!-- Main UI goes here -->\n",
    "static/style.css": "/* UI Styling */\n",
    "utils/prompts/.gitkeep": "",

    # Core module stubs
    "modules/logger.py": "# Logging setup\n",
    "modules/exceptions.py": "# Exception handler\n",
    "modules/voice_input.py": "# Record and save voice input\n",
    "modules/transcriber.py": "# Transcribe voice with Groq Whisper\n",
    "modules/emotion_intent.py": "# Detect emotion and intent\n",
    "modules/prompt_builder.py": "# Build full prompt with cultural layers\n",
    "modules/response_generator.py": "# Generate LLM response (OpenAI/Claude)\n",
    "modules/tts_engine.py": "# Arabic emotional text-to-speech\n",
    "modules/safety.py": "# Crisis escalation and filtering\n",
    "modules/evaluator.py": "# Compare GPT-4o vs Claude\n",
    "modules/memory.py": "for saving session",
    "utils/timers.py": "# Latency timers\n"
    
}

def create_structure():
    print(f"📁 Creating project structure in: {BASE_DIR}\n")

    for folder in folders:
        full_path = BASE_DIR / folder
        os.makedirs(full_path, exist_ok=True)
        print(f"📁 Created folder: {full_path}")

    for file_path, content in files.items():
        full_file = BASE_DIR / file_path
        if not full_file.exists():
            full_file.write_text(content, encoding="utf-8")
            print(f"📝 Created file: {full_file}")
        else:
            print(f"✅ Skipped (already exists): {full_file}")

if __name__ == "__main__":
    create_structure()
    print("\n✅ Project scaffold complete in current directory.")
