import os
from celery import Celery

celery_app = Celery('tasks', broker_url=os.getenv("CELERY_BROKER_URL"), result_backend=os.getenv("CELERY_RESULT_BACKEND"))