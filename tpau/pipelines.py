import json
import os


class PrintPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'tradingpost_car':
            f = open('/home/nikita/workstuff/ads/car/%s.json' % item['uid'], 'w+')
        elif spider.name == 'tradingpost_dog':
            f = open('/home/nikita/workstuff/ads/dog/%s.json' % item['uid'], 'w+')
        elif spider.name == 'tradingpost_cat':
            f = open('/home/nikita/workstuff/ads/cat/%s.json' % item['uid'], 'w+')
        else:
            dir = '/home/nikita/workstuff/ads/%s/' % item['tp_category_id']
            if not os.path.exists(dir):
                os.makedirs(dir)
            f = open('/home/nikita/workstuff/ads/%s/%s.json' % (item['tp_category_id'], item['uid']), 'w+')
        f.write(json.dumps(dict(item)))
        f.close()
