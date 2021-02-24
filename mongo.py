import pymongo


class MongoClient:

    def __init__(self, host, port):
        self._client = pymongo.MongoClient(host=host, port=port)
        self._db = self._client.engblog
        self._blogs = self._db.blogs

    def insert_blog(self, blog):
        doc = self._blogs.find_one({'url': blog.get('url')})
        if doc is not None:
            return False

        self._blogs.insert(blog)
        return True
