import os, sys, csv
from datetime import datetime

class DevEventPipeline:
    TODAY = datetime.now().strftime("%y%m%d")
    file_path = os.path.abspath('/opt/airflow/data')

    def open_spider(self, spider):
        os.makedirs(self.file_path, exist_ok=True)
        self.file = open(f'{self.file_path}/event_{self.TODAY}.csv', 'w', newline='', encoding='utf-8')
        field_names = ['title', 'url', 'img_url', 'host', 'period', 'tags']
        self.writer = csv.DictWriter(self.file, fieldnames=field_names)
        self.writer.writeheader()

    def process_item(self, item, spider):
        self.writer.writerow(item)
        return item
    
    def close_spider(self, spider):
        self.file.close()
