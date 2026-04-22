from cachetools import TTLCache
import time 
from collections import defaultdict

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from api.connrpc import auth_client
from rpc import auth_pb2


api_key_cache = TTLCache(maxsize=10_000, ttl=300)  # 5 min cache
rate_store = defaultdict(lambda: {"count": 0, "reset": time.time() + 60})


async def check_rate_limit(api_key, limit):
    bucket = rate_store[api_key]
    now = time.time()

    if now > bucket["reset"]:
        bucket["count"] = 0
        bucket["reset"] = now + 60

    if bucket["count"] >= limit:
        return False

    bucket["count"] += 1
    return True



class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        api_key = request.headers.get('x-api-key')

        if not api_key:
            return JSONResponse({"detail": "Missing API key"}, status_code=401)
        
        # cache hit
        if api_key in api_key_cache:
            request.state.auth = api_key_cache[api_key]
            return await call_next(request)
        
        response = await auth_client.stub.ValidateAPIKey(
            auth_pb2.ValidateRequest(api_key=api_key)
        )

        if not response.valid:
            return JSONResponse({"detail": "Invalid API key"}, status_code=401)

        auth_data = {
            "user_id": response.user_id,
            "rate_limit": response.rate_limit,
        }

        if not await check_rate_limit(api_key=api_key, limit=auth_data['rate_limit']):
            return JSONResponse({"detail": "Rate limit exceeded"}, status_code=429)

        api_key_cache[api_key] = auth_data
        request.state.auth = auth_data
        return await call_next(request)
    

    

