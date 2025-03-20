# Data container file

import scrapy

class SpiderItem(scrapy.Item):
    pass

class VancouverHouseItem(scrapy.Item):
    # Source URL
    source = scrapy.Field()
    # Property Title
    title = scrapy.Field()
    # Main Image
    cover_image = scrapy.Field()
    # Living Area (sq ft)
    living_area = scrapy.Field()
    # List Price (CAD)
    price = scrapy.Field()
    # Listed Date
    listed_date = scrapy.Field()
    # Property Type (House/Condo/Townhouse)
    property_type = scrapy.Field()
    # Number of Beds
    bedrooms = scrapy.Field()
    # Number of Baths
    bathrooms = scrapy.Field()
    # Address
    address = scrapy.Field()
    # Neighborhood
    neighborhood = scrapy.Field()

