import scrapy
import json
import requests
import numpy as np

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from stock.items import StockItem
#from stock.pipelines import DuplicatesPipeline





class TestSpider(scrapy.Spider):
    name = 'url'
    start_urls=['https://www.otcmarkets.com/research/stock-screener/api?market=20,21,22&page=5&pageSize=100000']




    def parse(self, response):
        item = StockItem()
        responsee = response.text.strip('"').replace('\\"', '"')
        responsee=json.loads(responsee)['stocks']
        #rec = responsee["records"]
        #page = responsee["pages"]
        for i in range(len(responsee)):
            s = responsee[i]["symbol"]
            if (0 < len(s) <5 and (0<responsee[i]["price"] <= 0.06)):
                item["stock"]=f'https://www.otcmarkets.com/otcapi/company/profile/full/{s}?symbol={s}'
               #item["stock"]=s
                price= responsee[i]["price"]
                if price<0.0001:
                  price=0
                item["price"]=price
                yield item
