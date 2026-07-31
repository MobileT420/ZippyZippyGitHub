from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.websocket import router as websocket_router
from app.upload import router as upload_router
from app.control import router as control_router

app = FastAPI(
    title="Zippy Receiver",
    version="1.0.0"
)

app.include_router(websocket_router)
app.include_router(upload_router)
app.include_router(control_router)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


@app.get("/")
def home():

    return FileResponse(
        "app/static/index.html"
    )