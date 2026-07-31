from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from app.device_manager import manager

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    device_name = "Unknown"

    try:

        while True:

            message = await websocket.receive_json()

            if message["type"] == "register":

                device_name = message["device_name"]

                manager.add(
                    device_name,
                    websocket
                )

                print(f"\n✅ {device_name} Connected")

                await websocket.send_json(
                    {
                        "status": "connected"
                    }
                )

            elif message["type"] == "ping":

                await websocket.send_json(
                    {
                        "type": "pong"
                    }
                )

            elif message["type"] == "upload_status":

                print(message)

    except WebSocketDisconnect:

        manager.remove(device_name)

        print(f"\n❌ {device_name} Disconnected")