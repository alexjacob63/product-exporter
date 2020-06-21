import json
import pandas as pd
from celery import shared_task

from .utils import FileUploadHandler


@shared_task()
def handle_file_upload(file_path):
    df = pd.read_csv(file_path)
    handler = FileUploadHandler(df)
    handler.save_products()
    with open('my_status.txt', 'w') as json_file:
        json_data = {'processing': False}
        json_file.write(json.dumps(json_data))
