from core.doc import WordDocumentProcessor
from core.pdf import PDFProcessor
from core.ppt import PowerPointProcessor
from core.img import ImageProcessor

import os
from celery import Celery

celery = Celery('tasks', broker_url=os.getenv("CELERY_BROKER_URL"), result_backend=os.getenv("CELERY_RESULT_BACKEND"))

word_doc_processor = WordDocumentProcessor()
pdf_processor = PDFProcessor()
ppt_processor = PowerPointProcessor()
img_processor = ImageProcessor()


file_type_to_processor_mapping = {
    "word_doc": word_doc_processor,
    "pdf": pdf_processor,
    "powerpoint": ppt_processor,
    "image": img_processor
}


@celery.task(queue="extract", name="extract_text")
def extract_text(file_path: str | os.PathLike, file_type: str) -> str:
    processor = file_type_to_processor_mapping[file_type]
    extracted_text = processor.extract_text(file_path)
    return extracted_text