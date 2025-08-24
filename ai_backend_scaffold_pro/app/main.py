from fastapi import FastAPI
from .db import init_db
from .logging_conf import setup_logging
from .routers import auth, projects, generation, assets, presets

app = FastAPI(title="AI Aided Asset Versioning Backend")

setup_logging()
init_db()

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(generation.router)
app.include_router(assets.router)
app.include_router(presets.router)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
