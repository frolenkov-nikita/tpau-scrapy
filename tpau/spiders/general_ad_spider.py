import re

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import  Request

from tpau.items import AdItem

class GeneralAdSpider(CrawlSpider):
    name = 'tradingpost_general'
    start_urls = [
        'http://www.tradingpost.com.au/Household/Appliances/Browse',
        'http://www.tradingpost.com.au/DIY-Home-Renovations/Bathroom-Laundry/Browse',
        'http://www.tradingpost.com.au/DIY-Home-Renovations/Tools-Equipment/Browse',
        'http://www.tradingpost.com.au/DIY-Home-Renovations/Kitchens/Browse',
        'http://www.tradingpost.com.au/DIY-Home-Renovations/Building-Materials-Services/Browse',
        'http://www.tradingpost.com.au/Household/Furnishings-and-Home-Decor/Browse',
        'http://www.tradingpost.com.au/Household/Furniture/Browse',
        'http://www.tradingpost.com.au/DIY-Home-Renovations/Building-Materials-Services/Doors-Windows-Awnings/Browse',
        'http://www.tradingpost.com.au/Musical-Instruments-Equipment/Browse',
        'http://www.tradingpost.com.au/Sport-Leisure-Travel/Gymnasium-Equipment/Browse',
        'http://www.tradingpost.com.au/Sport-Leisure-Travel/Bicycles-Cycling-Equipment/Browse',
        'http://www.tradingpost.com.au/Sport-Leisure-Travel/Billiards-Pool-Games-Tables/Browse',
        'http://www.tradingpost.com.au/Sport-Leisure-Travel/Camping-Adventure/Browse',
        'http://www.tradingpost.com.au/Sport-Leisure-Travel/Water-Sports/Browse',

    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('PageNumber', ), unique=True),
             callback='parse_category', follow=True),
        )

    def parse_category(self, response):
        hxs = HtmlXPathSelector(response)
        for url in hxs.select("//div[@class='results ']//a[contains(@class,'megaclick t_productLink')]/@href"):
            yield Request(url.extract(), callback=self.parse_ad)

    def parse_ad(self, response):
        hxs = HtmlXPathSelector(response)
        ad = AdItem()
        ad['uid'] = hxs.select("//div[@class='right' and contains(text(),'Item no')]/text()")[0].extract().split('.')[-1].strip()
        ad['location'] = hxs.select('//h2[@class="ad-number"]/text()').extract()[0]
        ad['title'] = hxs.select('//h1[@class="ad-title"]/text()').extract()[0].strip()

        desc = hxs.select('//*[@class="autoItemDetails"]//text()').extract()
        if desc:
            ad['description'] = desc[0].strip()

        exp = hxs.select("//div[@class='stack']/div[@class='left']/text()").extract()
        if exp:
            ad['expires_on'] = exp[0].split(':')[-1]

        dp = hxs.select("//*[@class='dealerphone']/text()")
        if dp:
            ad['dealerphone'] = dp.extract()[0].strip()

        fs = {
            'additional_information': 'Additional Information'
        }
        for key, name in fs.items():
            table_html = hxs.select("//h3[contains(text(),'%s')]/following-sibling::div[1]" % name)
            if table_html:
                p = {}
                for tr in table_html.select("table/tr"):
                    k = tr.select('th/text()').extract()
                    v = tr.select('td/text()').extract()
                    if k and v:
                        p[k[0].strip()] = v[0].strip()
                if p:
                    ad[key] = p
        ad['images'] = []
        for i in hxs.select("//div[@class='ad-image-thumb']/img/@src"):
            ad['images'].append('http://www.tradingpost.com.au' + i.extract())

        ad['large_images'] = map(lambda s: re.sub(r'\d{2,3}x\d{2,3}', '640x480', s), ad['images'])

        meta = hxs.select('/html/head/meta[@name="X-ISH-SEO"]/@content').extract()[0].strip()
        ad['tp_category_id'] = re.findall(r"ItemCategoryID\s*=\s*'(.*?)'", meta)[0]
        ad['category_id'] = re.findall(r"Taxonomy\/\w+\/\w+\/(\w+)", meta)[0]
        return ad
