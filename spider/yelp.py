import html
import gzip

import dateutil.parser
import requests
from bs4 import BeautifulSoup

from spider.base_crawler import BaseCrawler


class YelpCrawler(BaseCrawler):

    def crawl_next_batch(self):
        page = 1
        while True:
            blogs = self.crawl_page('https://engineeringblog.yelp.com/page/{}'.format(page)) if page > 1 \
                else self.crawl_page('https://engineeringblog.yelp.com/')
            yield from blogs

            if not blogs:
                break
            page = page + 1

    def crawl_page(self, url):
        response = requests.get(url, headers=self.http_headers())
        if response.status_code != 200:
            return []

        return self.extract_blogs_from_html(response.content.decode('utf-8'))

    def extract_blogs_from_html(self, html):
        soup = BeautifulSoup(html, 'lxml')
        articles = soup.find_all(name='article')
        result = []
        for article in articles:
            blog = {}
            entry_title = article.find(name='h3')
            blog['title'] = entry_title.a.string
            blog['url'] = 'https://engineeringblog.yelp.com/{}'.format(entry_title.a.attrs['href'])

            pub_datetime = article.find(class_='post-date').string
            blog['pub_date'] = dateutil.parser.parse(pub_datetime).date().isoformat()

            entry_image = article.find(class_='column-beta')
            if entry_image and entry_image.find(name='img'):
                blog['cover'] = 'https://engineeringblog.yelp.com/{}'.format(entry_image.find(name='img').attrs['src'])
            else:
                blog['cover'] = self.get_company_logo()

            result.append(blog)

        return result

    @classmethod
    def get_company_name(cls):
        return 'Yelp'
