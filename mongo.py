import pymongo


class MongoClient:

    def __init__(self, host, port):
        self._client = pymongo.MongoClient(host=host, port=port)
        self._db = self._client.engblog

    def insert_blog(self, blog):
        doc = self._db.blogs.find_one({'url': blog.get('url')})
        if doc is not None:
            return False

        self._db.blogs.insert(blog)
        return True

    def insert_company(self, company):
        self._db.companies.update_one(
            {'company': company},
            {"$set": {'company': company}},
            upsert=True
        )
