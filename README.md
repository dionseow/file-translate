# (In-place File Translation)


This service allows users to upload a file (.docx, .ppt, .pdf, .png or .jpg) and translate the text within the document. After translation is complete, the original text is replaced with the translated text in-place.

## Getting started

1. Define the type of language pair translation to be performed. A good place to start would be looking at the OPUS models in the huggingface repo. Once a model has been selected, place either the huggingface model name or local model directory under the `translater/main.py` script

2. Define the PaddleOCR model engine. This service uses Paddle OCR to perform OCR for images. The english model works decently well on any languages with roman alphabets. You can define the model to use for PaddleOCR under the `api/models` directory if using a local copy or by defining it under the `api/app/core/img.py` script

3. Run `docker-compose up --build` and access the service as `http://localhost:8888/docs`

