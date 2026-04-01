import json
import tempfile

from app.execution.runners.exec_compile import exec_compile
from app.execution.runners.exec_interpret import exec_interpret

async def borealis_compiler(language: str, source_code: str, stdin: str):

    temp_dir = tempfile.mkdtemp(prefix="borealis_exec_")

    if language == "c":
        stdout, stderr, exit_code = await exec_compile(
            command="gcc", temp_dir=temp_dir, stdin=stdin, source_code=source_code
        )
    
    elif language == "cpp" or language == "c++" or language == "cxx":
        stdout, stderr, exit_code = await exec_compile(
            command="g++", temp_dir=temp_dir, stdin=stdin, source_code=source_code
        )
        
    elif language == "python" or language == "py":
        stdout, stderr, exit_code = await exec_interpret(
            command="python3", temp_dir=temp_dir, stdin=stdin, source_code=source_code
        )

    elif language == "javascript" or language == "js":
        stdout, stderr, exit_code = await exec_interpret(
            command="node", temp_dir=temp_dir, stdin=stdin, source_code=source_code
        )
    
    return stdout, stderr, exit_code


async def run_borealis(request, exec_id):

    redis = request.app.state.redis

    print("Looking for ", f"id:{exec_id}")
    job_data = await redis.get(f"job:{exec_id}")
    job = json.loads(job_data)

    job['status'] = 'running'
    await redis.set(f"job:{exec_id}", json.dumps(job))

    stdout, stderr, exit_code = await borealis_compiler(
        language=job['language'], source_code=job['source_code'], stdin=job['stdin'],
    )

    # update result
    job.update({
        "status": "completed",
        "stdout": stdout,
        "stderr": stderr,
        "exit_code": exit_code
    })

    await redis.set(f"job:{exec_id}", json.dumps(job))