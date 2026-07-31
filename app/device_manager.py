from fastapi import WebSocket


class DeviceManager:

    def __init__(self):

        self.devices = {}

    def add(
        self,
        name: str,
        websocket: WebSocket
    ):

        self.devices[name] = {
            "socket": websocket
        }

    def remove(self, name: str):

        self.devices.pop(name, None)

    def names(self):

        return list(self.devices.keys())

    def get(self, name: str):

        return self.devices.get(name)

    async def send(
        self,
        name: str,
        message: dict
    ):

        device = self.get(name)

        if device is None:
            return False

        try:

            await device["socket"].send_json(
                message
            )

            return True

        except Exception:

            self.remove(name)

            return False


manager = DeviceManager()