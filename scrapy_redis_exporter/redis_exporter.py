import logging
from io import TextIOWrapper
import redis
from scrapy.exceptions import NotConfigured
from scrapy.extensions.feedexport import BlockingFeedStorage, build_storage

logger = logging.getLogger(__name__)



class redisFeedStorage(BlockingFeedStorage):
    def __init__(self, uri, list_key, *, feed_options=None):
        if not list_key:
            raise NotConfigured("Missing redis_list_key")

        if feed_options and feed_options.get("overwrite", True) is False:
            raise NotConfigured(
                "redisFeedStorage does not support appending to files. Please "
                "remove the overwrite option from your FEEDS setting or set it to True."
            )
        self.client = redis.Redis.from_url(uri)
        self.list_key = list_key
        

    @classmethod
    def from_crawler(cls, crawler, uri, *, feed_options=None):
        return build_storage(
            cls,
            uri,
            list_key=crawler.settings.get("REDIS_LIST_KEY"),
            feed_options=feed_options,
        )


    def _store_in_thread(self, file: TextIOWrapper):
        file.seek(0)
        content = file.read()
        res = self.client.rpush(self.list_key, content)
        if not res:
            raise NotConfigured(f"Failed to upload the file to redis: {res}")
        logger.info(f"Feed file uploaded to redis: {self.list_key}")
        file.close()
        self.client.close()
