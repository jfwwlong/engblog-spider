import dateutil.parser
import requests
from bs4 import BeautifulSoup

from spider.base_crawler import BaseCrawler


class DropboxCrawler(BaseCrawler):

    def crawl_next_batch(self):
        sub_category_urls = self.get_sub_category_urls()

        for sub_category_url in sub_category_urls:
            blogs = self.crawl_page(sub_category_url)
            yield from blogs

    def get_sub_category_urls(self):
        response = requests.get('https://dropbox.tech/', headers=self.http_headers())
        if response.status_code != 200:
            raise Exception("Cannot crawl Dropbox blog categories")

        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        return [a.attrs['href'] for a in soup.find_all(class_='dr-pill--primary')]

    def crawl_page(self, url):
        response = requests.get(url, headers=self.http_headers())
        if response.status_code != 200:
            return []

        return self.extract_blogs_from_html(response.text)

    def extract_blogs_from_html(self, html):
        soup = BeautifulSoup(html, 'lxml')
        container = soup.find(name='main')
        articles = container.select('.article-section')[1].select('li')
        result = []
        for article in articles:
            blog = {}
            entry_title = article.find(name='a')
            blog['title'] = entry_title.span.string
            blog['url'] = entry_title.attrs['href']

            pub_datetime = article.find(attrs={'data-element-id': 'article-date'}).string
            blog['pub_date'] = dateutil.parser.parse(pub_datetime).date().isoformat()
            blog['cover'] = self.get_company_logo()

            result.append(blog)

        return result

    @classmethod
    def get_company_name(cls):
        return 'Dropbox'
