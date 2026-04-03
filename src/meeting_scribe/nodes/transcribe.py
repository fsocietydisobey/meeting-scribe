"""Transcription node — sends audio to Gemini for speech-to-text."""

import base64
from pathlib import Path

from meeting_scribe.log import get_logger
from meeting_scribe.nodes import get_client
from meeting_scribe.state import MeetingState

log = get_logger("transcribe")


async def transcribe(state: MeetingState) -> dict:
    """Transcribe audio file using Gemini's native audio understanding."""
    audio_path = Path(state["audio_path"])
    log.info("Transcribing: %s", audio_path.name)

    # Read and encode audio
    audio_bytes = audio_path.read_bytes()
    audio_b64 = base64.b64encode(audio_bytes).decode()
    log.info("Audio size: %.1f MB", len(audio_bytes) / (1024 * 1024))

    client = get_client()
    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
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

    log.info("Transcript length: %d chars", len(response.text))
    log.debug("Transcript:\n%s", response.text)
    return {"transcript": response.text}
