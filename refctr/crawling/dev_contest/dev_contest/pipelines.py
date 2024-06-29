import os, sys, csv
from datetime import datetime

class DevContestPipeline:
    TODAY = datetime.now().strftime("%y%m%d")
    file_path = os.path.abspath('../../../data')

    def open_spider(self, spider):
        os.makedirs(self.file_path, exist_ok=True)
        # self.file = open(f'/opt/airflow/data/contest_{self.TODAY}.csv', 'w', newline='', encoding='utf-8')
        self.file = open(f'{self.file_path}/contest_{self.TODAY}.csv', 'w', newline='', encoding='utf-8')
        field_names = ['title', 'url', 'img_url', 'status', 'category', 'target', 'host', 'sponsor', 'period', 'd-day', 'total_prize', 'first_prize']
        self.writer = csv.DictWriter(self.file, fieldnames=field_names)
        self.writer.writeheader()

    def process_item(self, item, spider):
        self.writer.writerow(item)
        return item
    
    def close_spider(self, spider):
        self.file.close()