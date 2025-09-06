import csv
import os
from datetime import datetime
from pathlib import Path

from itemadapter import ItemAdapter

from tests.test_files import BASE_DIR


class PepParsePipeline:

    def open_spider(self, spider):
        self.count_status = {}
        BASE_DIR = Path(__file__).parent.parent
        RESULTS_DIR = BASE_DIR / 'results'
        RESULTS_DIR.mkdir(exist_ok=True)

    def process_item(self, item, spider):
        if item['status'] in self.count_status:
            self.count_status[item['status']] += 1
        else:
            self.count_status[item['status']] = 1

        return item

    def close_spider(self, spider):
        BASE_DIR = Path(__file__).parent.parent
        RESULTS_DIR = BASE_DIR / 'results'
        RESULTS_DIR.mkdir(exist_ok=True)
        file_name = datetime.now().strftime('status_summary_%Y-%m-%d_%H:%M:%S.csv')
        file_path = RESULTS_DIR / file_name

        with open(file_path, mode='w', encoding='utf-8') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(['Статус', 'Количество'])
            for status, count in self.count_status.items():
                writer.writerow([status, count])
            total = sum(self.count_status.values())
            writer.writerow(['Total', total])

