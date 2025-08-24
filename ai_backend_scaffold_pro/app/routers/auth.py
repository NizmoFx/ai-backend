from fastapi import APIRouter
from ..auth import create_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(username: str = "demo"):
    token = create_token(username)
    return {"access_token": token, "token_type": "bearer"}
