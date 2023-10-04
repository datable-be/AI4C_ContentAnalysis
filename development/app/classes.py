from enum import Enum
from pydantic import BaseModel, Field, HttpUrl


class LDSource(str, Enum):
    ft = "FT"  # Fashion Thesaurus
    wd = "Wikidata"


class SelectorType(str, Enum):
    fragment = "FragmentSelector"


class SelectorStandard(str, Enum):
    w3 = "http://www.w3.org/TR/media-frags/"


class Selector(BaseModel):
    type: SelectorType = Field(
        title="type",
        description="Selector type",
        default=SelectorType.fragment,
    )
    conformsTo: SelectorStandard = Field(
        title="conformsTo",
        description="Selector standard",
        default=SelectorStandard.w3,
    )
    value: str = Field(
        title="value",
        description="Area from which the foreground detection should be applied (default='xywh=percent:0,0,100,100')",
        default="xywh=percent:0,0,100,100",
        pattern="^xywh=percent:[0-9]+,[0-9]+,[0-9]+,[0-9]+$",
    )


class ObjectRequest(BaseModel):
    # to revise when API request has definite form
    id: str = Field(
        title="id", description="Identifier of the resource to be tagged"
    )
    min_confidence: float = Field(
        title="min_confidence",
        description="Confidence threshold (default=0.8)",
        default=0.8,
        ge=0,
        le=1,
    )
    max_objects: int = Field(
        title="max_objects",
        description="Maximum number of objects to retrieve (default=1)",
        default=1,
    )
    source: HttpUrl = Field(title="source", description="HTTP(S) URL to image")
    service: str = Field(
        title="service",
        description="Name of the object detection service",
        default="internal",
    )
    service_key: str = Field(
        title="service_key", description="API key of the external service"
    )


class ColorRequest(BaseModel):
    # to revise when API request has definite form
    id: str = Field(title="id", description="Identifier of the request")
    max_colors: int = Field(
        title="max_colors",
        description="Maximum number of colors to retrieve (default=3)",
        default=3,
    )
    min_area: float = (
        Field(
            title="min_area",
            description="Minimum share of a given color in the total area of the depicted object (default=0.15)",
            default=0.15,
            ge=0,
            le=1,
        ),
    )
    ld_source: LDSource = Field(
        title="ld_source",
        description="LD source from which the color URIs are given: Fashion Thesaurus or Wikidata (default = FT)",
        default=LDSource.ft,
    )
    source: HttpUrl = Field(title="source", description="HTTP(S) URL to image")
    foreground_detection: bool = Field(
        title="foreground_detection",
        description="Whether the tool should apply foreground detection for the given area (default=True)",
        default=True,
    )
    selector: Selector = Field(
        title="selector", description="Selector for the image"
    )


class ResponseModel(BaseModel):
    # to do when API response has definite form
    ...
