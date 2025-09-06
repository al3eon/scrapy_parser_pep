import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        tr = response.css('table.pep-zero-table.docutils'
                          '.align-default tbody tr')
        for row in tr:
            number = row.xpath('td[2]/a/text()').get()
            name = row.xpath('td[3]/a/text()').get()
            link = row.xpath('td[2]/a/@href').get()
            yield response.follow(
                link,
                callback=self.parse_pep,
                meta={'number': number, 'name': name}
            )

    def parse_pep(self, response):
        data = {
            'number': response.meta['number'],
            'name': response.meta['name'],
            'status': response.css(
                'section#pep-content dl dt:contains("Status:") + dd abbr::text'
            ).get()
        }
        yield PepParseItem(data)
