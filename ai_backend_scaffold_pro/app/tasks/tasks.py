from .worker import celery_app
from ..config import settings
from ..services.ai.dummy_provider import DummyProvider
from ..services.ai.openai_provider import OpenAIProvider
from ..services.ai.gemini_provider import GeminiProvider
import json, os

def get_provider():
    prov = settings.ai_provider.lower()
    if prov == "openai":
        return OpenAIProvider(settings.openai_key)
    if prov == "gemini":
        return GeminiProvider(settings.gemini_key)
    return DummyProvider()

@celery_app.task(name="app.tasks.tasks.process_generation")
def process_generation(input_path: str, output_path: str, params_json: str) -> str:
    params = json.loads(params_json)
    provider = get_provider()
    resize = params.get("resize")
    crop = params.get("crop")
    overlay_text = params.get("overlay_text")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    result = provider.process(input_path, output_path, resize=resize, crop=crop, overlay_text=overlay_text)
    return result
