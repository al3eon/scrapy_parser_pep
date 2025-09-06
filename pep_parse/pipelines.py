import csv
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path


class PepParsePipeline:

    def open_spider(self, spider):
        self.count_status = defaultdict(int)
        self.settings = spider.settings
        self.base_path = None
        if self.settings.get('FEEDS'):
            for feed_path in self.settings.get('FEEDS', {}).keys():
                feed_path_str = str(feed_path)
                if '%(time)s' in feed_path_str:
                    self.base_path = os.path.dirname(feed_path_str)
                    break
        if not self.base_path:
            self.base_path = 'results'
        Path(self.base_path).mkdir(parents=True, exist_ok=True)

    def process_item(self, item, spider):
        self.count_status[item['status']] += 1
        return item

    def close_spider(self, spider):
        file_name = datetime.now().strftime(
            'status_summary_%Y-%m-%d_%H:%M:%S.csv')
        file_path = Path(self.base_path) / file_name

        with open(file_path, mode='w', encoding='utf-8') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(['Статус', 'Количество'])
            for status, count in self.count_status.items():
                writer.writerow([status, count])

            total = sum(self.count_status.values())
            writer.writerow(['Total', total])
