FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y python3-opencv
COPY ./deploy/api/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

WORKDIR /app

COPY ./api/app /app/app
COPY ./api/models /app/models

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]