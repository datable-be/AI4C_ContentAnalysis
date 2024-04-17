from uuid import uuid4
from pydantic import HttpUrl

from constants import APP_URL
from classes import (
    LDSource,
    AnnotationType,
    NtuaAnnotation,
    NtuaCreator,
    NtuaTarget,
    NtuaValidationReview,
    ObjectRequest,
    ColorRequest,
    EuropeanaResponse,
    NtuaResponse,
    RequestService,
)

from constants import GOOGLE_KG_URL

from api.v1.annotation.tools import get_utc_timestamp, google_mid_to_wikidata


def object_to_ntua(data: dict, request: ObjectRequest) -> dict:

    creator = NtuaCreator(name='AI4C object detector')

    annotations = []

    if request.service == RequestService.internal:
        for item in data['data']:

            target = NtuaTarget(source=request.source)

            annotation = NtuaAnnotation(
                id=HttpUrl(APP_URL + '/object-annotation/' + str(uuid4())),
                created=get_utc_timestamp(),
                creator=creator,
                body=[item['wikidata']['wikidata_concepturi']],
                confidence=item['confidence'],
                target=target,
                review=NtuaValidationReview(),
            )
            annotations.append(annotation)

    elif request.service == RequestService.googlevision:
        for item in data['data'][0]['localizedObjectAnnotations']:

            target = NtuaTarget(source=request.source)

            wikidata_identifier = google_mid_to_wikidata(item['mid'])
            if wikidata_identifier == '':
                wikidata_identifier = GOOGLE_KG_URL + item['mid']

            annotation = NtuaAnnotation(
                id=HttpUrl(APP_URL + '/color-annotation/' + str(uuid4())),
                created=get_utc_timestamp(),
                creator=creator,
                body=[wikidata_identifier],
                confidence=item['score'],
                target=target,
                review=NtuaValidationReview(),
            )
            annotations.append(annotation)

    result = NtuaResponse(graph=annotations)

    return result.model_dump(by_alias=True)


def color_to_ntua(data: dict, request: ColorRequest) -> dict:

    creator = NtuaCreator(name='AI4C color detector')
    target = NtuaTarget(source=request.source)

    body = []

    for key in data['data']['colors']:
        if request.ld_source == LDSource.wd:
            url = data['data']['colors'][key]['wikidata_uri']
        else:
            url = data['data']['colors'][key]['europeana_uri']
        body.append(url)

    review = NtuaValidationReview()

    annotation = NtuaAnnotation(
        id=request.id,
        created=get_utc_timestamp(),
        creator=creator,
        body=body,
        # to do: default confidence of 0.5 as this is not supplied by the APIs
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
