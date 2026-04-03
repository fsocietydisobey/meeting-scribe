"""Emotion detection node — analyzes tone and sentiment per speaker from audio + transcript."""

import base64
import json
from pathlib import Path

from meeting_scribe.nodes import get_client, get_model
from meeting_scribe.state import MeetingState


async def detect_emotions(state: MeetingState) -> dict:
    """Analyze speaker emotions from the audio and transcript."""
    audio_path = Path(state["audio_path"])
    transcript = state["transcript"]

    audio_bytes = audio_path.read_bytes()
    audio_b64 = base64.b64encode(audio_bytes).decode()

    client = get_client()
    response = await client.aio.models.generate_content(
        model=get_model(),
        contents=[
            {
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": "audio/wav",
                            "data": audio_b64,
                        }
                    },
                    {
                        "text": (
                            "Analyze the emotional tone of each speaker in this meeting audio. "
                            "You have both the audio (for vocal cues like pitch, pace, volume, "
                            "tension, hesitation) and the transcript below for context.\n\n"
                            "Return JSON with this structure:\n"
                            "```json\n"
                            "{\n"
                            '  "speaker_emotions": [\n'
                            "    {\n"
                            '      "speaker": "Name or Speaker label",\n'
                            '      "overall_tone": "e.g. calm, frustrated, enthusiastic",\n'
                            '      "emotions_detected": ["confident", "slightly anxious"],\n'
                            '      "notable_moments": ["Got tense when discussing deadlines", "Excited about the new feature"]\n'
                            "    }\n"
                            "  ],\n"
                            '  "meeting_mood": "Overall emotional temperature of the meeting"\n'
                            "}\n"
                            "```\n\n"
                            "Rules:\n"
                            "- Base your analysis primarily on vocal tone, not just word choice\n"
                            "- Note shifts in emotion throughout the meeting\n"
                            "- Be specific about notable moments where tone changed\n"
                            "- Return ONLY valid JSON, no markdown fences\n\n"
                            f"## Transcript\n\n{transcript}"
                        ),
                    },
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
        data = {"speaker_emotions": [], "meeting_mood": "unknown"}

    return {
        "speaker_emotions": data.get("speaker_emotions", []),
        "meeting_mood": data.get("meeting_mood", "unknown"),
    }
