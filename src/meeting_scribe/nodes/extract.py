"""Extraction node — pulls action items, decisions, and participants."""

import json

from meeting_scribe.log import get_logger
from meeting_scribe.nodes import get_client
from meeting_scribe.state import MeetingState

log = get_logger("extract")


async def extract_actions(state: MeetingState) -> dict:
    """Extract action items, decisions, and participants from the transcript."""
    transcript = state["transcript"]
    log.info("Extracting action items, decisions, participants")

    client = get_client()
    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
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
        # Strip markdown code fences if present
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            text = text.rsplit("```", 1)[0]
        data = json.loads(text)
        log.info("Extracted %d action items, %d decisions, %d participants",
                 len(data.get("action_items", [])), len(data.get("decisions", [])),
                 len(data.get("participants", [])))
    except (json.JSONDecodeError, IndexError):
        log.warning("Failed to parse Gemini response as JSON, returning empty results")
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
