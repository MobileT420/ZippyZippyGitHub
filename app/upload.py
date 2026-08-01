from fastapi import APIRouter, UploadFile, File, Form
from pathlib import Path
import shutil
from datetime import datetime
import html
from datetime import datetime
from zoneinfo import ZoneInfo

router = APIRouter()

UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)


# -----------------------------
# Media Upload
# -----------------------------

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    relativePath: str = Form(""),
    deviceFolder: str = Form("unknown_device")
):

    relativePath = relativePath.strip("/\\")

    destination_folder = (
        UPLOAD_FOLDER /
        deviceFolder /
        relativePath
    )

    destination_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    destination = destination_folder / file.filename

    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "success": True
    }


# -----------------------------
# Notification Upload
# -----------------------------

@router.post("/notification")
async def upload_notification(

    packageName: str = Form(...),

    appName: str = Form(...),

    title: str = Form(""),

    text: str = Form(""),

    time: int = Form(...),

    deviceFolder: str = Form(...)
):

    notification_folder = (
        UPLOAD_FOLDER /
        deviceFolder /
        "notifications"
    )

    notification_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    html_file = notification_folder / "notifications.html"

    if not html_file.exists():

        html_file.write_text(
            """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Zippy Notifications</title>

<style>

body{
    font-family:Arial;
    background:#f5f5f5;
    margin:20px;
}

.card{

    background:white;

    border-radius:10px;

    padding:15px;

    margin-bottom:12px;

    box-shadow:0 2px 8px rgba(0,0,0,.15);
}

.app{

    color:#1976d2;

    font-weight:bold;

    font-size:18px;
}

.title{

    margin-top:8px;

    font-weight:bold;
}

.time{

    margin-top:10px;

    color:gray;

    font-size:12px;
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

    dt = (
        datetime
        .fromtimestamp(time / 1000, ZoneInfo("Asia/Kolkata"))
        .strftime("%d-%m-%Y %H:%M:%S")
    )

    card = f"""
<div class="card">

<div class="app">{html.escape(appName)}</div>

<div class="title">{html.escape(title)}</div>

<div>{html.escape(text)}</div>

<div class="time">{dt}</div>

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

    return {
        "success": True
    }