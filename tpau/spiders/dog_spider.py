from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from general_ad_spider import GeneralAdSpider
from tpau.items import DogAdItem

class DogSpider(GeneralAdSpider):
    name = 'dog'
    start_urls = [
        'http://www.tradingpost.com.au/Pets-Horses/Dogs/Browse'
        ]
    rules = (
        Rule(SgmlLinkExtractor(allow=('PageNumber', ), unique=True),
        callback='parse_category', follow=True),
    )
