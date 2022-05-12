from datetime import timedelta
from dotenv import load_dotenv
import redis
import os

load_dotenv()

# Token expiration
ACCESS_EXPIRES = timedelta(hours=1)

# Blocklist config

jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, password=os.getenv('REDIS_PASSWORD'), decode_responses=True
)
