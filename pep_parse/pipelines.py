import csv
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from pep_parse.spiders.constants import RESULTS_DIR


class PepParsePipeline:

    def open_spider(self, spider):
        self.count_status = defaultdict(int)
        feeds = spider.settings.get('FEEDS', {})
        self.base_path = RESULTS_DIR
        if feeds:
            feed_path = next(iter(feeds))
            self.base_path = os.path.dirname(str(feed_path))
        Path(self.base_path).mkdir(parents=True, exist_ok=True)

    def process_item(self, item, spider):
        self.count_status[item['status']] += 1
        return item

    def close_spider(self, spider):
        file_name = datetime.now().strftime(
            'status_summary_%Y-%m-%d_%H:%M:%S.csv')
        file_path = Path(self.base_path) / file_name
        data = (
            ('Статус', 'Количество'),
            *sorted(self.count_status.items()),
            ('Total', sum(self.count_status.values()))
        )

        with open(file_path, mode='w', encoding='utf-8') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(data)
