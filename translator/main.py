from typing import Union
from fastapi import FastAPI
from transformers import pipeline

translator = pipeline("translation", model="/code/translator/id-en")

app = FastAPI()

@app.get("/translate")
def translate_sentence(source_text: str):
    return translator(source_text)[0]["translation_text"]