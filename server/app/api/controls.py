from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import json
import logging
from dataclasses import asdict

from app.ardunio.serial_read import read_control_struct, SERIAL_PORT

router = APIRouter()

serial_queue = asyncio.Queue()

logger = logging.getLogger("uvicorn.error")

def blocking_read(queue: asyncio.Queue):
    # Run serial reader in a thread via the event loop's executor
    logger.debug("[SerialExecutor] Starting serial reader in executor.")
    for value in read_control_struct(SERIAL_PORT):
        logger.debug(f"[SerialExecutor] Received value from serial: {value}")
        queue.put_nowait(value)

@router.websocket("/controls")
async def control_websocket(websocket: WebSocket):
    logger.debug("[WebSocket] New client connected.")
    await websocket.accept()
    loop = asyncio.get_running_loop()
    if not getattr(control_websocket, "serial_started", False):
        logger.debug("[Controls] Submitting serial reader to executor.")
        loop.run_in_executor(None, blocking_read, serial_queue)
        control_websocket.serial_started = True
    try:
        while (value := await serial_queue.get()):
            logger.debug(f"[WebSocket] Sending value to client: {value}")
            await websocket.send_text(json.dumps(asdict(value)))
    except WebSocketDisconnect:
        logger.debug("[WebSocket] WebSocket disconnected")
    except Exception as e:
        logger.debug(f"[WebSocket] WebSocket error: {e}")
