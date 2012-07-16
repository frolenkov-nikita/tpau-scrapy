
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


class MotorbikeAdItem(CarAdItem):
    pass


class AdItem(Item):
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


class DogAdItem(AdItem):
    pass


class CatAdItem(AdItem):
    pass


class CaravanAdItem(AdItem):
    pass


class BoatAdItem(AdItem):
    pass


class TruckAdItem(CarAdItem):
    pass


class FarmItem(AdItem):
    pass


class TrailerItem(AdItem):
    pass


class CommercialItem(AdItem):
    pass