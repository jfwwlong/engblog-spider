import logging
import json

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)


class BaseCrawler:

    def __init__(self, mongo_client, config_parser):
        self._mongo_client = mongo_client
        self._config_parser = config_parser

    def persist(self, blog):
        return self._mongo_client.insert_blog(blog)

    def get_company_logo(self):
        return self._config_parser.get_company_logo(self.get_company_name())

    def get_company_icon(self):
        return self._config_parser.get_company_icon(self.get_company_name())

    def crawl_blogs(self):
        count = 0
        for blog in self.crawl_next_batch():
            blog['company'] = self.get_company_name()
            blog['companyIcon'] = self.get_company_icon()

            if not self.persist(blog):
                return

            count += 1
            logger.info('Crawled and persisted %s blogs into database for: %s', count, self.get_company_name())

    def crawl_next_batch(self):
        raise NotImplemented

    @classmethod
    def get_company_name(cls):
        raise NotImplemented

    @staticmethod
    def http_headers():
        return {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/52.0.2743.116 Safari/537.36 '
        }

    @staticmethod
    def rest_api_headers():
        return {
            'Accept': 'application/json'
        }

    @staticmethod
    def extract_medium_api_response(response):
        return json.loads(response.content[16:].decode("utf-8"))['payload']
