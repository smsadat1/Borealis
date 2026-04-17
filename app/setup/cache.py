import redis.asyncio as redis

from starlette.applications import Starlette

from setup.db import init_db

REDIS_URL = "redis://borealis-redis:6379"

async def lifespan(app: Starlette):

    app.state.redis = redis.from_url(REDIS_URL, decode_responses=True)
    init_db()
    print("DB initialized")

    try:
        await app.state.redis.ping()
        print('Redis connected')
    except Exception as e:
        print('Redis connection failed', e)
        raise e

    yield
    await app.state.redis.close()
    print('Redis conneciton closed')
