"""Meeting pipeline state definition."""

from typing import TypedDict


class MeetingState(TypedDict):
    """State flowing through the LangGraph pipeline.

    Required keys are always present. Optional keys are populated
    progressively as nodes execute.
    """

    # Input — always present
    audio_path: str
    transcript: str

    # Populated by downstream nodes
    summary: str
    action_items: list[str]
    decisions: list[str]
    participants: list[str]
    speaker_emotions: list[dict]
    meeting_mood: str
