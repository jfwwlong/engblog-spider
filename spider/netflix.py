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
        items = payload['streamItems']

        if not items:
            return result, {}

        references = payload['references']['Post']

        paging = payload['paging']

        for item in items:

            blog_references = item['section']['items']
            for reference in blog_references:
                post_id = reference['post']['postId']
                raw_blog_data = references[post_id]
                blog = {
                    'pub_date': datetime.datetime.fromtimestamp(raw_blog_data['createdAt'] / 1000).date().isoformat(),
                    'title': raw_blog_data['title'],
                    'url': 'https://netflixtechblog.com/' + raw_blog_data['uniqueSlug'],
                }

                if raw_blog_data['virtuals'] and raw_blog_data['virtuals']['previewImage'] and \
                        raw_blog_data['virtuals']['previewImage']['imageId']:
                    blog['cover'] = 'https://cdn-images-1.medium.com/max/800/{}'.format(
                        raw_blog_data['virtuals']['previewImage']['imageId'])
                else:
                    blog['cover'] = self.get_company_logo()
                result.append(blog)

        return result, paging

    @classmethod
    def get_company_name(cls):
        return "Netflix"
