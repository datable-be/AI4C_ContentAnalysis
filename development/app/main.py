import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from api.v1.object import detect as object_detect
from api.v1.color import detect as color_detect

# CONSTANTS

with open("info.json", "r") as f:
    INFO = json.load(f)
with open("settings.json", "r") as f:
    SETTINGS = json.load(f)

# CLASSES


class DetectionRequest(BaseModel):
    requestType: str
    data: dict  # to do: when API is of fixed form, replace with ObjectRequest | ColorRequest


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
async def route(request: DetectionRequest) -> dict:

    if request.requestType == "color":
        return color_detect.detection()
    elif request.requestType == "object":
        return object_detect.detection()
    else:
        raise HTTPException(status_code=404, detail="Invalid requestType")
