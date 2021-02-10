from w3lib.html import remove_tags
from scrapy.http import Request
from BaseSpider import BaseSpider


class MitrosSpider(BaseSpider):
    name = "mitrosspider"
    allowed_domains = ["mitrosverkoopt.nl"]

    def parse(self, response):
        page_items = response.css(
            "div.pagination > ul > li.pagination__item.numbers")
        page = int(page_items.css('.pagination__item--active > a::text').get())
        pages = int(page_items[-1:].css('a::text').get())

        cards = response.css("div.card__item")
        for card in cards:
            address = card.css("div.card__inner h5 strong::text").get().lower()
            state = card.css("div.card__overlay h6 strong::text").get().lower()
            price_text = card.css("div.card__overlay p::text").get()
            price = int(''.join(i for i in price_text if i.isdigit()))
            m2_text = card.css("div.card__inner small::text").get()
            m2 = int(''.join(i for i in m2_text if i.isdigit()))
            href = card.css("a::attr(href)").get()
            if state == 'verkocht':
                continue
            if price < 225000 or price > 450000:
                continue
            if m2 <= 60:
                continue
            if not 'wetering' in address and not 'pijlsweer' in address:
                continue
            yield {
                'address': address,
                'state': state,
                'link': href,
                'price': price,
                'm2': m2,
            }

        # If we are not at the last page, go to the next.
        if page < pages:
            next_link = page_items[page].xpath('a[last()]/@href').extract_first()
            next_link = next_link.strip() if next_link else None
            yield Request(
                response.urljoin(next_link),
                callback=self.parse,
            )
