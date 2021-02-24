import dateutil.parser
import requests
from bs4 import BeautifulSoup

from spider.base_crawler import BaseCrawler


class TwitterCrawler(BaseCrawler):

    def crawl_next_batch(self):
        page = 1
        while True:
            blogs = self.crawl_page('https://blog.twitter.com/engineering/en_us/_jcr_content/par/nowrap/column/'
                                    'topic-results.{}.html'.format(page))
            yield from blogs

            if not blogs:
                break
            page = page + 1

    def crawl_page(self, url):
        response = requests.get(url, headers=self.http_headers())
        if response.status_code != 200:
            return []

        return self.extract_blogs_from_html(response.text)

    def extract_blogs_from_html(self, html):
        soup = BeautifulSoup(html, 'lxml')
        articles = soup.find_all(class_='result')
        result = []
        for article in articles:
            blog = {}
            entry_title = article.find(class_='result__title')
            blog['title'] = entry_title.string
            blog['url'] = 'https://blog.twitter.com/{}'.format(entry_title.attrs['href'])

            entry_meta = article.find(class_='result__byline')
            pub_datetime = entry_meta.find(name='time').string
            blog['pub_date'] = dateutil.parser.parse(pub_datetime).date().isoformat()
            blog['cover'] = self.get_company_logo()

            result.append(blog)

        return result

    @classmethod
    def get_company_name(cls):
        return 'Twitter'
