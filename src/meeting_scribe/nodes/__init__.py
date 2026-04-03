"""Shared utilities for pipeline nodes."""

import os

from google import genai

DEFAULT_MODEL = "gemini-2.0-flash"


def get_client() -> genai.Client:
    """Create a Gemini client using GOOGLE_AI_API_KEY from the environment."""
    api_key = os.environ.get("GOOGLE_AI_API_KEY", "")
    return genai.Client(api_key=api_key)


def get_model() -> str:
    """Get the model name from GEMINI_MODEL env var or default."""
    return os.environ.get("GEMINI_MODEL", DEFAULT_MODEL)
