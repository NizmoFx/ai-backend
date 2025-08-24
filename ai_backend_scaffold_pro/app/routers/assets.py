from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from ..deps import get_db
from .. import models
from ..auth import get_current_user

router = APIRouter(prefix="/assets", tags=["assets"])

@router.get("/{asset_id}")
def download(asset_id: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    asset = db.get(models.Asset, asset_id)
    if not asset:
        raise HTTPException(404, "Not found")
    path = asset.result_path or asset.original_path
    try:
        with open(path, "rb") as f:
            data = f.read()
        return Response(content=data, media_type="image/jpeg")
    except FileNotFoundError:
        raise HTTPException(404, "File missing")
