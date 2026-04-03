"""Shared utilities for pipeline nodes."""

import os

from google import genai


def get_client() -> genai.Client:
    """Create a Gemini client using GOOGLE_AI_API_KEY from the environment."""
    api_key = os.environ.get("GOOGLE_AI_API_KEY", "")
    return genai.Client(api_key=api_key)
