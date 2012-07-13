import re

from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import  Request

from tpau.items import CarAdItem

class CarSpider(BaseSpider):
    name = 'tradingpost_car'
    start_urls = [
        'http://www.tradingpost.com.au/is-bin/INTERSHOP.enfinity/WFS/Telstra-TradingPost-Site/en_AU/-/AUD/ViewListingSelectCategory-Continue?CatalogCategoryPath=Automotive/Used-Cars',
        'http://www.tradingpost.com.au/Automotive/Used-Cars/Browse']
    for i in range(0, 3500):
        start_urls.append('http://www.tradingpost.com.au/Automotive/Used-Cars/Browse?PageNumber=%s' % i)

#    rules = (
#       Rule(SgmlLinkExtractor(allow=('AdNumber', ), unique=True),
#            callback='parse_item', follow=True),
#    )

    def parse(self, response):
       # print response.body
        hxs = HtmlXPathSelector(response)
        for url in hxs.select("//div[@class='results ']//a[contains(@class,'megaclick t_productLink')]/@href"):
            yield Request(url.extract(), callback=self.parse_ad)

    def parse_ad(self, response):
        hxs = HtmlXPathSelector(response)
        ad = CarAdItem()
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
            'specifications': "Specifications",
            'additional_specifications': "Additional Specifications",
            'engine': 'Engine',
            'steering_wheels': 'Steering & Wheels',
            'dimensions': 'Dimensions'
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

