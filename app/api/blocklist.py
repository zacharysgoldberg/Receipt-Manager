from datetime import timedelta
from dotenv import load_dotenv
import redis
import os

load_dotenv()

# Token expiration
ACCESS_EXPIRES = timedelta(hours=1)

# Blocklist config

jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, password='admin123', decode_responses=True
)

# jwt_redis_blocklist = redis.StrictRedis.from_url(
#     url='rediss://', decode_responses=True
# )
