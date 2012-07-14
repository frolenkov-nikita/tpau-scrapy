from cat_spider import CatSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtracto


class GeneralAdSpider(CatSpider):
    rules = (
        Rule(SgmlLinkExtractor(allow=('AdNumber', ), unique=True),
             callback='parse_item', follow=True),
        )
