# redis Feed Storage

[Storage backend](https://docs.scrapy.org/en/latest/topics/feed-exports.html#storage-backends) to store feeds in [Redis](https://redis.io/). 
- URI scheme: `redis`
- Example URI: `redis://user:password@host:port/db`

## Requirements
- Python >= 3.8
- Scrapy >= 2.11.1

## Installation
Install the redis Feed Storage for Scrapy via pip:

```
pip install git+https://github.com/ritikkumarsahu/scrapy-feedexporter-redis
```

## Configuration and Usage
Follow these steps to use the redis Feed Storage with Scrapy:

1. Add this storage backend in your Scrapy project's setting `FEED_STORAGES`, as follows:

```
# settings.py
FEED_STORAGES = {
    'redis': 'scrapy_redis_exporter.redis_exporter.redisFeedStorage'
}
```

2. Set up your Scrapy project's `FEEDS` settings by specifying the URI that contains the connection string to which the feed will be exported on redis:

```python
# settings.py
FEEDS = {
    "redis://connection_uri": {
        "format": "json",
        "overwrite": True  # default
    }
}
```

## Limitations
- The `overwrite` feed option is fixed to `True`, meaning each export will replace the existing file at the specified URI. Use with caution to avoid unintended data loss.
- This storage backend uses [delayed file delivery](https://docs.scrapy.org/en/latest/topics/feed-exports.html#delayed-file-delivery).
