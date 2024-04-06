from classes import (
    LDSource,
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

from constants import GOOGLE_KG_URL

from api.v1.annotation.tools import get_utc_timestamp


def object_to_ntua(data: dict, request: ObjectRequest) -> dict:

    creator = NtuaCreator(name='AI4C object detector')

    annotations = []

    if request.service == RequestService.internal:
        for item in data['data']:

            # to do: check selector (see 'box' key)
            selector = NtuaSelector()
            target = NtuaTarget(source=request.source, selector=selector)

            annotation = NtuaAnnotation(
                # to do: is this correct? always same id?
                id=request.id,
                created=get_utc_timestamp(),
                creator=creator,
                # to do: Datable docs conflict specification?
                body=[item['wikidata']['wikidata_concepturi']],
                confidence=item['confidence'],
                target=target,
                review=NtuaValidationReview(),
            )
            annotations.append(annotation)

    elif request.service == RequestService.googlevision:
        for item in data['data'][0]['labelAnnotations']:

            # to do: check selector (see 'box' key)
            selector = NtuaSelector()
            target = NtuaTarget(source=request.source, selector=selector)

            annotation = NtuaAnnotation(
                # to do: is this correct? always same id?
                id=request.id,
                created=get_utc_timestamp(),
                creator=creator,
                # to do: Datable docs conflict specification? + uri?
                body=[GOOGLE_KG_URL + item['mid']],
                confidence=item['score'],
                target=target,
                review=NtuaValidationReview(),
            )
            annotations.append(annotation)

    result = NtuaResponse(graph=annotations)

    return result.model_dump(by_alias=True)


def color_to_ntua(data: dict, request: ColorRequest) -> dict:

    creator = NtuaCreator(name='AI4C color detector')
    target = NtuaTarget(source=request.source, selector=NtuaSelector())

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
        # default confidence of 0.5 as this is not supplied by the APIs
        confidence=0.5,
        # to do: check selector
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
