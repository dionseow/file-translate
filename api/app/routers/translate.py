import logging

from fastapi import APIRouter
from app.core.celery_app import celery_app
from app.schemas.languages import Languages

logging = logging.getLogger(__name__)

router = APIRouter()

@router.get("/translate")
def translate(text: str, language: Languages) -> str:
    translate_task_result = celery_app.send_task("translate", args=[text, language], queue="translate")
    translated_text = translate_task_result.get()
    return translated_text