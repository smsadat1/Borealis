from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from cache import lifespan
from execution import create_execution, list_executions, get_execution, cancel_execution

async def check_borealis(request):
    return JSONResponse(status_code=200, content={"stauts": "ok"})


borealis_routes = [
    Route('/', methods=['GET'], endpoint=check_borealis),
    Route('/executions', methods=['POST'], endpoint=create_execution),
    Route('/executions', methods=['GET'], endpoint=list_executions),
    Route('/executions/{id}', methods=['GET'], endpoint=get_execution),
    Route('/executions/{id}', methods=['DELETE'], endpoint=cancel_execution),
]

Borealis = Starlette(routes=borealis_routes, lifespan=lifespan)