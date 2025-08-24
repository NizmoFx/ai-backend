from celery import Celery
import os
from ..config import settings

celery_app = Celery(
    "worker",
    broker=settings.rabbitmq_url,
    backend=os.getenv("CELERY_BACKEND", "rpc://")
)

celery_app.conf.task_routes = {"app.tasks.tasks.*": {"queue": "generation"}}
