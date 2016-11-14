import scrapy
import re
import os.path
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from craigslist_sample.items import FOXItem
from scrapy.utils.response import body_or_str

class MySpider(CrawlSpider):
    name = "fox"
    allowed_domains = ["foxnews.com"]
    start_urls = ['http://www.foxnews.com']

    base_url = 'http://www.foxnews.com/sitemap.xml'
    label = ['?idx=1','?idx=2','?idx=3','?idx=4','?idx=5','?idx=6',
            '?idx=7','?idx=8','?idx=9','?idx=10','?idx=11','?idx=12',
            '?idx=13','?idx=14','?idx=15','?idx=16','?idx=17','?idx=18',
            '?idx=19','?idx=20','?idx=21','?idx=22','?idx=23','?idx=24',
            '?idx=25','?idx=26','?idx=27','?idx=28','?idx=29']

    def parse(self,response):
        for l in self.label:
            url = self.base_url+l
            yield scrapy.Request(url,self.parseList)

    def parseList(self,response):
        nodename = 'loc'
        text = body_or_str(response)
        r = re.compile(r"(<%s[\s>])(.*?)(</%s>)" % (nodename, nodename), re.DOTALL)
        for match in r.finditer(text):
            url = match.group(2)
            yield scrapy.Request(url,self.parse_items)

    def parse_items(self, response):
        hxs = Selector(response)
        items = []
        item = FOXItem()
        item["title"] = hxs.xpath('//h1[@itemprop="headline"]/text()').extract()[0]
        article = hxs.xpath('//div[@class="article-text"]/p/text()').extract()
        item["article"] = "".join(article).encode('utf8')
        item['link'] = response.url
        items.append(item)
        return(items)