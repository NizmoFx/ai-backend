from .base import AIProvider
import os

class GeminiProvider(AIProvider):
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY not set")

    def process(self, input_path, output_path, resize=None, crop=None, overlay_text=None):
        # Placeholder: integrate with Google Gemini image APIs when available.
        import shutil
        shutil.copyfile(input_path, output_path)
        return output_path
