from pydantic import BaseModel
from typing import Optional, Dict, Any

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ProjectCreate(BaseModel):
    name: str

class ProjectOut(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class AssetOut(BaseModel):
    id: int
    project_id: int
    original_path: str
    result_path: Optional[str] = None
    class Config:
        from_attributes = True

class GenerationRequest(BaseModel):
    asset_id: int
    operations: Dict[str, Any]  # e.g., {"resize": [512,512], "overlay_text": "Hello"}

class JobOut(BaseModel):
    id: int
    status: str
    result_path: Optional[str] = None
    class Config:
        from_attributes = True

class PresetCreate(BaseModel):
    name: str
    params: Dict[str, Any]

class PresetOut(BaseModel):
    id: int
    name: str
    params: Dict[str, Any]
    class Config:
        from_attributes = True
