from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from classes import ObjectRequest, ColorRequest
from constants import INFO, SETTINGS, DESCRIPTION
from api.v1.object import detect as object_detect
from api.v1.color import detect as color_detect


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

    if not q:
        return INFO

    if q == "version":
        return {"version": INFO["version"]}
    elif q == "info":
        return INFO
    else:
        raise HTTPException(status_code=404, detail="Invalid query")


@app.post("/v1/object")
async def object_detection(
    request: ObjectRequest,
) -> dict:
    """
    Handle an object detection POST request to the API
    """

    return object_detect.detection(SETTINGS)


@app.post("/v1/color")
async def color_detection(
    request: dict,
) -> dict:
    """
    Handle a color detection POST request to the API
    """

    return color_detect.detection(SETTINGS)
