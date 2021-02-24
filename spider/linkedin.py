import dateutil.parser
import requests
from bs4 import BeautifulSoup

from spider.base_crawler import BaseCrawler


class LinkedInCrawler(BaseCrawler):

    def crawl_next_batch(self):
        page = 1
        while True:
            blogs = self.crawl_page('https://engineering.linkedin.com/blog?page={}'.format(page))
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
        main_container = soup.find(class_='post-list')
        articles = main_container.find_all(class_='post-li')
        result = []
        for article in articles:
            blog = {}
            entry_post = article.find(class_='post')
            entry_header = entry_post.find(class_='header')
            blog['title'] = entry_header.a.string
            blog['url'] = 'https://engineering.linkedin.com/{}'.format(entry_header.a.attrs['href'])

            pub_datetime = entry_header.find(class_='sub-heading').find(class_='timestamp').string
            blog['pub_date'] = dateutil.parser.parse(pub_datetime).date().isoformat()

            entry_image = article.find(class_='post-thumb')
            if entry_image:
                blog['cover'] = 'https://engineering.linkedin.com/{}'.format(entry_image.a.img.attrs['data-background-src'])
            else:
                blog['cover'] = self.get_company_logo()

            result.append(blog)

        return result

    @classmethod
    def get_company_name(cls):
        return 'LinkedIn'
