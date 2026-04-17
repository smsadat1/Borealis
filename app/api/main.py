from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, WebSocketRoute

from setup.cache import lifespan
from api.execution import create_execution, list_executions, get_execution, cancel_execution
from api.middleware import APIKeyMiddleware
from api.ws import borealis_ws_stream


async def check_borealis(request):
    return JSONResponse(status_code=200, content={"stauts": "ok"})

borealis_routes = [
    Route('/', methods=['GET'], endpoint=check_borealis),
    Route('/executions', methods=['POST'], endpoint=create_execution),
    Route('/executions', methods=['GET'], endpoint=list_executions),
    Route('/executions/{exec_id}', methods=['GET'], endpoint=get_execution),
    Route('/executions/{exec_id}', methods=['DELETE'], endpoint=cancel_execution),
    WebSocketRoute('/executions/{exec_id}/stream', endpoint=borealis_ws_stream),
]

Borealis = Starlette(routes=borealis_routes, lifespan=lifespan)
Borealis.add_middleware(APIKeyMiddleware)