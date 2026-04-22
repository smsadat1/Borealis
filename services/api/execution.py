import asyncio
import json
import uuid

from starlette.responses import JSONResponse

from api.connrpc import run_borealis
from api.ws import send_status


async def create_execution(request):
    
    form = await request.form()
    language = form['language']
    version = form['version']

    stdins: list[str] = []

    for item in form.getlist('inputs'):
        if hasattr(item, 'read'):
            stdins.append((await item.read()).decode('utf-8'))
        else:
            stdins.append(item)


    file = form['file']
    src_code = (await file.read()).decode('utf-8')

    exec_id = str(uuid.uuid4())

    job_data = {
        "id": exec_id,
        "status": "queued",
        "language": language,
        "version": version,
        "source_code": src_code,
        "stdins": stdins,
        "stdout": None,
        "stderr": None,
        "exit_code": None
    }

    await send_status(exec_id=exec_id, status="Recived")

    redis = request.app.state.redis
    await redis.set(f"job:{exec_id}", json.dumps(job_data))
    await redis.lpush("queue:executions", exec_id)

    asyncio.create_task(run_borealis(
        request=request, exec_id=exec_id, lang=language, version=version, src_code=src_code, stdins=stdins))

    return JSONResponse(status_code=200, content={"id": exec_id, "status": "Queued"})


async def list_executions(request):
    
    return JSONResponse(status_code=200, content={"executions": []})


async def get_execution(request):
    
    exec_id = request.path_params['exec_id']

    redis = request.app.state.redis
    job_data = await redis.get(f"exec_id:{exec_id}")
    job_data = json.loads(job_data)

    if not job_data:
       return JSONResponse(status_code=404, content={"error": "Job not found"})

    return JSONResponse(
        status_code=200, 
        content={
            "id": job_data['id'],
            "status": job_data['status'],
            "total_tests": job_data['total_tests'],
            "passed_tests": job_data['passed_tests'],
            "failed_tests": job_data['failed_tests'],
            "timeouts": job_data['timeouts'],
        }
    )


async def cancel_execution(request):
    
    exec_id = request.path_params['id']
    return JSONResponse(status_code=200, content={"id": exec_id, "status": "cancelled"})
