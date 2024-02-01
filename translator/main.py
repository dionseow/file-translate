import os
from typing import Union
from fastapi import FastAPI
from transformers import pipeline
from celery import Celery
from schemas.languages import Languages

translator = pipeline("translation", model="/code/translator/id-en")

celery = Celery("tasks",
                broker=os.getenv("CELERY_BROKER_URL"),
                backend=os.getenv("CELERY_RESULT_BACKEND"))

@celery.task(name="translate", queue="translate")
def translate_text(text: str, language: Languages) -> str:
    return translator(source_text[0]['translation_text'])