import os
import redis
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# [token expiration]
ACCESS_EXPIRES = timedelta(hours=1)

# [blocklist config]
# [development only]
jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, password='admin123', decode_responses=True
)
