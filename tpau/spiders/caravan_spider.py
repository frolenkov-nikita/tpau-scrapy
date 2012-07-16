from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from tpau.items import CaravanAdItem
from general_ad_spider import GeneralAdSpider


class CaravanSpider(GeneralAdSpider):
    name = 'caravan'
    start_urls = [
        'http://www.tradingpost.com.au/Automotive/Caravans/CARAVAN/Browse?intref=nav122&OmnSearchType=Browse',
        'http://www.tradingpost.com.au/Automotive/Caravans/POP-TOP/Browse?intref=nav124&OmnSearchType=Browse',
        'http://www.tradingpost.com.au/Automotive/Caravans/CAMPER-TRAILER/Browse?intref=nav125&OmnSearchType=Browse',
        'http://www.tradingpost.com.au/Automotive/Caravans/MOTORHOME/Browse?intref=nav126&OmnSearchType=Browse',
        'http://www.tradingpost.com.au/Automotive/Caravans/CAMPERVAN/Browse?intref=nav127&OmnSearchType=Browse',
        'http://www.tradingpost.com.au/Automotive/Caravans/SLIDE-ON-CAMPER/Browse?intref=nav129&OmnSearchType=Browse',
        'http://www.tradingpost.com.au/Automotive/Wheels-Tyres-Parts-Accessories/Caravan-Accessories/Browse?intref=nav128&OmnSearchType=Browse',
        'http://www.tradingpost.com.au/Automotive/Relocatables/Browse?intref=nav169&OmnSearchType=Browse'
        ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('PageNumber', ), unique=True),
             callback='parse_category', follow=True),
        )



