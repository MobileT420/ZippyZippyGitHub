import asyncio
import json
import html
from pathlib import Path

import requests


RAILWAY_HTTP = (
    "https://zippyzippygithub-production.up.railway.app"
)

DOWNLOAD_FOLDER = Path("downloads")


# ---------------------------------
# Notification HTML
# ---------------------------------

def save_notification(remote_path, data):

    # Device folder is first part of remote path
    device_folder = remote_path.split("/")[0]

    notification_folder = (
        DOWNLOAD_FOLDER /
        device_folder /
        "notifications"
    )

    notification_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    html_file = (
        notification_folder /
        "notifications.html"
    )

    # Create HTML once
    if not html_file.exists():

        html_file.write_text(
            """
<!DOCTYPE html>
<html>

<head>

<meta charset="utf-8">

<title>Zippy Notification Backup</title>

<style>

body {
    font-family: Arial, sans-serif;
    background: #f5f5f5;
    margin: 20px;
}

h2 {
    margin-bottom: 20px;
}

.card {
    background: white;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,.15);
}

.app {
    color: #1976d2;
    font-weight: bold;
    font-size: 18px;
}

.title {
    margin-top: 8px;
    font-weight: bold;
}

.text {
    margin-top: 5px;
    white-space: pre-wrap;
}

.time {
    margin-top: 10px;
    color: gray;
    font-size: 12px;
}

</style>

</head>

<body>

<h2>Zippy Notification Backup</h2>

</body>

</html>
""",
            encoding="utf-8"
        )

    content = html_file.read_text(
        encoding="utf-8"
    )

    card = f"""
<div class="card">

<div class="app">{html.escape(str(data.get("appName", "")))}</div>

<div class="title">{html.escape(str(data.get("title", "")))}</div>

<div class="text">{html.escape(str(data.get("text", "")))}</div>

<div class="time">{html.escape(str(data.get("time", "")))}</div>

</div>

"""

    content = content.replace(
        "</body>",
        card + "\n</body>"
    )

    html_file.write_text(
        content,
        encoding="utf-8"
    )

    print(
        f"🔔 Notification saved: "
        f"{data.get('appName', '')}"
    )


# ---------------------------------
# Delete Railway File
# ---------------------------------

def delete_remote_file(remote_path):

    try:

        response = requests.delete(
            f"{RAILWAY_HTTP}/download/file",
            params={
                "path": remote_path
            },
            timeout=30
        )

        if response.ok:

            print(
                f"🗑 Railway deleted: "
                f"{remote_path}"
            )

            return True

        print(
            f"⚠ Delete failed "
            f"HTTP {response.status_code}: "
            f"{remote_path}"
        )

    except Exception as e:

        print(
            f"⚠ Delete error: {e}"
        )

    return False


# ---------------------------------
# Notification Download
# ---------------------------------

def process_notification(remote_path):

    try:

        response = requests.get(
            f"{RAILWAY_HTTP}/download/file",
            params={
                "path": remote_path
            },
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        save_notification(
            remote_path,
            data
        )

        # Only delete AFTER PC successfully
        # added notification to HTML
        delete_remote_file(
            remote_path
        )

    except Exception as e:

        print(
            f"❌ Notification error "
            f"{remote_path}: {e}"
        )


# ---------------------------------
# Media Download
# ---------------------------------

def process_media(
    remote_path,
    expected_size
):

    try:

        print(
            f"⬇ Downloading: {remote_path}"
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
            f"{RAILWAY_HTTP}/download/file",
            params={
                "path": remote_path
            },
            stream=True,
            timeout=120
        ) as response:

            response.raise_for_status()

            with open(
                temp_file,
                "wb"
            ) as output:

                for chunk in response.iter_content(
                    chunk_size=1024 * 1024
                ):

                    if chunk:

                        output.write(chunk)

        actual_size = (
            temp_file.stat().st_size
        )

        if actual_size != expected_size:

            print(
                f"❌ Size mismatch: "
                f"{remote_path}"
            )

            temp_file.unlink(
                missing_ok=True
            )

            return

        # Safe final save
        temp_file.replace(
            local_file
        )

        print(
            f"✅ Saved: {local_file}"
        )

        # Delete only after successful save
        delete_remote_file(
            remote_path
        )

    except Exception as e:

        print(
            f"❌ Media download error "
            f"{remote_path}: {e}"
        )


# ---------------------------------
# Sync Railway
# ---------------------------------

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

        print(
            f"📦 Railway Files: "
            f"{len(files)}"
        )

        for item in files:

            remote_path = item["path"]

            # -------------------------
            # Notification
            # -------------------------

            if (
                "/notifications/" in remote_path
                and remote_path.lower().endswith(".json")
            ):

                process_notification(
                    remote_path
                )

                continue

            # Ignore old notification HTML
            if (
                "/notifications/" in remote_path
                and remote_path.lower().endswith(".html")
            ):

                continue

            # -------------------------
            # Media
            # -------------------------

            process_media(
                remote_path,
                item["size"]
            )

    except Exception as e:

        print(
            f"❌ Download sync error: {e}"
        )


# ---------------------------------
# Background Worker
# ---------------------------------

async def download_worker():

    print(
        "📥 Download Manager Started"
    )

    while True:

        await asyncio.to_thread(
            sync_files
        )

        await asyncio.sleep(30)