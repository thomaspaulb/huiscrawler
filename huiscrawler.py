from scrapy.crawler import CrawlerProcess

from MitrosSpider import MitrosSpider


process = CrawlerProcess()


def run():
    process.crawl(MitrosSpider, "https://www.mitrosverkoopt.nl/koopaanbod?&city%5B%5D=Utrecht&ccm_paging_p=1")
    process.start()


if __name__ == "__main__":
    run()
