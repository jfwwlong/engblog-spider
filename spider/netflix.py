import requests
import json
import datetime

from spider.base_crawler import BaseCrawler


class NetflixCrawler(BaseCrawler):

    def crawl_next_batch(self):
        paging_next = {}
        while True:
            result, paging = self.fetch_next_batch(paging_next)
            if not result:
                return
            paging_next = paging['next']
            yield from result

    def fetch_next_batch(self, paging_next):
        result = []
        params = {}
        if paging_next.get('to'):
            params = {
                'to': paging_next['to'],
                'page': paging_next['page']
            }

        response = requests.get("https://medium.com/_/api/collections/2615bd06b42e/stream", params=params)
        payload = json.loads(response.content[16:].decode("utf-8"))['payload']

        if not payload or not payload['references'] or not payload['references']['Post'] or not payload['paging']:
            return result, {}

        paging = payload['paging']

        blog_ids = payload['references']['Post'].keys()
        for blog_id in blog_ids:
            blog = payload['references']['Post'][blog_id]
            result.append(self.convert_blog(blog))

        return result, paging

    def convert_blog(self, blog):
        cover = self.get_company_logo()
        if blog['virtuals'] and blog['virtuals']['previewImage'] and blog['virtuals']['previewImage']['imageId']:
            cover = blog['virtuals']['previewImage']['imageId']

        return {
            'pub_date': datetime.datetime.fromtimestamp(blog['firstPublishedAt'] / 1000).date().isoformat(),
            'title': blog['title'],
            'url': 'https://netflixtechblog.com/' + blog['uniqueSlug'],
            'cover': 'https://cdn-images-1.medium.com/fit/t/1024/576/{}'.format(cover)
        }

    @classmethod
    def get_company_name(cls):
        return "Netflix"
