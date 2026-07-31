from fastapi import WebSocket


class DeviceManager:

    def __init__(self):

        self.phones = {}

        self.receivers = {}

    # ---------------- Phones ----------------

    def add_phone(self, name, websocket):
        self.phones[name] = websocket

    def remove_phone(self, name):
        self.phones.pop(name, None)

    # ---------------- Receiver ----------------

    def add_receiver(self, name, websocket):
        self.receivers[name] = websocket

    def remove_receiver(self, name):
        self.receivers.pop(name, None)

    # ---------------- Get ----------------

    def get_receiver(self, name):
        return self.receivers.get(name)

    def get_phone(self, name):
        return self.phones.get(name)

    def names(self):
        return list(self.phones.keys())


manager = DeviceManager()