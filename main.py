import logging
import os

from config_parser import ConfigParser
from mongo import MongoClient
from spider.base_crawler import BaseCrawler

for module in os.listdir('spider'):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__('spider.' + module[:-3], locals(), globals())
del module

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

if __name__ == "__main__":
    mongo_client = MongoClient('localhost', 27017)
    config_parser = ConfigParser()

    for cls in BaseCrawler.__subclasses__():
        cls(mongo_client, config_parser).crawl_blogs()
