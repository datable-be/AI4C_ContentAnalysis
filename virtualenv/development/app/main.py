import json
from fastapi import FastAPI
from api.v1.object import detect as object_detect
from api.v1.color import detect as color_detect

# CONSTANTS

with open("metadata.json", "r") as f:
    METADATA = json.load(f)
with open("settings.json", "r") as f:
    SETTINGS = json.load(f)


# CREATE API

app = FastAPI()


# API REQUESTS


@app.get("/")
async def read_root(q: str | None = None):
    if q == "version":
        return {"version": METADATA["version"]}
    elif q == "explain":
        return METADATA
    else:
        return {"Hello": "World"}


@app.post("/v1/color/detect")
async def detect_color(q: str | None = None):
    return color_detect.detection()


@app.post("/v1/object/detect")
async def detect_object(q: str | None = None):
    return object_detect.detection()
