import asyncio
import json
import websockets
import json

from file_receiver import *

from config import *


async def start():

    while True:

        try:

            print("Connecting...")

            async with websockets.connect(
                RAILWAY_WS
            ) as ws:

                print("Connected")

                await ws.send(
                    json.dumps(
                        {
                            "type": "receiver",
                            "name": RECEIVER_NAME
                        }
                    )
                )

                while True:

                    message = await ws.recv()

                    if isinstance(message, bytes):

                        print(f"Received {len(message)} bytes")

                    else:

                        if isinstance(message, bytes):

                            write_chunk(message)

                        else:

                            data = json.loads(message)

                            t = data.get("type")

                            if t == "start_upload":

                                path = "uploads/" + \
                                    data["deviceFolder"] + "/" + \
                                    data["relativePath"] + \
                                    data["filename"]

                                start_file(path)

                                print("Receiving:", path)

                            elif t == "finish_upload":

                                finish_file()
        except Exception as e:

            print(e)

            print("Reconnect in 5 seconds...")

            await asyncio.sleep(5)