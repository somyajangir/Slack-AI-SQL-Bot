"""
Configuration management for Slack Data Bot
This file handles all settings, API keys, and environment variables.
Think of it as the "settings" of your application.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration - centralized settings"""

    # ========== SLACK SETTINGS ==========
    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")

    # ========== GROQ SETTINGS (LLM Provider) ==========
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")

    # ========== DATABASE SETTINGS ==========
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/analytics"
    )

    # ========== APPLICATION SETTINGS ==========
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

    # ========== PERFORMANCE & LIMITS ==========
    MAX_RESULT_ROWS = 10
    QUERY_TIMEOUT = 30
    CACHE_TTL = 3600
    DB_POOL_MIN = 1
    DB_POOL_MAX = 10

    @classmethod
    def validate(cls):
        """
        Validate all required configs are set.
        Runs when app starts.
        """

        required = [
            "SLACK_BOT_TOKEN",
            "SLACK_SIGNING_SECRET",
            "GROQ_API_KEY",
            "DATABASE_URL",
        ]

        missing = [key for key in required if not getattr(cls, key)]

        if missing:
            raise ValueError(
                f"Missing required configuration: {', '.join(missing)}\n"
                f"Check your .env file!"
            )

        print("Configuration validated successfully")


# Create instance
config = Config()

# Validate on import (fail fast)
config.validate()