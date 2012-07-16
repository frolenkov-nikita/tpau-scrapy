from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from tpau.items import CommercialItem
from general_ad_spider import GeneralAdSpider


class CommercialSpider(GeneralAdSpider):
    name = 'commercial'
    start_urls = [
        'http://www.tradingpost.com.au/Business-Office/Business/Business-Shop-Equipment/Browse?intref=nav091&OmnSearchType=Browse',
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('PageNumber', ), unique=True),
             callback='parse_category', follow=True),
        )

