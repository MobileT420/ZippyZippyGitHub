from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter()

UPLOAD_FOLDER = Path("uploads")


# -----------------------------
# List Files
# -----------------------------

@router.get("/download/list")
def list_files():

    files = []

    if not UPLOAD_FOLDER.exists():
        return files

    for file in UPLOAD_FOLDER.rglob("*"):

        if file.is_file():

            relative_path = (
                str(file.relative_to(UPLOAD_FOLDER))
                .replace("\\", "/")
            )

            files.append({
                "path": relative_path,
                "size": file.stat().st_size
            })

    return files


# -----------------------------
# Safe File Path
# -----------------------------

def get_safe_file(file_path: str):

    root = UPLOAD_FOLDER.resolve()

    target = (
        UPLOAD_FOLDER / file_path
    ).resolve()

    try:
        target.relative_to(root)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid path"
        )

    return target


# -----------------------------
# Download File
# -----------------------------

@router.get("/download/file")
def download_file(path: str):

    file = get_safe_file(path)

    if not file.exists() or not file.is_file():

        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    return FileResponse(
        path=file,
        filename=file.name,
        media_type="application/octet-stream"
    )


# -----------------------------
# Delete File
# -----------------------------

@router.delete("/download/file")
def delete_file(path: str):

    file = get_safe_file(path)

    if not file.exists() or not file.is_file():

        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    file.unlink()

    # Remove empty parent folders
    parent = file.parent

    while parent != UPLOAD_FOLDER:

        try:
            parent.rmdir()
        except OSError:
            break

        parent = parent.parent

    return {
        "success": True,
        "deleted": path
    }