from enum import Enum
from pydantic import BaseModel, Field


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
