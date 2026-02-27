"""
Utility functions for Slack Data Bot
Reusable helper functions used across the application.
"""

import logging
from typing import List, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


def format_table_for_slack(
    columns: List[str],
    rows: List[Tuple],
    query_info: str
) -> str:
    """
    Format database results into Slack-friendly markdown table.
    """

    if not columns:
        return "No results found"

    if not rows:
        return "No data returned"

    header = " | ".join(columns)
    separator = " | ".join(["---"] * len(columns))

    row_strs = []
    for row in rows[:10]:  # Limit to first 10 rows
        row_strs.append(" | ".join(str(v) for v in row))

    table = f"```\n{header}\n{separator}\n" + "\n".join(row_strs)

    if len(rows) > 10:
        table += f"\n... and {len(rows) - 10} more rows"

    table += f"\n```\n_Query returned {query_info}_"

    return table


def log_event(event_type: str, data: dict):
    """
    Log important system events.
    """
    logger.info(f"EVENT: {event_type} - {data}")


def format_error_message(error_text: str) -> str:
    """
    Format error message for Slack display.
    """
    return f"```\n⚠️ {error_text}\n```"