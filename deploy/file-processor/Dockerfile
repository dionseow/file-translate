FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y python3-opencv && apt-get -y install tesseract-ocr
COPY ./deploy/file-processor/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

COPY ./models/ocr /app/models

WORKDIR /app

COPY ./file-processor /app