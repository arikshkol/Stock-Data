import scrapy
import json
import requests

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from stock.items import StockItem


# from stock.pipelines import DuplicatesPipeline


class TestSpider(scrapy.Spider):
    name = 'symbol'
    start_urls = ['https://www.otcmarkets.com/research/stock-screener/api?market=20,21,22&page=5&pageSize=100000']

    def parse(self, response):
        item = StockItem()
        responsee = response.text.strip('"').replace('\\"', '"')
        responsee=json.loads(responsee)['stocks']
        #rec = responsee["records"]
        #page = responsee["pages"]
        for i in range(len(responsee)):
            s = responsee[i]["symbol"]
            if (0 < len(s) < 5 and (0.001 >= responsee[i]["price"]>0)):
                item["stock"] = s
                price= responsee[i]["price"]
                if price<0.0001:
                  price=0
                item["price"]=price
                yield item
