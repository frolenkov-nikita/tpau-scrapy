from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from tpau.items import BoatAdItem
from general_ad_spider import GeneralAdSpider


class BoatSpider(GeneralAdSpider):
    name = 'boat'
    start_urls = [
        'http://www.tradingpost.com.au/Boats/Power-Boats/Browse?intref=nav130&OmnSearchType=Browse',
        'http://www.tradingpost.com.au/Boats/Sail-Boats/Browse?intref=nav131&OmnSearchType=Browse',
        'http://www.tradingpost.com.au/Boats/Jet-Skis/Browse?intref=nav132&OmnSearchType=Browse',
        'http://www.tradingpost.com.au/Boats/Boat-Accessories/Browse?intref=nav133&OmnSearchType=Browse',
        'http://www.tradingpost.com.au/Automotive/Trailers/Boat-Trailer/Browse?intref=nav134&OmnSearchType=Browse',
        'http://www.tradingpost.com.au/Sport-Leisure-Travel/Fishing-Hunting/Browse?intref=nav135&OmnSearchType=Browse',
        'http://www.tradingpost.com.au/Boats/Boat-Accessories/Outboard-Motors-Engines/Browse?intref=nav136&OmnSearchType=Browse',
        'http://www.tradingpost.com.au/Sport-Leisure-Travel/Water-Sports/Browse?intref=nav137&OmnSearchType=Browse',
        ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('PageNumber', ), unique=True),
             callback='parse_category', follow=True),
        )



