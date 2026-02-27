# slack_handler.py

import logging
import httpx
from slack_sdk import WebClient
from config import config
from error_handlers import SlackError

logger = logging.getLogger(__name__)


class SlackHandler:
    """Handle Slack API interactions"""

    def __init__(self):
        self.client = WebClient(token=config.SLACK_BOT_TOKEN)
        logger.info("Slack client initialized")

    async def send_response(self, response_url: str, text: str) -> bool:
        """
        Send response to Slack using async HTTP
        """
        try:
            payload = {
                "text": text,
                "mrkdwn": True
            }

            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(response_url, json=payload)

            if response.status_code != 200:
                raise SlackError(
                    message=f"Slack responded with {response.status_code}",
                    user_friendly="Failed to send message to Slack"
                )

            logger.info("Response sent to Slack")
            return True

        except SlackError:
            raise

        except Exception as e:
            logger.error(f"Slack send failed: {str(e)}")
            raise SlackError(
                message=str(e),
                user_friendly="Failed to send response to Slack"
            )


slack_handler = SlackHandler()