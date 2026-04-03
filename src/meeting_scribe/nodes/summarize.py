"""Summarization node — generates a concise meeting summary."""

from meeting_scribe.log import get_logger
from meeting_scribe.nodes import get_client
from meeting_scribe.state import MeetingState

log = get_logger("summarize")


async def summarize(state: MeetingState) -> dict:
    """Summarize the meeting transcript using Gemini."""
    transcript = state["transcript"]
    log.info("Summarizing transcript (%d chars)", len(transcript))

    client = get_client()
    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
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

    log.info("Summary generated (%d chars)", len(response.text))
    log.debug("Summary:\n%s", response.text)
    return {"summary": response.text}
