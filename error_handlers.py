"""
Error handling for Slack Data Bot
When something goes wrong, we catch it here and create
a nice message for the user instead of showing technical errors.
"""

from typing import Optional
from dataclasses import dataclass


# ========== CUSTOM ERROR CLASSES ==========

@dataclass
class BotError(Exception):
    """
    Base error class for our bot.

    Stores:
    - technical message (for logs)
    - user-friendly message (for Slack)
    """
    message: str
    user_friendly: Optional[str] = None

    def __str__(self):
        return self.user_friendly or self.message


@dataclass
class SQLGenerationError(BotError):
    """Error when LLM can't generate SQL"""
    pass


@dataclass
class DatabaseError(BotError):
    """Error when database query fails"""
    pass


@dataclass
class ValidationError(BotError):
    """Error when input is invalid"""
    pass


@dataclass
class SlackError(BotError):
    """Error when Slack communication fails"""
    pass


# ========== ERROR HANDLER CLASS ==========

class ErrorHandler:
    """Centralized error handling and formatting"""

    @staticmethod
    def format_error(error: Exception) -> dict:
        """
        Convert any exception to structured dictionary.
        """

        if isinstance(error, BotError):
            return {
                "type": error.__class__.__name__,
                "message": error.message,
                "slack_text": f"⚠️ {error.user_friendly or error.message}",
            }

        # Unknown error fallback
        return {
            "type": "UnexpectedError",
            "message": str(error),
            "slack_text": "⚠️ An unexpected error occurred. Please try again later.",
        }