FROM python:3.9

WORKDIR /code

COPY ./deploy/translator/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./translator /code/translator

CMD ["uvicorn", "translator.main:app", "--host", "0.0.0.0", "--port", "80"]