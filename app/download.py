from fastapi import APIRouter
from pathlib import Path

router = APIRouter()

UPLOAD_FOLDER = Path("uploads")


@router.get("/download/list")
def list_files():

    files = []

    for file in UPLOAD_FOLDER.rglob("*"):

        if file.is_file():

            files.append({

                "path": str(
                    file.relative_to(
                        UPLOAD_FOLDER
                    )
                ).replace("\\","/"),

                "size": file.stat().st_size

            })

    return files