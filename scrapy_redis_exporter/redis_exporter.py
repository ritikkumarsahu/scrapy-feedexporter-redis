import logging
from io import TextIOWrapper
import redis
from scrapy.exceptions import NotConfigured, NotSupported
from scrapy.extensions.feedexport import BlockingFeedStorage, build_storage

logger = logging.getLogger(__name__)



class redisFeedStorage(BlockingFeedStorage):
    def __init__(self, uri, list_id, expire_duration, *, feed_options=None):
        if not list_id:
            raise NotConfigured("Missing redis_list_id")

        if feed_options and feed_options.get("overwrite", True) is False:
            raise NotConfigured(
                "redisFeedStorage does not support appending to files. Please "
                "remove the overwrite option from your FEEDS setting or set it to True."
            )
        self.client = redis.Redis.from_url(uri)
        self.list_id = list_id
        self.expire_duration = int(expire_duration) if expire_duration else None
        

    @classmethod
    def from_crawler(cls, crawler, uri, *, feed_options=None):
        return build_storage(
            cls,
            uri,
            list_id=crawler.settings.get("REDIS_LIST_ID"),
            expire_duration=crawler.settings.get("REDIS_EXPIRE_DURATION", 21600), # 6 hours
            feed_options=feed_options,
        )


    def _store_in_thread(self, file: TextIOWrapper):
        file.seek(0)
        content = file.read()
        size = file.tell()/1048576
        if size > 500:
            raise NotSupported(f"File is too large to store in redis {round(size,2)} > 500 MB")
        else:
            res = self.client.rpush(self.list_id, content)
            if self.expire_duration:
                self.client.expire(self.list_id, self.expire_duration)
            if not res:
                raise NotConfigured(f"Failed to upload the file to redis: {res}")
            logger.info(f"Feed file uploaded to redis: {self.list_id}")
        file.close()
        self.client.close()
