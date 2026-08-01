import asyncio
import json
import websockets

from config import *
from download_manager import download_worker


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

                    print(message)

        except Exception as e:

            print(e)
            print("Reconnect in 5 seconds...")

            await asyncio.sleep(5)


async def main():

    await asyncio.gather(
        start(),
        download_worker()
    )


if __name__ == "__main__":

    asyncio.run(main())