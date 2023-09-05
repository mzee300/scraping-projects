import scrapy
from scrapy.utils import spider

from parse_data import get_maine_inmates, get_arrests_data


# from maine_inmates.items import MaineInmatesItem
# from maine_inmates.models import Base
# from sqlalchemy.orm import sessionmaker


class InmatesSpiderSpider(scrapy.Spider):
    name = 'inmates'
    allowed_domains = ["maine.gov"]
    BASE_URL = 'https://www1.maine.gov/cgi-bin/online/mdoc/search-and-deposit/'
    start_url = BASE_URL + 'search.pl?Search=Continue'

    custom_settings = {
        "ITEM_PIPELINES": {"maine_inmates.maine_inmates.pipelines.DatabasePipeline": 300}
    }

    def start_requests(self):
        yield scrapy.Request(self.start_url, callback=self.parse, dont_filter=True)

    def parse(self, response, **kwargs):
        yield scrapy.Request(
            url=self.BASE_URL + 'search.pl?Search=Continue',
            headers=self.get_headers(),
            body=self.get_search_body(),
            method='POST',
            callback=self.parse_results,
            dont_filter=True,
            meta={'page': 1}
        )

    def parse_results(self, response):
        cookie = response.headers.get('Set-Cookie').decode('utf-8')
        ids = list(dict.fromkeys(response.css('table.at-data-table a::attr(href)').extract()))
        for id in ids:
            yield scrapy.Request(
                url=self.BASE_URL + id,
                headers=self.get_headers(cookie),
                callback=self.parse_inner_pages,
                dont_filter=True,
                meta={'cookie': cookie}
            )

        next_url = response.css('a:contains("Next 30 results")::attr(href)').get()
        if next_url is not None:
            print(f"======================================{next_url}=======================================")
            next_page = response.meta['page'] + 1
            yield scrapy.Request(
                url=self.BASE_URL + next_url,
                headers=self.get_headers(cookie),
                callback=self.parse_results,
                dont_filter=True,
                meta={'page': next_page}
            )
            return
        else:
            print("Scraping Completed")

    def get_headers(self, cookie=None):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': self.BASE_URL,
            'Referer': self.BASE_URL + 'search.pl?Search=Continue'
        }
        if cookie:
            headers['Cookie'] = cookie
        return headers

    @staticmethod
    def get_search_body():
        return 'mdoc_number=&first_name=&middle_name=&last_name=&gender=&age_from=&age_to=&weight_from=&weight_to' \
               '=&feet_from=&inches_from=&feet_to=&inches_to=&eyecolor=&haircolor=&race=&mark=&status=&location' \
               '=&mejis_index=&submit=Search'

    def parse_inner_pages(self, response):
        link = response.url
        item = {
            "inmates_data_hash": get_maine_inmates(response, link),
            "arrests_data_hash": get_arrests_data(response, link)
        }
        yield item
