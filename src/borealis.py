from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

async def check_borealis(request):
    return JSONResponse(status_code=200, content={"stauts": "ok"})

async def create_execution(request):
    
    data = await request.json()

    return JSONResponse(status_code=200, content={"id": "123", "status": "queued"})

async def list_executions(request):
    
    return JSONResponse(status_code=200, content={"executions": []})


async def get_execution(request):
    
    exec_id = request.path_params['id']

    return JSONResponse(
        status_code=200,
        content={
            "id": exec_id,
            "status": "completed",
            "stdout": "...",
        }
    )

async def cancel_execution(request):
    
    exec_id = request.path_params['id']

    return JSONResponse(status_code=200, content={"id": exec_id, "status": "cancelled"})



borealis_routes = [
    Route('/', methods=['GET'], endpoint=check_borealis),
    Route('/executions', methods=['POST'], endpoint=create_execution),
    Route('/executions', methods=['GET'], endpoint=list_executions),
    Route('/executions/{id}', methods=['GET'], endpoint=get_execution),
    Route('/executions/{id}', methods=['DELETE'], endpoint=cancel_execution),
]

Borealis = Starlette(routes=borealis_routes)