import dateutil.parser
import requests
from bs4 import BeautifulSoup

from spider.base_crawler import BaseCrawler


class UberCrawler(BaseCrawler):

    def crawl_next_batch(self):
        page = 1
        while True:
            blogs = self.crawl_page('https://eng.uber.com/page/{}'.format(page))
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
        main_container = soup.find(class_='td-ss-main-content')
        articles = main_container.find_all(class_='item-details')
        result = []
        for article in articles:
            blog = {}
            entry_title = article.find(class_='entry-title')
            blog['title'] = entry_title.string
            blog['url'] = entry_title.a.attrs['href']

            entry_meta = article.find(class_='td-module-meta-info')
            pub_datetime = entry_meta.find(name='time').attrs['datetime']
            blog['pub_date'] = dateutil.parser.parse(pub_datetime).date().isoformat()

            entry_image = article.find(class_='td-module-thumb')
            if entry_image:
                blog['cover'] = entry_image.find(name='img').attrs['data-img-url']
            else:
                blog['cover'] = self.get_company_logo()

            result.append(blog)

        return result

    @classmethod
    def get_company_name(cls):
        return 'Uber'
