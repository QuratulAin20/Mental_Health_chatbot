import os
import datetime
import logging

# Create log directory if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Session-based filename for general interaction logs
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
DEFAULT_LOG_FILE = os.path.join(LOG_DIR, f"session_{timestamp}.log")

# Setup standard Python logging for internal tracking
logging.basicConfig(
    filename=DEFAULT_LOG_FILE,
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    encoding='utf-8'
)

# Crisis detection terms
CRISIS_KEYWORDS = [
    "انتحار", "أنتحر", "أموت", "أنهي حياتي", "ما أريد أعيش", "أقتل نفسي",
    "زهقت", "خلاص", "ودّيت أرتاح", "كرهت حياتي"
]


def log_interaction(user_input: str, bot_response: str, model: str = "gpt-4o", log_file: str = DEFAULT_LOG_FILE):
    """
    Logs a single user-bot exchange with optional crisis escalation flag.
    """
    try:
        crisis_flag = any(keyword in user_input.lower() for keyword in CRISIS_KEYWORDS)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}]\n")
            f.write(f"USER: {user_input.strip()}\n")
            f.write(f"BOT ({model}): {bot_response.strip()}\n")
            f.write(f"CRISIS_ESCALATION: {crisis_flag}\n\n")

        # Internal system log
        logging.info(f" USER: {user_input.strip()}")
        logging.info(f"BOT ({model}): {bot_response.strip()}")
        if crisis_flag:
            logging.warning(" CRISIS ESCALATION DETECTED")

    except Exception as e:
        logging.exception(" Failed to log interaction")


def log_model_comparison(user_input: str, gpt_response: str, claude_response: str, gpt_time: float, claude_time: float):
    """
    Logs both model responses for the same input to model_comparisons.log.
    """
    try:
        log_path = os.path.join(LOG_DIR, "model_comparisons.log")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"\n USER INPUT:\n{user_input.strip()}\n")
            f.write(f"\n GPT-4o ({gpt_time:.2f}s):\n{gpt_response.strip()}\n")
            f.write(f"\n Claude-3 Opus ({claude_time:.2f}s):\n{claude_response.strip()}\n")
            f.write("-" * 60 + "\n")
    except Exception as e:
        logging.exception(" Failed to log model comparison")
