import json
from celery import shared_task

from .utils import FileUploadHandler


@shared_task
def add(x, y):
    return x + y


@shared_task()
def handle_file_upload(file_path):
    handler = FileUploadHandler(file_path)
    handler.save_products()
    with open('my_status.txt', 'w') as json_file:
        json_data = {'processing': False}
        json_file.write(json.dumps(json_data))
