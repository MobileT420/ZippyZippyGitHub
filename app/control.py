from fastapi import APIRouter
from app.device_manager import manager

router = APIRouter()


@router.get("/devices")
def devices():

    return manager.names()


@router.post("/upload/start/{device}")
async def start_upload(device: str):

    ok = await manager.send(
        device,
        {
            "type": "upload_command",
            "command": "start"
        }
    )

    return {
        "success": ok
    }


@router.post("/upload/stop/{device}")
async def stop_upload(device: str):

    ok = await manager.send(
        device,
        {
            "type": "upload_command",
            "command": "stop"
        }
    )

    return {
        "success": ok
    }