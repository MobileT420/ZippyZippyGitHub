from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from app.device_manager import manager

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    device_name = None
    receiver_name = None

    try:

        while True:

            message = await websocket.receive_json()

            message_type = message.get("type")

            # -------------------------
            # Android Phone
            # -------------------------
            if message_type == "register":

                device_name = message["device_name"]

                device_id = message.get(
                    "device_id",
                    ""
                )

                android_version = message.get(
                    "android_version",
                    ""
                )

                manager.add_phone(
                    device_name,
                    websocket
                )

                print(f"\n📱 Phone Connected")
                print(f"Name : {device_name}")
                print(f"ID   : {device_id}")
                print(f"OS   : Android {android_version}")

                await websocket.send_json(
                    {
                        "status": "connected"
                    }
                )

            # -------------------------
            # Home PC Receiver
            # -------------------------
            elif message_type == "receiver":

                receiver_name = message["name"]

                manager.add_receiver(
                    receiver_name,
                    websocket
                )

                print(
                    f"\n🖥 Receiver Connected : {receiver_name}"
                )

                await websocket.send_json(
                    {
                        "status": "connected"
                    }
                )

            # -------------------------
            # Heartbeat
            # -------------------------
            elif message_type == "ping":

                await websocket.send_json(
                    {
                        "type": "pong"
                    }
                )

            # -------------------------
            # Receiver Upload Status
            # -------------------------
            elif message_type == "upload_status":

                print(
                    f"\n📤 {message}"
                )

            # -------------------------
            # Unknown Message
            # -------------------------
            else:

                print(
                    f"\n⚠ Unknown Message : {message}"
                )

    except WebSocketDisconnect:

        if device_name is not None:

            manager.remove_phone(
                device_name
            )

            print(
                f"\n❌ Phone Disconnected : {device_name}"
            )

        if receiver_name is not None:

            manager.remove_receiver(
                receiver_name
            )

            print(
                f"\n❌ Receiver Disconnected : {receiver_name}"
            )

    except Exception as e:

        print(
            f"\n❌ WebSocket Error : {e}"
        )

        if device_name is not None:
            manager.remove_phone(
                device_name
            )

        if receiver_name is not None:
            manager.remove_receiver(
                receiver_name
            )