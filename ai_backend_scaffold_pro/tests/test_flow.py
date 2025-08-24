import os, io
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def get_token():
    r = client.post("/auth/login")
    return r.json()["access_token"]

def test_flow(tmp_path):
    # login
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    # project
    r = client.post("/projects", json={"name": "demo"}, headers=headers)
    pid = r.json()["id"]
    # asset upload (generate a tiny image)
    from PIL import Image
    img = Image.new("RGB", (64,64), (123,222,111))
    buf = io.BytesIO()
    img.save(buf, format="JPEG"); buf.seek(0)
    files = {"file": ("sample.jpg", buf, "image/jpeg")}
    r = client.post(f"/projects/{pid}/assets", files=files, headers=headers)
    aid = r.json()["id"]
    # start generation
    r = client.post("/generation/start", json={"asset_id": aid, "operations": {"resize": [32,32], "overlay_text": "hi"}}, headers=headers)
    assert r.status_code == 200
