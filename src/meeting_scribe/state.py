"""Meeting pipeline state definition."""

from typing import TypedDict


class MeetingState(TypedDict, total=False):
    """State flowing through the LangGraph pipeline."""

    # Input
    audio_path: str

    # After transcription
    transcript: str

    # After summarization
    summary: str

    # After extraction
    action_items: list[str]
    decisions: list[str]
    participants: list[str]

    # After emotion detection
    speaker_emotions: list[dict]
    meeting_mood: str
