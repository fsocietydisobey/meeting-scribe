"""LangGraph pipeline: transcribe → (summarize + extract + emotions) in parallel."""

import asyncio
from pathlib import Path
from typing import cast

from langgraph.graph import StateGraph

from meeting_scribe.log import get_tracer

from meeting_scribe.nodes.emotion import detect_emotions
from meeting_scribe.nodes.extract import extract_actions
from meeting_scribe.nodes.summarize import summarize
from meeting_scribe.nodes.transcribe import transcribe
from meeting_scribe.state import MeetingState


def build_graph() -> StateGraph:
    """Build the meeting processing pipeline.

    After transcription, summarize, extract, and emotion detection
    run in parallel since they all only need the transcript + audio.
    """
    graph = StateGraph(MeetingState)

    graph.add_node("transcribe", transcribe)
    graph.add_node("summarize", summarize)
    graph.add_node("extract_actions", extract_actions)
    graph.add_node("detect_emotions", detect_emotions)

    graph.set_entry_point("transcribe")
    graph.add_edge("transcribe", "summarize")
    graph.add_edge("transcribe", "extract_actions")
    graph.add_edge("transcribe", "detect_emotions")
    graph.add_edge(["summarize", "extract_actions", "detect_emotions"], "__end__")

    return graph


def compile_graph():
    """Compile the graph ready for invocation."""
    return build_graph().compile()


async def process_meeting(audio_path: str | Path) -> MeetingState:
    """Run the full pipeline on an audio file. Returns final state."""
    app = compile_graph()
    result = await app.ainvoke(
        {"audio_path": str(audio_path)}, config={"callbacks": [get_tracer()]}
    )
    return cast(MeetingState, result)


def process_meeting_sync(audio_path: str | Path) -> MeetingState:
    """Synchronous wrapper for process_meeting."""
    return asyncio.run(process_meeting(audio_path))
