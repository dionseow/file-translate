import os
import shutil
import logging
import requests

from typing import Union
from pathlib import Path
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse

from app.core.doc import WordDocumentTranslator
from app.core.pdf import PDFTranslator
from app.core.ppt import PowerPointTranslator
from app.core.img import ImageTranslator


logger = logging.getLogger(__name__)

router = APIRouter()

UPLOAD_FOLDER = os.getenv("UPLOAD_PATH")

word_doc_translator = WordDocumentTranslator()
pdf_translator = PDFTranslator()
ppt_translator = PowerPointTranslator()
img_translator = ImageTranslator()


def save_file_to_local(file: File) -> str:
    file_object = file.file
    upload_file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    if not os.path.exists(upload_file_path):
        uploaded_file = open(upload_file_path, "wb+")
        shutil.copyfileobj(file_object, uploaded_file)
        uploaded_file.close()
    return upload_file_path

def translate(text: str) -> str:
    resp = requests.get(f"http://translater:80/translate?source_text={text}")
    return resp.json()


@router.post(
    "/upload-word-doc/",
    summary=("Performs inplace translation for word document"),
)
async def upload_word_doc(file: UploadFile = File(...)) -> FileResponse:
    file_path = save_file_to_local(file)
    file_stem = Path(file_path).stem
    new_file_name = f"{file_stem}_translated.jpg"
    new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
    word_doc_translator.translate_in_place(file_path, new_file_path, translate)
    return FileResponse(new_file_path, filename=new_file_name)


@router.post(
    "/upload-powerpoint/",
    summary=("Performs inplace translation for word document"),
)
async def upload_powerpoint(file: UploadFile = File(...)) -> FileResponse:
    file_path = save_file_to_local(file)
    file_stem = Path(file_path).stem
    new_file_name = f"{file_stem}_translated.jpg"
    new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
    ppt_translator.translate_in_place(file_path, new_file_path, translate)
    return FileResponse(new_file_path, filename=new_file_name)


@router.post(
    "/upload-pdf/",
    summary=("Performs inplace translation for word document"),
)
async def upload_pdf(file: UploadFile = File(...)) -> FileResponse:
    file_path = save_file_to_local(file)
    file_stem = Path(file_path).stem
    new_file_name = f"{file_stem}_translated.jpg"
    new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
    pdf_translator.translate_in_place(file_path, new_file_path, translate)
    return FileResponse(new_file_path, filename=new_file_name)


@router.post(
    "/upload-image/",
    summary=("Performs inplace translation for word document"),
)
async def upload_img(file: UploadFile = File(...)) -> FileResponse:
    file_path = save_file_to_local(file)
    file_stem = Path(file_path).stem
    new_file_name = f"{file_stem}_translated.jpg"
    new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
    img_translator.translate_in_place(file_path, new_file_path, translate)
    return FileResponse(new_file_path, filename=new_file_name)