from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..deps import get_db
from .. import models, schemas
from ..tasks.tasks import process_generation
from ..config import settings
from ..auth import get_current_user
import os, json

router = APIRouter(prefix="/generation", tags=["generation"])

@router.post("/start", response_model=schemas.JobOut)
def start(req: schemas.GenerationRequest, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    asset = db.get(models.Asset, req.asset_id)
    if not asset:
        raise HTTPException(404, "Asset not found")
    outdir = os.path.join(settings.storage_dir, "generated")
    os.makedirs(outdir, exist_ok=True)
    output_path = os.path.join(outdir, f"asset_{asset.id}_result.jpg")
    job = models.Job(asset_id=asset.id, status="queued", params=json.dumps(req.operations), result_path=output_path)
    db.add(job); db.commit(); db.refresh(job)
    # enqueue
    async_result = process_generation.delay(asset.original_path, output_path, json.dumps(req.operations))
    job.status = f"queued:{async_result.id}"
    db.commit()
    return job

@router.get("/status/{job_id}", response_model=schemas.JobOut)
def status(job_id: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    job = db.get(models.Job, job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    # naive completion check: file exists
    if job.result_path and os.path.exists(job.result_path):
        job.status = "done"
        db.commit()
    return job


@router.post("/start_by_preset", response_model=schemas.JobOut)
def start_by_preset(asset_id: int, preset_id: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    asset = db.get(models.Asset, asset_id)
    preset = db.get(models.Preset, preset_id)
    if not asset or not preset:
        raise HTTPException(404, "Asset or preset not found")
    import json, os
    from ..config import settings
    outdir = os.path.join(settings.storage_dir, "generated")
    os.makedirs(outdir, exist_ok=True)
    output_path = os.path.join(outdir, f"asset_{asset.id}_preset_{preset.id}.jpg")
    job = models.Job(asset_id=asset.id, status="queued", params=preset.params, result_path=output_path)
    db.add(job); db.commit(); db.refresh(job)
    from ..tasks.tasks import process_generation
    async_result = process_generation.delay(asset.original_path, output_path, preset.params)
    job.status = f"queued:{async_result.id}"
    db.commit()
    return job
