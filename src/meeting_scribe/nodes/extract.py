"""Extraction node — pulls action items, decisions, and participants."""

import json

from meeting_scribe.nodes import get_client, get_model
from meeting_scribe.state import MeetingState


async def extract_actions(state: MeetingState) -> dict:
    """Extract action items, decisions, and participants from the transcript."""
    transcript = state["transcript"]

    client = get_client()
    response = await client.aio.models.generate_content(
        model=get_model(),
        contents=[
            {
                "parts": [
                    {
                        "text": (
                            "Analyze this meeting transcript and extract the following as JSON:\n\n"
                            "```json\n"
                            "{\n"
                            '  "action_items": ["Action item with owner if mentioned"],\n'
                            '  "decisions": ["Decision that was made"],\n'
                            '  "participants": ["Name or Speaker label"]\n'
                            "}\n"
                            "```\n\n"
                            "Rules:\n"
                            "- Action items should be specific and actionable\n"
                            "- Include the responsible person if mentioned\n"
                            "- Decisions should capture what was agreed upon\n"
                            "- List all identifiable participants\n"
                            "- Return ONLY valid JSON, no markdown fences\n\n"
                            f"## Transcript\n\n{transcript}"
                        ),
                    }
                ],
            }
        ],
    )

    try:
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            text = text.rsplit("```", 1)[0]
        data = json.loads(text)
    except (json.JSONDecodeError, IndexError):
        data = {
            "action_items": [],
            "decisions": [],
            "participants": [],
        }

    return {
        "action_items": data.get("action_items", []),
        "decisions": data.get("decisions", []),
        "participants": data.get("participants", []),
    }
