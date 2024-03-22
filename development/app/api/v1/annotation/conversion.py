from classes import (
    AnnotationType,
    NtuaAnnotation,
    NtuaCreator,
    NtuaSelector,
    NtuaTarget,
    NtuaValidationReview,
    ObjectRequest,
    ColorRequest,
    EuropeanaResponse,
    NtuaResponse,
    RequestService,
)

from api.v1.annotation.tools import get_utc_timestamp


def object_to_ntua(data: dict, request: ObjectRequest) -> dict:
    if request.service == RequestService.internal:
        pass
    elif request.service == RequestService.googlevision:
        pass
    return data


def color_to_ntua(data: dict, request: ColorRequest) -> dict:

    creator = NtuaCreator(name='AI4C color detector')
    target = NtuaTarget(source=request.source, selector=NtuaSelector())

    body = []

    for key in data['colors']:
        url = data['colors'][key]['europeana_uri']
        body.append(url)

    review = NtuaValidationReview()

    annotation = NtuaAnnotation(
        id=request.id,
        created=get_utc_timestamp(),
        creator=creator,
        body=body,
        # to do: what should this be?
        confidence=0.5,
        target=target,
        review=review,
    )

    result = NtuaResponse(graph=[annotation])

    return result.model_dump(by_alias=True)


def object_to_europeana(data: dict, request: ObjectRequest) -> dict:
    if request.service == RequestService.internal:
        pass
    elif request.service == RequestService.googlevision:
        pass
    return data


def color_to_europeana(data: dict, request: ColorRequest) -> dict:
    if request.service == RequestService.internal:
        pass
    elif request.service == RequestService.huggingface:
        pass
    return data


def convert(data: dict, request: ObjectRequest | ColorRequest) -> dict:

    # to do: conversion logic + other formats?

    if isinstance(request, ObjectRequest):
        if request.annotation_type == AnnotationType.ntua:
            return object_to_ntua(data, request)
        elif request.annotation_type == AnnotationType.europeana:
            return object_to_europeana(data, request)

    elif isinstance(request, ColorRequest):
        if request.annotation_type == AnnotationType.ntua:
            return color_to_ntua(data, request)
        elif request.annotation_type == AnnotationType.europeana:
            return color_to_europeana(data, request)
    else:
        return data
