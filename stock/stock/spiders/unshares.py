import scrapy
import json
import requests


from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from stock.items import StockItem
#from stock.pipelines import DuplicatesPipeline





class TestSpider(scrapy.Spider):
    name = 'unshares'
    start_urls=['https://backend.otcmarkets.com/otcapi/market-data/active/current?tierGroup=PS&page=1&pageSize=50']




    def parse(self, response):
        item = StockItem()
        responsee = response.json()
        rec = responsee["records"]
        page = responsee["pages"]
        for i in range(len(rec)):
            s = rec[i]["symbol"]
            if (0 < len(s) <5 and (rec[i]["price"] < 0.01)):
                item["stock"]=s
                item["price"]=rec[i]["price"]
                yield scrapy.Request(f'https://backend.otcmarkets.com/otcapi/company/profile/full/{s}?symbol={s}', callback=self.parse_un,meta={'item': item,'page':page})
    def parse_un(self,response):
     page=response.meta['page']
     item = response.meta['item']
     responseee=response.json()
     if responseee['securities'][0]['unrestrictedShares']:
      unshares=responseee['securities'][0]['unrestrictedShares']
      if item['price']<0.001 and unshares<8000000000:
       item["unshares"]=unshares
       yield item
      if 0.01<=item['price']<0.002 and unshares<5000000000:
       item["unshares"]=unshares
       yield item
      if 0.02<=item['price']<0.003 and unshares<2000000000:
       item["un"]=unshares
       yield item
      if 0.003<=item['price']<0.004 and unshares<1000000000:
       item["unshares"]=unshares
       yield item
     for i in range(2,page+1):
            yield response.follow(f'https://backend.otcmarkets.com/otcapi/market-data/active/current?tierGroup=PS&page={i}&pageSize=50', callback=self.parse)
     
     