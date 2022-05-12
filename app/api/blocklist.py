from datetime import timedelta
from dotenv import load_dotenv
import redis
import os

load_dotenv()

# Token expiration
ACCESS_EXPIRES = timedelta(hours=1)

# Blocklist config

jwt_redis_blocklist = redis.StrictRedis.from_url(
    url=os.getenv('REDIS_URL'), decode_responses=True
)

# Development only
# jwt_redis_blocklist = redis.StrictRedis(
#     host="localhost", port=6379, password='admin123', decode_responses=True
# )
