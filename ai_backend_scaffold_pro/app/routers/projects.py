from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from ..deps import get_db
from .. import models, schemas
from ..services import storage
from ..auth import get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("", response_model=schemas.ProjectOut)
def create_project(payload: schemas.ProjectCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    p = models.Project(name=payload.name)
    db.add(p); db.commit(); db.refresh(p)
    return p

@router.post("/{project_id}/assets", response_model=schemas.AssetOut)
async def upload_asset(project_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    project = db.get(models.Project, project_id)
    if not project:
        raise HTTPException(404, "Project not found")

saved = storage.save_upload(file.file, file.filename)
# moderation
from ..services.moderation import basic_checks
basic_checks(saved)

    asset = models.Asset(project_id=project_id, original_path=saved)
    db.add(asset); db.commit(); db.refresh(asset)
    return asset
