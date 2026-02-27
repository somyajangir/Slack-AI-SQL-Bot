# llm.py
"""
LangChain SQL Integration for Natural Language → SQL

Assignment-compliant version:
- Single LLM call
- Outputs ONE SELECT statement
- No agent
- No multi-step reasoning
- Minimal prompt
"""

import logging
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from config import config
from error_handlers import SQLGenerationError

logger = logging.getLogger(__name__)


class SQLChainExecutor:
    """
    Minimal NL → SQL generator

    This version:
    - Makes exactly ONE LLM call
    - Uses a short schema description
    - Returns a single SELECT statement
    - No agents, no retries, no loops
    """

    def __init__(self):
        try:
            logger.info("Initializing SQL generator...")

            self.llm = ChatGroq(
                model=config.GROQ_MODEL,
                temperature=0,
                api_key=config.GROQ_API_KEY,
                timeout=20
            )

            logger.info(f"LLM initialized: {config.GROQ_MODEL}")

            # Minimal schema prompt (assignment compliant)
            self.system_prompt = """
You are a PostgreSQL expert.

There is ONLY one table:

sales_daily(
    date DATE,
    region TEXT,
    category TEXT,
    revenue NUMERIC(12,2),
    orders INTEGER,
    created_at TIMESTAMPTZ
)

Rules:
- Output ONLY ONE valid PostgreSQL SELECT statement.
- Do NOT explain anything.
- Do NOT add markdown.
- Do NOT add comments.
- Only return SQL.
"""

        except Exception as e:
            logger.error(f"LLM initialization failed: {str(e)}")
            raise SQLGenerationError(
                message=str(e),
                user_friendly="Failed to initialize SQL system."
            )

    def execute(self, question: str) -> dict:
        """
        Convert natural language → SQL (single call)

        Returns:
        {
            "result": "SELECT ...;",
            "success": True
        }
        """
        try:
            logger.info(f"Generating SQL for: {question}")

            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=question)
            ]

            response = self.llm.invoke(messages)

            sql = response.content.strip()

            # Ensure semicolon at end
            if not sql.endswith(";"):
                sql += ";"

            logger.info("SQL generated successfully")

            return {
                "result": sql,
                "success": True
            }

        except Exception as e:
            logger.error(f"SQL generation error: {str(e)}", exc_info=True)
            raise SQLGenerationError(
                message=str(e),
                user_friendly="Failed to generate SQL. Please rephrase your question."
            )


# Global instance (used by main.py)
sql_chain = SQLChainExecutor()