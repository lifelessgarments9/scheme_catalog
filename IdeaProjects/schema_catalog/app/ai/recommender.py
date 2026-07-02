import os

import google.generativeai as genai

from app.catalog.models import Device

genai.configure(api_key=os.environ.get("GEMINI_API_KEY", ""))

_MODEL = "gemini-1.5-flash"

_SYSTEM_TEMPLATE = """You are a technical assistant for a chip and controller catalog.
Use the catalog context below to answer questions, suggest suitable devices, and explain technical details.
Be concise and precise.

=== CATALOG CONTEXT ===
{context}
=== END CONTEXT ===
"""


class Recommender:
    """Builds a catalog context and sends prompts to Gemini."""

    def __init__(self):
        self.model = genai.GenerativeModel(_MODEL)
        self._context: str = ""

    def build_context(self) -> str:
        """Collect doc_text from all devices into a single context string."""
        devices = Device.objects.only("name", "description", "doc_text").all()
        parts = [
            f"[{d.name}]\nDescription: {d.description}\nDocs: {d.doc_text or 'N/A'}"
            for d in devices
        ]
        self._context = "\n\n".join(parts)
        return self._context

    def recommend(self, user_prompt: str) -> str:
        """Build prompt with catalog context and call Gemini."""
        context = self._context or self.build_context()
        system = _SYSTEM_TEMPLATE.format(context=context[:28000])  # guard token limit
        response = self.model.generate_content(f"{system}\n\nUser: {user_prompt}")
        return response.text