import sys
import traceback
from modules.logger import logging  
import functools

class MentalHealthChatBotException(Exception):
    """Custom Exception for the mental health bot with enhanced trace logging."""

    def __init__(self, error_message, error_details: type):
        super().__init__(error_message)
        self.error_message = str(error_message)

        try:
            _, _, exc_tb = error_details.exc_info()
            self.line = exc_tb.tb_lineno
            self.filename = exc_tb.tb_frame.f_code.co_filename
        except Exception:
            self.line = "Unknown"
            self.filename = "Unknown"

        # Log the exception immediately
        logging.error(f"Error in [{self.filename}] at line [{self.line}]: {self.error_message}")
        logging.debug("Full traceback:\n" + "".join(traceback.format_exception(*error_details.exc_info())))

    def __str__(self):
        return f"Error in script [{self.filename}] at line [{self.line}]: {self.error_message}"
    
    
def handle_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except MentalHealthChatBotException as e:
            print(f"MentalHealthChatBotException: {e}")
            # Optional: return a specific response or handle further
        except Exception as e:
            print(f"Unexpected Error: {e}")
            # Optional: return a specific response or handle further
    return wrapper