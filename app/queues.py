import os
import redis
from rq import Queue

REDIS_URL = os.getenv("REDIS_URL")

redis_conn = redis.from_url(REDIS_URL)
default_queue = Queue("default", connection=redis_conn)
