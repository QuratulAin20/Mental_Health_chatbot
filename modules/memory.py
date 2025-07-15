from collections import defaultdict
from datetime import datetime
from typing import List, Dict, Any

# Global memory dictionary: session_id -> list of interaction dicts
session_memory = defaultdict(list)

def remember_interaction(session_id: str, emotion: str, verse: str, response: str) -> None:
    """Store an interaction in session memory."""
    session_memory[session_id].append({
        "timestamp": datetime.utcnow().isoformat(),
        "emotion": emotion,
        "quran_verse": verse,
        "bot_response": response
    })

def get_session_memory(session_id: str) -> List[Dict[str, Any]]:
    """Retrieve all interactions for a given session ID."""
    return session_memory.get(session_id, [])