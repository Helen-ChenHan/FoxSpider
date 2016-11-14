from scrapy.item import Item, Field

class FOXItem(Item):
    title = Field()
    link = Field()
    article = Field()
