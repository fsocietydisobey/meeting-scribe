"""Summarization node — generates a concise meeting summary."""

from meeting_scribe.nodes import get_client, get_model
from meeting_scribe.state import MeetingState


async def summarize(state: MeetingState) -> dict:
    """Summarize the meeting transcript using Gemini."""
    transcript = state["transcript"]

    client = get_client()
    response = await client.aio.models.generate_content(
        model=get_model(),
        contents=[
            {
                "parts": [
                    {
                        "text": (
                            "You are a meeting summarizer. Given the following meeting transcript, "
                            "provide a clear, structured summary.\n\n"
                            "Include:\n"
                            "1. **Meeting Overview** — 2-3 sentence high-level summary\n"
                            "2. **Key Topics Discussed** — bullet points of main topics\n"
                            "3. **Important Details** — any numbers, dates, names, or specifics mentioned\n\n"
                            "Keep it concise but comprehensive.\n\n"
                            f"## Transcript\n\n{transcript}"
                        ),
                    }
                ],
            }
        ],
    )

    return {"summary": response.text}
