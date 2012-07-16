from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from tpau.items import FarmItem
from general_ad_spider import GeneralAdSpider


class FarmSpider(GeneralAdSpider):
    name = 'farm'
    start_urls = [
        'http://www.tradingpost.com.au/Rural-Machinery/Machinery/Browse'
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('PageNumber', ), unique=True),
             callback='parse_category', follow=True),
        )

