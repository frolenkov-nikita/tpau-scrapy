
from scrapy.item import Item, Field

class CarAdItem(Item):

    url = Field()
    location = Field()
    title = Field()
    description = Field()
    expires_on = Field()
    uid = Field()
    dealerphone = Field()
    standard_features = Field()
    optional_features = Field()
    specifications = Field()
    additional_specifications = Field()
    engine = Field()
    steering_wheels = Field()
    dimensions = Field()
    make = Field()
    model = Field()
    images = Field()
    large_images = Field()
    tp_category_id = Field()
    category_id = Field()


class DogAdItem(Item):
    url = Field()
    location = Field()
    title = Field()
    description = Field()
    expires_on = Field()
    uid = Field()
    dealerphone = Field()
    additional_information = Field()
    model = Field()
    images = Field()
    large_images = Field()
    tp_category_id = Field()
    category_id = Field()

class CatAdItem(DogAdItem):
    pass