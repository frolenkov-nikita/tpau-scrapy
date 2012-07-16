import re

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import  Request

from tpau.items import MotorbikeAdItem


class MotorbikeAdSpider(CrawlSpider):
    name = 'motorbike'
    start_urls = [
        'http://www.tradingpost.com.au/Automotive/Motorbikes-ATVs/ROAD/Browse?intref=nav034&OmnSearchType=Browse',
        'http://www.tradingpost.com.au/Automotive/Motorbikes-ATVs/ENDURO/Browse?intref=nav035&OmnSearchType=Browse',
        'http://www.tradingpost.com.au/Automotive/Motorbikes-ATVs/MOTORCROSS/Browse?intref=nav036&OmnSearchType=Browse',
        'http://www.tradingpost.com.au/Automotive/Motorbikes-ATVs/TRAIL/Browse?intref=nav037&OmnSearchType=Browse',
        'http://www.tradingpost.com.au/Automotive/Motorbikes-ATVs/FARM-TRAIL/Browse?intref=nav038&OmnSearchType=Browse',
        'http://www.tradingpost.com.au/Automotive/Motorbikes-ATVs/SCOOTER/Browse?intref=nav039&OmnSearchType=Browse',
        'http://www.tradingpost.com.au/Automotive/Motorbikes-ATVs/ATV/Browse?intref=nav040&OmnSearchType=Browse',
        'http://www.tradingpost.com.au/Automotive/Motorbikes-ATVs/DUAL-PURPOSE/Browse?intref=nav041&OmnSearchType=Browse',
        'http://www.tradingpost.com.au/Automotive/Motorbikes-ATVs/MINI-BIKE/Browse?intref=nav042&OmnSearchType=Browse',
        'http://www.tradingpost.com.au/Automotive/Go-Karts-Buggies/Browse?intref=nav043&OmnSearchType=Browse',
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
        ad = MotorbikeAdItem()
        ad['uid'] = hxs.select("//div[@class='stack']/div[@class='right']/text()")[0].extract().split('.')[-1].strip()
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

        f = {
            'standard_features': 'Standard Features',
            'optional_features': 'Optional Features'
        }
        for key, name in f.items():
            table_html = hxs.select("//h4[contains(text(),'%s')]/following-sibling::table" % name)
            if table_html:
                t = []
                for s in table_html.select("tr/td/text()"):

                    s = s.extract().strip()
                    if s:
                        t.append(s)
                if t:
                    ad[key] = t

        fs = {
            'specifications': "Vehicle Details",
            'additional_specifications': "Additional Details",
            'engine': 'Engine',
            'steering_wheels': 'Wheels',
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

        ad['make'] = hxs.select("//ul[@id='breadcrumb']/li[@class='bc-l6']/a/div[@class='bc-butt']/text()").extract()[0].strip()
        ad['model'] = hxs.select("//ul[@id='breadcrumb']/li[@class='bc-l7']/a/div[@class='bc-butt']/text()").extract()[0].strip()
        ad['images'] = []
        for i in hxs.select("//div[@class='ad-image-thumb']/img/@src"):
            ad['images'].append('http://www.tradingpost.com.au' + i.extract())

        ad['large_images'] = map(lambda s: re.sub(r'\d{2,3}x\d{2,3}', '640x480', s), ad['images'])

        meta = hxs.select('/html/head/meta[@name="X-ISH-SEO"]/@content').extract()[0].strip()
        ad['tp_category_id'] = re.findall(r"ItemCategoryID\s*=\s*'(.*?)'", meta)[0]
        ad['category_id'] = re.findall(r"Taxonomy\/\w+\/\w+\/(\w+)", meta)[0]
        return ad


