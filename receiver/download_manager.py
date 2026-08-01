import asyncio
from pathlib import Path
from urllib.parse import quote

import requests


RAILWAY_HTTP = (
    "https://zippyzippygithub-production.up.railway.app"
)

DOWNLOAD_FOLDER = Path("downloads")


def sync_files():

    try:

        response = requests.get(
            f"{RAILWAY_HTTP}/download/list",
            timeout=30
        )

        response.raise_for_status()

        files = response.json()

        if not files:
            return

        print(f"📦 Railway Files: {len(files)}")

        for item in files:

            remote_path = item["path"]
            expected_size = item["size"]

            # Do not download notification HTML here
            if "/notifications/" in remote_path:
                continue

            print(f"⬇ Downloading: {remote_path}")

            encoded_path = quote(
                remote_path,
                safe=""
            )

            download_url = (
                f"{RAILWAY_HTTP}/download/file"
                f"?path={encoded_path}"
            )

            local_file = (
                DOWNLOAD_FOLDER /
                Path(remote_path)
            )

            local_file.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            temp_file = Path(
                str(local_file) + ".part"
            )

            with requests.get(
                download_url,
                stream=True,
                timeout=120
            ) as download:

                download.raise_for_status()

                with open(temp_file, "wb") as output:

                    for chunk in download.iter_content(
                        chunk_size=1024 * 1024
                    ):

                        if chunk:
                            output.write(chunk)

            # Verify size before accepting file
            actual_size = temp_file.stat().st_size

            if actual_size != expected_size:

                print(
                    f"❌ Size mismatch: "
                    f"{remote_path}"
                )

                temp_file.unlink(
                    missing_ok=True
                )

                continue

            # Finished file
            temp_file.replace(local_file)

            print(
                f"✅ Saved: {local_file}"
            )

            # Delete Railway copy only after
            # successful PC save
            delete_response = requests.delete(
                f"{RAILWAY_HTTP}/download/file",
                params={
                    "path": remote_path
                },
                timeout=30
            )

            if delete_response.ok:

                print(
                    f"🗑 Railway deleted: "
                    f"{remote_path}"
                )

            else:

                print(
                    f"⚠ Could not delete Railway copy: "
                    f"{remote_path}"
                )

    except Exception as e:

        print(
            f"❌ Download sync error: {e}"
        )


async def download_worker():

    print("📥 Download Manager Started")

    while True:

        await asyncio.to_thread(
            sync_files
        )

        # Check Railway every 30 seconds
        await asyncio.sleep(30)