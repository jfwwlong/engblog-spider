import logging

from config_parser import ConfigParser
from mongo import MongoClient
from spider.Datadog import DatadogCrawler
from spider.Instagram import InstagramCrawler
from spider.dropbox import DropboxCrawler
from spider.indeed import IndeedCrawler
from spider.linkedin import LinkedInCrawler
from spider.mercari import MercariCrawler
from spider.twitter import TwitterCrawler
from spider.uber import UberCrawler
from spider.netflix import NetflixCrawler
from spider.airbnb import AirbnbCrawler
from spider.pinterest import PinterestCrawler

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

if __name__ == "__main__":
    mongo_client = MongoClient('localhost', 27017)
    config_parser = ConfigParser()

    instagram_crawler = DatadogCrawler(mongo_client, config_parser)
    instagram_crawler.crawl_blogs()
    logger.info("Finished crawling %s", instagram_crawler.get_company_name())

    # indeedCrawler = IndeedCrawler(mongo_client, config_parser)
    # indeedCrawler.crawl_blogs()
    # logger.info("Finished crawling %s", indeedCrawler.get_company_name())
    #
    # mercariCrawler = MercariCrawler(mongo_client, config_parser)
    # mercariCrawler.crawl_blogs()
    # logger.info("Finished crawling %s", mercariCrawler.get_company_name())
    #
    # netflix_crawler = NetflixCrawler(mongo_client, config_parser)
    # netflix_crawler.crawl_blogs()
    # logger.info("Finished crawling %s", netflix_crawler.get_company_name())
    #
    # airbnb_crawler = AirbnbCrawler(mongo_client, config_parser)
    # airbnb_crawler.crawl_blogs()
    # logger.info("Finished crawling %s", airbnb_crawler.get_company_name())

    # pinterest_crawler = PinterestCrawler(mongo_client, config_parser)
    # pinterest_crawler.crawl_blogs()
    # logger.info("Finished crawling %s", pinterest_crawler.get_company_name())

