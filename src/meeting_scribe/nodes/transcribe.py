"""Transcription node — sends audio to Gemini for speech-to-text."""

import base64
from pathlib import Path

from meeting_scribe.nodes import get_client, get_model
from meeting_scribe.state import MeetingState


async def transcribe(state: MeetingState) -> dict:
    """Transcribe audio file using Gemini's native audio understanding."""
    audio_path = Path(state["audio_path"])

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
                            "Transcribe this meeting audio verbatim. "
                            "When speakers introduce themselves, use their actual names as labels "
                            "(e.g., 'Joseph:', 'Mark:') instead of generic labels like 'Speaker 1'. "
                            "If a speaker hasn't been identified, use 'Unknown Speaker' until you can match their voice to a name. "
                            "Preserve natural speech patterns but clean up filler words. "
                            "Format as a clean transcript with timestamps if possible."
                        ),
                    },
                ],
            }
        ],
    )

    return {"transcript": response.text}
