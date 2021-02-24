import dateutil.parser
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

from spider.base_crawler import BaseCrawler


class MercariCrawler(BaseCrawler):

    def __init__(self, mongo_client, config_parser):
        super().__init__(mongo_client, config_parser)
        transport = AIOHTTPTransport(url="https://engineering.mercari.com/api/graphql")
        self._graphql_client = Client(transport=transport, fetch_schema_from_transport=True)

    def crawl_next_batch(self):
        offset = 0
        while True:
            result = self.fetch_next_batch(offset)
            if not result:
                return

            yield from result
            offset += len(result)

    def fetch_next_batch(self, offset):
        query = gql(
            """
            query GET_POST($lang: RootQueryToPostConnectionWhereArgsBogoLocales, $searchWord: String, $perPage: Int = 10, $offset: Int = 0, $slug: String) {
                posts(where: {locale: $lang, categoryName: $slug, offsetPagination: {offset: $offset, size: $perPage}, search: $searchWord}) {
                    edges {
                      node {
                        title
                        featuredImage {
                          sourceUrl
                        }
                        date
                        categories {
                          nodes {
                            name
                          }
                        }
                        slug
                        acf {
                          authorfield {
                            userId
                            name
                          }
                        }
                        author {
                          name
                          userId
                        }
                      }
                    }
                  }
                }
            """
        )

        response = self._graphql_client.execute(query, variable_values={'offset': offset, 'lang': "en_US"})
        articles = response['posts']['edges']
        result = []
        for article in articles:
            blog = {
                'title': article['node']['title'],
                'url': 'https://engineering.mercari.com/en/blog/entry/{}'.format(article['node']['slug']),
                'pub_date': dateutil.parser.parse(article['node']['date']).date().isoformat(), 'company': 'Mercari'
            }

            if article['node']['featuredImage']:
                blog['cover'] = article['node']['featuredImage']['sourceUrl']
            else:
                blog['cover'] = self.get_company_logo()

            result.append(blog)

        return result

    @classmethod
    def get_company_name(cls):
        return "Mercari"
