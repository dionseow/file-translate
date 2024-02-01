import os
import shutil
import logging
from typing import Union
from pathlib import Path
from fastapi import APIRouter, UploadFile, File

from app.core.celery_app import celery_app

logger = logging.getLogger(__name__)

router = APIRouter()

UPLOAD_FOLDER = os.getenv("UPLOAD_PATH")

def save_file_to_local(file: File) -> str:
    file_object = file.file
    upload_file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    if not os.path.exists(upload_file_path):
        uploaded_file = open(upload_file_path, "wb+")
        shutil.copyfileobj(file_object, uploaded_file)
        uploaded_file.close()
    return upload_file_path

@router.post(
    "/extract-text-word-doc"
)
async def extract_text_word_doc(file: UploadFile = File(...)) -> str:
    file_path = save_file_to_local(file)
    extract_task = celery_app.send_task("extract_text", args=[file_path, "word_doc"], queue="extract")
    extracted_text = extract_task.get()
    return extracted_text


@router.post(
    "/extract-text-powerpoint"
)
async def extract_text_powerpoint(file: UploadFile = File(...)) -> str:
    file_path = save_file_to_local(file)
    extract_task = celery_app.send_task("extract_text", args=[file_path, "powerpoint"], queue="extract")
    extracted_text = extract_task.get()
    return extracted_text

@router.post(
    "/extract-text-pdf"
)
async def upload_word_doc(file: UploadFile = File(...)) -> str:
    file_path = save_file_to_local(file)
    extract_task = celery_app.send_task("extract_text", args=[file_path, "pdf"], queue="extract")
    extracted_text = extract_task.get()
    return extracted_text

@router.post(
    "/extract-text-image"
)
async def upload_word_doc(file: UploadFile = File(...)) -> str:
    file_path = save_file_to_local(file)
    extract_task = celery_app.send_task("extract_text", args=[file_path, "image"], queue="extract")
    extracted_text = extract_task.get()
    return extracted_text