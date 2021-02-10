import os
from scrapy.spiders import Spider


class BaseSpider(Spider):
    name = "mainspider"
    custom_settings = {
        'STATUSMAILER_RECIPIENTS': os.getenv('STATUSMAILER_RECIPIENTS'),
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'EXTENSIONS': {
            'hclib.StatusMailer.StatusMailer': 80
        }
    }

    def __init__(self, start='', *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start]
