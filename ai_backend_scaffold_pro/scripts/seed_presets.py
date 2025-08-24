from app.db import SessionLocal, init_db
from app import models
import json

init_db()
db = SessionLocal()

presets = [
    ("square_resize_512", {"resize":[512,512]}),
    ("thumb_crop", {"crop":[0,0,256,256]}),
    ("brand_overlay", {"overlay_text":"Brand"}),
]

for name, params in presets:
    if not db.query(models.Preset).filter(models.Preset.name==name).first():
        db.add(models.Preset(name=name, params=json.dumps(params)))
db.commit()
print("Seeded presets.")
