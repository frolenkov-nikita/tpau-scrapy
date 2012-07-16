import os

BOT_NAME = 'tpau'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['tpau.spiders']
NEWSPIDER_MODULE = 'tpau.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = ['tpau.pipelines.PrintPipeline']

COOKIES_ENABLED = True
CRAWLSPIDER_FOLLOW_LINKS = True

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
OUTPUT_DIR = os.path.join(os.path.expanduser('~'), 'workstuff', 'ads')