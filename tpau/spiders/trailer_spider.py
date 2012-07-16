from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from tpau.items import TrailerItem
from general_ad_spider import GeneralAdSpider


class TrailerSpider(GeneralAdSpider):
    name = 'trailer'
    start_urls = [
        'http://www.tradingpost.com.au/Automotive/Trailers/BIKE-TRAILER/Browse?intref=nav142&OmnSearchType=Browse'
        ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('PageNumber', ), unique=True),
             callback='parse_category', follow=True),
        )

