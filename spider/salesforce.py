import datetime

import requests

from spider.base_crawler import BaseCrawler


class SalesforceCrawler(BaseCrawler):

    def crawl_next_batch(self):
        offset = None
        while True:
            params = {'to': offset} if offset is not None else {}
            response = requests.get(
                'https://medium.com/salesforce-engineering/load-more?sortBy=tagged&tagSlug=technology', params=params,
                headers=self.rest_api_headers())
            if response.status_code != 200:
                return []

            data = self.extract_medium_api_response(response)
            if not data or not data['references'] or not data['references']['Post']:
                return []

            blog_ids = data['references']['Post'].keys()
            res = []
            for blog_id in blog_ids:
                res.append(self.convert_blog(data['references']['Post'][blog_id]))

            yield from res
            offset = data['paging']['next']['to']

    def convert_blog(self, blog):
        cover = self.get_company_logo()
        if blog['virtuals'] and blog['virtuals']['previewImage'] and blog['virtuals']['previewImage']['imageId']:
            cover = blog['virtuals']['previewImage']['imageId']

        return {
            'title': blog['title'],
            'url': 'https://medium.com/salesforce-engineering/{}'.format(blog['uniqueSlug']),
            'pub_date': datetime.datetime.fromtimestamp(blog['firstPublishedAt'] / 1000).date().isoformat(),
            'cover': 'https://cdn-images-1.medium.com/fit/t/1024/576/{}'.format(cover)
        }

    @classmethod
    def get_company_name(cls):
        return 'Salesforce'
