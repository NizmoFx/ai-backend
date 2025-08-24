from .base import AIProvider
import os, requests

class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY not set")

    def process(self, input_path, output_path, resize=None, crop=None, overlay_text=None):
        # Placeholder showing where you'd call an OpenAI image edit API.
        # In this scaffold we just copy the input to output to keep flow working.
        import shutil
        shutil.copyfile(input_path, output_path)
        return output_path
