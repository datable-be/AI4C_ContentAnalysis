from classes import (
    AnnotationType,
    ObjectRequest,
    ColorRequest,
    EuropeanaResponse,
    NtuaResponse,
    RequestService,
)


def object_to_ntua(data: dict, request: ObjectRequest) -> NtuaResponse:
    if request.service == RequestService.internal:
        pass
    elif request.service == RequestService.googlevision:
        pass
    return data


def color_to_ntua(data: dict, request: ColorRequest) -> NtuaResponse:
    if request.service == RequestService.internal:
        pass
    elif request.service == RequestService.huggingface:
        pass
    return data


def object_to_europeana(
    data: dict, request: ObjectRequest
) -> EuropeanaResponse:
    if request.service == RequestService.internal:
        pass
    elif request.service == RequestService.googlevision:
        pass
    return data


def color_to_europeana(data: dict, request: ColorRequest) -> EuropeanaResponse:
    if request.service == RequestService.internal:
        pass
    elif request.service == RequestService.huggingface:
        pass
    return data


def convert(
    data: dict, request: ObjectRequest | ColorRequest
) -> EuropeanaResponse | NtuaResponse:

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
