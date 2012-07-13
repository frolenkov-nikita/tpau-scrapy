# Scrapy settings for tpau project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'tpau'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['tpau.spiders']
NEWSPIDER_MODULE = 'tpau.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = ['tpau.pipelines.PrintPipeline']

COOKIES_ENABLED = True
CRAWLSPIDER_FOLLOW_LINKS = True