from uuid import uuid4
from pydantic import HttpUrl

from constants import APP_URL
from classes import (
    AnnotationType,
    ColorRequest,
    EuropeanaAnnotation,
    EuropeanaBody,
    EuropeanaCreator,
    EuropeanaResponse,
    EuropeanaResponse,
    EuropeanaStatement,
    EuropeanaValidationReview,
    LDSource,
    NtuaAnnotation,
    NtuaCreator,
    NtuaResponse,
    NtuaTarget,
    NtuaValidationReview,
    ObjectRequest,
    RequestService,
)

from constants import GOOGLE_KG_URL

from api.v1.annotation.tools import get_utc_timestamp, google_mid_to_wikidata


def object_to_ntua(data: dict, request: ObjectRequest) -> dict:

    creator = NtuaCreator(name='AI4C object detector')
    target = NtuaTarget(source=request.source)

    annotations = []

    if request.service == RequestService.googlevision:
        for item in data['data']['objects'][0]['localizedObjectAnnotations']:

            wikidata_identifier = google_mid_to_wikidata(item['mid'])
            if wikidata_identifier == '':
                wikidata_identifier = GOOGLE_KG_URL + item['mid']

            annotation = NtuaAnnotation(
                id=HttpUrl(APP_URL + '/object-annotation/' + str(uuid4())),
                created=data['data']['created'],
                creator=creator,
                body=[wikidata_identifier],
                confidence=item['score'],
                target=target,
                review=NtuaValidationReview(),
            )
            annotations.append(annotation)

    else:
        for item in data['data']['objects']:

            annotation = NtuaAnnotation(
                id=HttpUrl(APP_URL + '/object-annotation/' + str(uuid4())),
                created=data['data']['created'],
                creator=creator,
                body=[item['wikidata']['wikidata_concepturi']],
                confidence=item['confidence'],
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

    annotation = NtuaAnnotation(
        id=HttpUrl(request.id),
        created=data['data']['created'],
        creator=creator,
        body=body,
        confidence=None,
        target=target,
        review=NtuaValidationReview(),
    )

    result = NtuaResponse(graph=[annotation])

    return result.model_dump(by_alias=True)


def object_to_europeana(data: dict, request: ObjectRequest) -> dict:

    creator = EuropeanaCreator(name='AI4C color detector')
    target = EuropeanaTarget(source=request.source)

    derivedFrom_objects, statement_objects = [], []
    index = 0

    if request.service == RequestService.googlevision:

        for item in data['data']['objects'][0]['localizedObjectAnnotations']:

            wikidata_identifier = google_mid_to_wikidata(item['mid'])
            if wikidata_identifier == '':
                wikidata_identifier = GOOGLE_KG_URL + item['mid']
            index += 1
            identifier = request.id + '.' + str(index)

            derivedFrom = EuropeanaAnnotation(
                id=HttpUrl(identifier),
                created=data['data']['created'],
                creator=creator,
                body=wikidata_identifier,
                confidence=item['score'],
                review=EuropeanaValidationReview(),
            )
            derivedFrom_objects.append(derivedFrom)

            statement_objects.append(wikidata_identifier)

    else:

        for item in data['data']['objects']:

            url = item['wikidata']['wikidata_concepturi']
            index += 1
            identifier = request.id + '.' + str(index)

            derivedFrom = EuropeanaAnnotation(
                id=HttpUrl(identifier),
                created=data['data']['created'],
                creator=creator,
                body=url,
                confidence=item['confidence'],
                review=EuropeanaValidationReview(),
            )
            derivedFrom_objects.append(derivedFrom)

            statement_objects.append(url)

    statements = EuropeanaStatement(
        # to do: what should this be? perhaps UUID like above?
        id=HttpUrl(APP_URL + '/object-annotation/' + str(uuid4())),
        dctformat=statement_objects,
    )

    body = EuropeanaBody(statements=statements)

    # to do: what should this be?
    target = '???'

    result = EuropeanaResponse(
        id=request.id,
        created=data['data']['created'],
        creator=creator,
        generated=get_utc_timestamp(),
        generator=creator,
        derivedFrom=derivedFrom_objects,
        body=body,
        target=target,
    )

    return result.model_dump(by_alias=True)


def color_to_europeana(data: dict, request: ColorRequest) -> dict:

    creator = EuropeanaCreator(name='AI4C color detector')
    target = EuropeanaTarget(source=request.source)

    derivedFrom_objects, statement_objects = [], []

    index = 0
    for key in data['data']['colors']:
        index += 1
        url = data['data']['colors'][key]['europeana_uri']
        identifier = request.id + '.' + str(index)

        derivedFrom = EuropeanaAnnotation(
            id=identifier,
            created=data['data']['created'],
            creator=creator,
            body=url,
            confidence=None,
            review=EuropeanaValidationReview(),
        )
        derivedFrom_objects.append(derivedFrom)

        statement_objects.append(url)

    statements = EuropeanaStatement(
        # to do: what should this be? perhaps UUID like above?
        id=HttpUrl(APP_URL + '/color-annotation/' + str(uuid4())),
        dctformat=statement_objects,
    )

    body = EuropeanaBody(statements=statements)

    # to do: what should this be?
    target = '???'

    result = EuropeanaResponse(
        id=HttpUrl(request.id),
        created=data['data']['created'],
        creator=creator,
        generated=get_utc_timestamp(),
        generator=creator,
        derivedFrom=derivedFrom_objects,
        body=body,
        target=target,
    )

    return result.model_dump(by_alias=True)


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

    return data
