# server.py
import json

from klein import route, run
from scrapy import signals
from scrapy.crawler import CrawlerRunner
import request 

from walmart.spiders.walmart import WalmartSpider


class MyCrawlerRunner(CrawlerRunner):
    """
    Crawler object that collects items and returns output after finishing crawl.
    """
    def crawl(self, crawler_or_spidercls, *args, **kwargs):
        # keep all items scraped
        self.items = []

        # create crawler (Same as in base CrawlerProcess)
        crawler = self.create_crawler(WalmartSpider)

        # handle each item scraped
        crawler.signals.connect(self.item_scraped, signals.item_scraped)

        # create Twisted.Deferred launching crawl
        dfd = self._crawl(crawler, *args, **kwargs)

        # add callback - when crawl is done cal return_items
        dfd.addCallback(self.return_items)
        return dfd

    def item_scraped(self, item, response, spider):
        self.items.append(item)

    def return_items(self, result):
        return self.items


def return_spider_output(output):
    """
    :param output: items scraped by CrawlerRunner
    :return: json with list of items
    """
    # this just turns items into dictionaries
    # you may want to use Scrapy JSON serializer here
    return json.dumps([dict(item) for item in output])




@route("/",methods=['POST'])

def schedule(request,product,brand):
    runner = MyCrawlerRunner()
    spider = WalmartSpider()
    deferred = runner.crawl(spider,product=product,brand=brand)
    deferred.addCallback(return_spider_output)
    return deferred
        
    
    


run("localhost",5000)
