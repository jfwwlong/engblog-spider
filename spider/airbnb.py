import datetime

import requests

from spider.base_crawler import BaseCrawler


class AirbnbCrawler(BaseCrawler):

    def crawl_next_batch(self):
        offset = None
        while True:
            params = {'to': offset} if offset is not None else {}
            response = requests.get('https://medium.com/airbnb-engineering/load-more?sortBy=latest', params=params,
                                    headers=self.rest_api_headers())
            if response.status_code != 200:
                return []

            data = self.extract_medium_api_response(response)
            if not data or not data['value']:
                return []

            blogs = data['value']
            res = []
            for blog in blogs:
                res.append(self.convert_blog(blog))

            yield from res
            offset = data['paging']['next']['to']

    def convert_blog(self, blog):
        return {
            'title': blog['title'],
            'url': 'https://medium.com/airbnb-engineering/{}'.format(blog['uniqueSlug']),
            'pub_date': datetime.datetime.fromtimestamp(blog['firstPublishedAt'] / 1000).date().isoformat(),
            'cover': 'https://cdn-images-1.medium.com/fit/t/1024/576/{}'.format(
                blog['virtuals']['previewImage']['imageId'])
        }

    @classmethod
    def get_company_name(cls):
        return 'Airbnb'
