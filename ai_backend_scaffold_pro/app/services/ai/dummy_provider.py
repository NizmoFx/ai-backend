from .base import AIProvider
from PIL import Image, ImageDraw, ImageFont

class DummyProvider(AIProvider):
    def process(self, input_path, output_path, resize=None, crop=None, overlay_text=None):
        img = Image.open(input_path).convert("RGB")
        if resize:
            img = img.resize((int(resize[0]), int(resize[1])))
        if crop:
            img = img.crop(tuple(map(int, crop)))
        if overlay_text:
            draw = ImageDraw.Draw(img)
            txt = overlay_text[:50]
            draw.text((10,10), txt, fill=(255,0,0))
        img.save(output_path, "JPEG")
        return output_path
