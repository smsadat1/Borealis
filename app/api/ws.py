import asyncio

from starlette.websockets import WebSocket

from setup.state import main_loop

active_ws = {}  # {exec_id: set of WebSocket connections}
last_status = {}

def set_main_loop():
    global main_loop
    if main_loop is None:
        main_loop = asyncio.get_running_loop()

async def borealis_ws_stream(websocket: WebSocket):
    
    set_main_loop()
    
    await websocket.accept()
    exec_id = websocket.path_params["exec_id"]
    
    if exec_id not in active_ws:
        active_ws[exec_id] = set()
    active_ws[exec_id].add(websocket)

    if exec_id in last_status:
        await websocket.send_text(last_status[exec_id])

    try:
        while True:
            await asyncio.sleep(3600) 
    except Exception as e:
        print("WS SEND ERROR:", repr(e))
    finally:
        active_ws[exec_id].discard(websocket)


async def send_status(exec_id: str, status: str):
    
    last_status[exec_id] = status

    conns = active_ws.get(exec_id, set())
    print(f"[WS DEBUG] active connections for {exec_id}: {len(conns)}")
    for ws in list(conns):
        try:
            await ws.send_text(status)
        except Exception as e:
            print("WS ERROR:", e)
            active_ws[exec_id].discard(ws)