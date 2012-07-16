import json
import os

from scrapy.conf import settings


class PrintPipeline(object):
    def process_item(self, item, spider):
        file_name = '%s.json' % item['uid']
        dir = os.path.join(settings.OUTPUT_DIR, spider.name, item['tp_category_id'])
        if not os.path.exists(dir):
            os.makedirs(dir)
        f = open(os.path.join(dir, file_name), 'w+')
        f.write(json.dumps(dict(item)))
        f.close()
