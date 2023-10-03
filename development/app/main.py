from enum import Enum
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from constants import INFO, SETTINGS, DESCRIPTION
from api.v1.object import detect as object_detect
from api.v1.color import detect as color_detect

# CLASSES


class RequestType(str, Enum):
    object = "object"
    color = "color"


class DetectionRequest(BaseModel):
    requestType: RequestType = Field(
        default=None, title="Type of detection request"
    )
    data: dict  # to do: when API is of fixed form, replace with submodel ObjectRequest | ColorRequest


class ResponseModel(BaseModel):
    # to do when API response is fixed
    ...


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


@app.post("/v1")
async def detection(
    request: DetectionRequest,
) -> dict:
    """
    Post a detection request to the API
    """

    if request.requestType == RequestType.color:
        return color_detect.detection(SETTINGS)
    elif request.requestType == RequestType.object:
        return object_detect.detection(SETTINGS)
    else:
        raise HTTPException(status_code=404, detail="Invalid requestType")
