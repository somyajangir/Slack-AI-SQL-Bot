# main.py
"""
FastAPI Application - Slack Data Bot
Handles Slack slash commands and coordinates:
Slack → LangChain → PostgreSQL → Slack
"""

import logging
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from slack_sdk.signature import SignatureVerifier

from config import config
from llm import sql_chain
from db import db_executor
from slack_handler import slack_handler
from utils import format_error_message, log_event
from error_handlers import BotError, ErrorHandler


# ============================================================
# LOGGING SETUP
# ============================================================

logging.basicConfig(
    level=config.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# ============================================================
# FASTAPI INIT
# ============================================================

app = FastAPI(
    title="Slack Data Bot",
    description="Natural language to SQL Slack bot",
    version="1.0.0"
)

signature_verifier = SignatureVerifier(config.SLACK_SIGNING_SECRET)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/")
async def root():
    return {
        "service": "Slack Data Bot",
        "status": "running"
    }


# ============================================================
# SLACK SLASH COMMAND ENDPOINT
# ============================================================

@app.post("/slack/slash-command")
async def handle_slash_command(request: Request, background_tasks: BackgroundTasks):
    """
    Slack requires response within 3 seconds.
    So we:
    1. Verify signature
    2. Immediately return response
    3. Process in background
    """

    # -------------------------------
    # 1️⃣ Verify Slack Signature
    # -------------------------------
    body = await request.body()

    if not signature_verifier.is_valid_request(body, request.headers):
        raise HTTPException(status_code=401, detail="Unauthorized")

    form_data = await request.form()

    question = form_data.get("text", "").strip()
    response_url = form_data.get("response_url")
    user_id = form_data.get("user_id", "unknown")
    channel_id = form_data.get("channel_id", "unknown")

    log_event("slash_command_received", {
        "user": user_id,
        "channel": channel_id,
        "question": question[:50]
    })

    # -------------------------------
    # 2️⃣ Add Background Task
    # -------------------------------
    background_tasks.add_task(
        process_slash_command,
        question,
        response_url,
        user_id
    )

    # -------------------------------
    # 3️⃣ Immediate Response to Slack
    # -------------------------------
    return {
        "response_type": "ephemeral",
        "text": "Processing your request..."
    }


# ============================================================
# BACKGROUND PROCESSING FUNCTION
# ============================================================

async def process_slash_command(question: str, response_url: str, user_id: str):
    try:
        # Validate question
        if not question:
            await slack_handler.send_response(
                response_url,
                "Please ask a question.\nExample: `/ask-data show revenue by region`"
            )
            return

        if len(question) > 500:
            await slack_handler.send_response(
                response_url,
                "Question too long (max 500 characters)."
            )
            return

        logger.info(f"Processing question: {question}")

        # ---------------------------------------
        # 1️⃣ Generate SQL
        # ---------------------------------------
        sql_result = sql_chain.execute(question)
        sql_query = sql_result["result"]

        logger.info(f"Generated SQL: {sql_query}")

        # ---------------------------------------
        # 2️⃣ Execute SQL
        # ---------------------------------------
        columns, rows, info = db_executor.execute_query(sql_query)

        # ---------------------------------------
        # 3️⃣ Format Result for Slack
        # ---------------------------------------

        if not rows:
            message = "*Results:*\n\nNo data found."
        else:
            # Format as simple table
            header = " | ".join(columns)
            separator = "-" * len(header)

            formatted_rows = []
            for row in rows:
                formatted_rows.append(" | ".join(str(cell) for cell in row))

            table = "\n".join(formatted_rows)

            message = f"*Results:*\n```{header}\n{separator}\n{table}```\n_{info}_"

        # ---------------------------------------
        # 4️⃣ Send Result to Slack
        # ---------------------------------------
        await slack_handler.send_response(response_url, message)

        log_event("query_success", {
            "user": user_id
        })

    except BotError as e:
        error_response = ErrorHandler.format_error(e)

        await slack_handler.send_response(
            response_url,
            format_error_message(error_response["slack_text"])
        )

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)

        await slack_handler.send_response(
            response_url,
            format_error_message("Unexpected error occurred.")
        )

# ============================================================
# STARTUP & SHUTDOWN
# ============================================================

@app.on_event("startup")
async def startup():
    logger.info("Slack Data Bot starting...")


@app.on_event("shutdown")
async def shutdown():
    db_executor.close()
    logger.info("Application shutdown complete.")


# ============================================================
# LOCAL RUN
# ============================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )