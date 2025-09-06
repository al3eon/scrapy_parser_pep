from pep_parse.spiders.constants import RESULTS_DIR

BOT_NAME = 'pep_parse'

SPIDER_NAME = 'pep_parse.spiders'
NEWSPIDER_MODULE = SPIDER_NAME
SPIDER_MODULES = [SPIDER_NAME]

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'pep_parse.pipelines.PepParsePipeline': 300,
}

FEEDS = {
    f'{RESULTS_DIR}/pep_%(time)s.csv': {
        'format': 'csv',
        'fields': ['number', 'name', 'status'],
    },
}
