from enum import Enum
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from api.v1.object import detect as object_detect
from api.v1.color import detect as color_detect

# CONSTANTS

with open("info.json", "r") as f:
    INFO = json.load(f)
with open("settings.json", "r") as f:
    SETTINGS = json.load(f)

# CLASSES


class RequestType(str, Enum):
    object = "object"
    color = "color"


class DetectionRequest(BaseModel):
    requestType: RequestType = Field(
        default=None, title="Type of detection request")
    data: dict  # to do: when API is of fixed form, replace with submodel ObjectRequest | ColorRequest


# CREATE API


app = FastAPI()


# API REQUESTS


@app.get("/")
async def read_root(q: str | None = None) -> dict:

    if not q:
        return INFO

    if q == "version":
        return {"version": INFO["version"]}
    elif q == "info":
        return INFO
    else:
        raise HTTPException(status_code=404, detail="Invalid query")


@app.post("/v1")
async def detection(request: DetectionRequest) -> dict:

    if request.requestType == RequestType.color:
        return color_detect.detection()
    elif request.requestType == RequestType.object:
        return object_detect.detection()
    else:
        raise HTTPException(status_code=404, detail="Invalid requestType")
