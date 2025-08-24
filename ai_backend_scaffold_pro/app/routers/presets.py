from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..deps import get_db
from .. import models, schemas
from ..auth import get_current_user
import json

router = APIRouter(prefix="/presets", tags=["presets"])

@router.post("", response_model=schemas.PresetOut)
def create_preset(body: schemas.PresetCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    p = models.Preset(name=body.name, params=json.dumps(body.params))
    db.add(p); db.commit(); db.refresh(p)
    return schemas.PresetOut(id=p.id, name=p.name, params=body.params)

@router.get("", response_model=list[schemas.PresetOut])
def list_presets(db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    out = []
    for p in db.query(models.Preset).all():
        out.append(schemas.PresetOut(id=p.id, name=p.name, params=json.loads(p.params)))
    return out

@router.get("/{preset_id}", response_model=schemas.PresetOut)
def get_preset(preset_id: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    p = db.get(models.Preset, preset_id)
    if not p: raise HTTPException(404, "Not found")
    import json
    return schemas.PresetOut(id=p.id, name=p.name, params=json.loads(p.params))
