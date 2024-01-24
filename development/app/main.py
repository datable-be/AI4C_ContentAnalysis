from os.path import join, exists

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse

from classes import ObjectRequest, ColorRequest
from constants import INFO, SETTINGS, DESCRIPTION, NET, TEMP_DIR
from api.v1.object import detect as object_detect
from api.v1.color import detect as color_detect

# Eagerly load object model (once, at startup)

net = NET

# CREATE API

app = FastAPI(
    title=INFO["title"],
    description=DESCRIPTION,
    summary=INFO["summary"],
    version=INFO["version"],
    terms_of_service=INFO["termsOfService"],
    contact=INFO["contact"],
    license_info=INFO["license"],
)

# API REQUESTS


@app.get("/")
async def info(q: str | None = None) -> JSONResponse:
    """
    Get descriptive metadata about the API
    """

    if q:
        if q == "version":
            return {"version": INFO["version"]}
        elif q == "info":
            return INFO
        else:
            raise HTTPException(status_code=404, detail="Invalid query")

    else:
        return INFO


@app.get("/image")
async def image(img: str | None = None) -> FileResponse:
    """
    Get image from the API
    """

    if img:
        path = join(TEMP_DIR, img)
        if exists(path):
            return FileResponse(path)
        else:
            raise HTTPException(status_code=404, detail="File not found")
    else:
        raise HTTPException(status_code=404, detail="Invalid query")


@app.post("/v1/object")
async def object_detection(
    request: ObjectRequest,
) -> dict:
    """
    Handle an object detection POST request to the API
    """
    return object_detect.detection(request, net, SETTINGS)


@app.post("/v1/color")
async def color_detection(
    request: ColorRequest,
) -> dict:
    """
    Handle a color detection POST request to the API
    """

    return color_detect.detection(request, net, SETTINGS)
