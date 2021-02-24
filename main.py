import logging

from config_parser import ConfigParser
from mongo import MongoClient
from spider.indeed import IndeedCrawler
from spider.mercari import MercariCrawler

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

if __name__ == "__main__":
    mongo_client = MongoClient('localhost', 27017)
    config_parser = ConfigParser()

    indeedCrawler = IndeedCrawler(mongo_client, config_parser)
    indeedCrawler.crawl_blogs()
    logger.info("Finished crawling %s", indeedCrawler.get_company_name())

    mercariCrawler = MercariCrawler(mongo_client, config_parser)
    mercariCrawler.crawl_blogs()
    logger.info("Finished crawling %s", mercariCrawler.get_company_name())
