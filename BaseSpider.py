import os
from scrapy.spiders import Spider


class BaseSpider(Spider):
    name = "mainspider"
    custom_settings = {
        'STATUSMAILER_RECIPIENTS': os.getenv('STATUSMAILER_RECIPIENTS'),
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'MAIL_HOST': os.getenv('MAIL_HOST'),
        'MAIL_PORT': os.getenv('MAIL_PORT'),
        'MAIL_USER': os.getenv('MAIL_USER'),
        'MAIL_PASS': os.getenv('MAIL_PASS'),
        'MAIL_FROM': os.getenv('MAIL_FROM'),
        'MAIL_SSL': bool(os.getenv('MAIL_SSL')),
        'EXTENSIONS': {
            'hclib.StatusMailer.StatusMailer': 80
        }
    }

    def __init__(self, start='', *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start]
