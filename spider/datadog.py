import dateutil.parser
import requests
from bs4 import BeautifulSoup

from spider.base_crawler import BaseCrawler


class DatadogCrawler(BaseCrawler):

    def crawl_next_batch(self):
        return self.crawl_page('https://www.datadoghq.com/blog/engineering/')

    def crawl_page(self, url):
        response = requests.get(url, headers=self.http_headers())
        if response.status_code != 200:
            return []

        return self.extract_blogs_from_html(response.text)

    def extract_blogs_from_html(self, html):
        soup = BeautifulSoup(html, 'lxml')
        container = soup.find(class_='container posts')
        articles = container.find(class_='row').children
        result = []
        for article in articles:
            blog = {'title': article.find(class_='regular-post-text').h4.string, 'url': article.a.attrs['href']}

            pub_date = self.extract_pub_date_from_blog(blog['url'])
            blog['pub_date'] = dateutil.parser.parse(pub_date).date().isoformat()
            blog['cover'] = article.find(name='picture').img.attrs['base-img']

            result.append(blog)

        return result

    def extract_pub_date_from_blog(self, blog_url):
        response = requests.get(blog_url, headers=self.http_headers())
        if response.status_code != 200:
            raise Exception("Cannot open blog for Datadog")

        html = response.text
        return BeautifulSoup(html, 'lxml').find(class_='header-meta').p.string.replace('Published: ', '')

    @classmethod
    def get_company_name(cls):
        return 'Datadog'
