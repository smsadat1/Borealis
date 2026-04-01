import asyncio
import json
import uuid

from starlette.responses import JSONResponse

from app.execution.runners.base import run_borealis

async def create_execution(request):
    
    form = await request.form()
    language = form['language']
    stdin = form['inputs']
    file = form['file']
    src_code = (await file.read()).decode('utf-8')

    exec_id = str(uuid.uuid4())

    job_data = {
        "id": exec_id,
        "status": "queued",
        "language": language,
        "source_code": src_code,
        "stdin": stdin,
        "stdout": None,
        "stderr": None,
        "exit_code": None
    }

    redis = request.app.state.redis
    await redis.set(f"job:{exec_id}", json.dumps(job_data))
    await redis.lpush("queue:executions", exec_id)

    asyncio.create_task(run_borealis(request=request, exec_id=exec_id))

    return JSONResponse(status_code=200, content={"id": exec_id, "status": "queued"})


async def list_executions(request):
    
    return JSONResponse(status_code=200, content={"executions": []})


async def get_execution(request):
    
    exec_id = request.path_params['id']

    redis = request.app.state.redis
    job_data = await redis.get(f"job:{exec_id}")
    job_data = json.loads(job_data)

    if not job_data:
       return JSONResponse(status_code=404, content={"error": "Job not found"})

    return JSONResponse(
        status_code=200, 
        content={
            "id": job_data['id'],
            "status": job_data['status'],
            "stdout": job_data['stdout'],
            "stderr": job_data['stderr'],
            "exit_code": job_data['exit_code'],
        }
    )


async def cancel_execution(request):
    
    exec_id = request.path_params['id']
    return JSONResponse(status_code=200, content={"id": exec_id, "status": "cancelled"})
