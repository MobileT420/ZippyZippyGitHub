from fastapi import WebSocket
import json


class DeviceManager:

    def __init__(self):

        self.phones = {}

        self.receivers = {}

    # ---------------- Phones ----------------

    def add_phone(self, name, websocket: WebSocket):

        self.phones[name] = websocket

        print(f"📱 Phone Connected : {name}")

    def remove_phone(self, name):

        self.phones.pop(name, None)

        print(f"📱 Phone Removed : {name}")

    # ---------------- Receivers ----------------

    def add_receiver(self, name, websocket: WebSocket):

        self.receivers[name] = websocket

        print(f"🖥 Receiver Connected : {name}")

    def remove_receiver(self, name):

        self.receivers.pop(name, None)

        print(f"🖥 Receiver Removed : {name}")

    # ---------------- Get ----------------

    def get_phone(self, name):

        return self.phones.get(name)

    def get_receiver(self, name):

        return self.receivers.get(name)

    # ---------------- Lists ----------------

    def names(self):

        return list(self.phones.keys())

    def receiver_names(self):

        return list(self.receivers.keys())

    # ---------------- Send ----------------

    async def send(self, device, data):

        websocket = self.phones.get(device)

        if websocket is None:

            print(f"❌ Phone not found : {device}")

            return False

        try:

            await websocket.send_text(
                json.dumps(data)
            )

            print(f"📤 Sent to {device} : {data}")

            return True

        except Exception as e:

            print(f"❌ Send Failed : {e}")

            return False


manager = DeviceManager()