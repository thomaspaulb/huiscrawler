import gzip
import datetime

from scrapy import signals
from scrapy.mail import MailSender
from scrapy.exceptions import NotConfigured
from scrapy.utils.serialize import ScrapyJSONEncoder

from collections import defaultdict

from io import StringIO


class StatusMailer(object):
    def __init__(self, recipients, mail, crawler):
        self.recipients = recipients
        self.mail = mail
        self.num_items = 0
        self.num_errors = 0

    @classmethod
    def from_crawler(cls, crawler):
        recipients = crawler.settings.getlist('STATUSMAILER_RECIPIENTS')
        if not recipients:
            raise NotConfigured

        mail = MailSender.from_settings(crawler.settings)
        instance = cls(recipients, mail, crawler)

        crawler.signals.connect(instance.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(instance.spider_closed, signal=signals.spider_closed)

        return instance

    def item_scraped(self, item, response, spider):
        self.num_items += 1

    def spider_closed(self, spider, reason):
        body='''Crawl statistics:

 - Spider name: {0}
 - Spider finished at: {1}
 - Number of items scraped: {2}
 - Number of errors: {3}'''.format(
            spider.name,
            datetime.datetime.now(),
            self.num_items,
            self.num_errors,
        )
        print (body)
        return self.mail.send(
            to=self.recipients,
            subject='Crawler for %s: %s' % (spider.name, reason),
            body=body,
        )
