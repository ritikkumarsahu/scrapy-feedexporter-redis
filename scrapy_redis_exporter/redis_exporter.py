import logging
from io import TextIOWrapper
import redis
from scrapy.exceptions import NotConfigured
from scrapy.extensions.feedexport import BlockingFeedStorage, build_storage

logger = logging.getLogger(__name__)



class redisFeedStorage(BlockingFeedStorage):
    def __init__(self, uri, list_id=None, *, feed_options=None):
        if not list_id:
            raise NotConfigured("Missing redis_list_id")

        if feed_options and feed_options.get("overwrite", True) is False:
            raise NotConfigured(
                "redisFeedStorage does not support appending to files. Please "
                "remove the overwrite option from your FEEDS setting or set it to True."
            )
        self.client = redis.Redis.from_url(uri)
        self.list_id = list_id
        

    @classmethod
    def from_crawler(cls, crawler, uri, *, feed_options=None):
        return build_storage(
            cls,
            uri,
            list_id=crawler.settings.get("redis_list_id"),
            feed_options=feed_options,
        )


    def _store_in_thread(self, file: TextIOWrapper):
        file.seek(0)
        content = file.read()
        res = self.client.rpush(self.list_id, content)
        if not res:
            raise NotConfigured(f"Failed to upload the file to redis: {res}")
        logger.info(f"Feed file uploaded to redis: {self.list_id}")
        file.close()
        self.client.close()
