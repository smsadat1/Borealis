import redis.asyncio as redis
from redis.asyncio.client import Redis

from starlette.applications import Starlette


REDIS_URL = "redis://localhost:6379"

async def lifespan(app: Starlette):

    app.state.redis = redis.from_url(REDIS_URL, decode_response=True)
    print('Redis connection established')
    yield
    await app.state.redis.close()
    print('Redis conneciton closed')

async def get_redis() -> Redis:
    return app.state.redis