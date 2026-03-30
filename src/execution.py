import asyncio
import uuid

from starlette.responses import JSONResponse

from compiler import run_borealis
from vars import jobs

async def create_execution(request):
    
    form = await request.form()
    language = form['language']
    file = form['file']
    src_code = (await file.read()).decode('utf-8')

    exec_id = str(uuid.uuid4())

    jobs[exec_id] = {
        "status": "queued",
        "stdout": None,
        "stderr": None,
        "exit_code": None
    }

    asyncio.create_task(run_borealis(exec_id=exec_id, lang=language, src_code=src_code))

    return JSONResponse(status_code=200, content={"id": exec_id, "status": "queued"})


async def list_executions(request):
    
    return JSONResponse(status_code=200, content={"executions": []})


async def get_execution(request):
    
    exec_id = request.path_params['id']

    job = jobs.get(exec_id)

    if not job:
       return JSONResponse(status_code=404, content={"error": "Job not found"})

    return JSONResponse(status_code=200, content=job)

async def cancel_execution(request):
    
    exec_id = request.path_params['id']

    return JSONResponse(status_code=200, content={"id": exec_id, "status": "cancelled"})
