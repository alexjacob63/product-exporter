import json
import os
import pandas as pd

from .models import Product


class FileUploadHandler(object):

    batch_size = 500

    def __init__(self, file_path):
        self.path = file_path
        self.df = pd.read_csv(file_path)

    def remove_duplicates(self):
        self.df.drop_duplicates('sku', inplace=True)

    def save_products(self):
        self.remove_duplicates()
        new_products = len(self.df.index)
        initial_products = Product.objects.count()
        with open('my_status.txt', 'w') as json_file:
            json_data = {'processing': True,
                         'new_products': new_products,
                         'initial_products': initial_products}
            json_file.write(json.dumps(json_data))
        to_save = list()
        for _, row in self.df.iterrows():
            try:
                Product.objects.get(sku=row['sku'])
            except:
                to_save.append(Product(name=row['name'], sku=row['sku'], description=row['description']))
                if len(to_save) > self.batch_size:
                    Product.objects.bulk_create(to_save)
                    to_save = list()
        if to_save:
            Product.objects.bulk_create(to_save)

        os.remove(self.path)
