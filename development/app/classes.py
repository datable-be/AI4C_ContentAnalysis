from typing import List, Dict
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl

from constants import NTUA_CONTEXT, EUROPEANA_CONTEXT


class LDSource(str, Enum):
    ft = 'FT'  # Fashion Thesaurus
    wd = 'Wikidata'


class AnnotationType(str, Enum):
    w3c = 'w3c'
    europeana = 'europeana'
    ntua = 'ntua'
    internal = 'internal'


class RequestService(str, Enum):
    internal = 'internal'
    googlevision = 'GoogleVision'
    blipvqabase = 'blip-vqa-base'


class SelectorType(str, Enum):
    fragment = 'FragmentSelector'
    rdfpath = 'RDFPathSelector'
    rdfproperty = 'RDFPropertySelector'


class SelectorStandard(str, Enum):
    w3 = 'http://www.w3.org/TR/media-frags/'


class GoogleFeatureType(str, Enum):
    localization = 'OBJECT_LOCALIZATION'
    label = 'LABEL_DETECTION'
    properties = 'IMAGE_PROPERTIES'


class NtuaEntity(str, Enum):
    person = 'Person'
    software = 'Software'


class NtuaReviewType(str, Enum):
    validation = 'Validation'
    rating = 'Rating'


class NtuaRecommendationType(str, Enum):
    accept = 'accept'
    reject = 'reject'


class ColorSelector(BaseModel):
    type: SelectorType = Field(
        title='type',
        description='Selector type',
        default=SelectorType.fragment,
    )
    conformsTo: SelectorStandard = Field(
        title='conformsTo',
        description='Selector standard',
        default=SelectorStandard.w3,
    )
    value: str = Field(
        title='value',
        description="Area from which the foreground detection should be applied (default='xywh=percent:0,0,100,100')",
        default='xywh=percent:0,0,100,100',
        pattern='^xywh=percent:[0-9]+,[0-9]+,[0-9]+,[0-9]+$',
    )


class ObjectRequest(BaseModel):
    id: str = Field(
        title='id',
        description='Identifier of the request. If empty, a UUID will be generated',
        default='',
    )
    min_confidence: float = Field(
        title='min_confidence',
        description='Confidence threshold (default=0.8)',
        default=0.8,
        ge=0,
        le=1,
    )
    max_objects: int = Field(
        title='max_objects',
        description='Maximum number of objects to retrieve (default=1)',
        default=1,
    )
    source: HttpUrl | str = Field(
        title='source',
        description='HTTP(S) URL to image or reference to file in local image directory',
    )
    service: RequestService = Field(
        title='service',
        description='Name of the object detection service',
        default=RequestService.internal,
    )
    service_key: str = Field(
        title='service_key',
        description='API key of the external service',
        default='',
    )
    annotation_type: AnnotationType = Field(
        title='annotation_type',
        description='Type of annotation standard to be used',
        default=AnnotationType.internal,
    )


class ColorRequest(BaseModel):
    id: str = Field(
        title='id',
        description='Identifier of the request. If empty, a UUID will be generated',
        default='',
    )
    max_colors: int = Field(
        title='max_colors',
        description='Maximum number of colors to retrieve (default=3)',
        default=3,
    )
    min_area: float = Field(
        title='min_area',
        description='Minimum share of a given color in the total area of the depicted object (default=0.15)',
        default=0.15,
        ge=0.00,
        le=1.00,
    )
    ld_source: LDSource = Field(
        title='ld_source',
        description='LD source from which the color URIs are given: Fashion Thesaurus or Wikidata (default = FT)',
        default=LDSource.ft,
    )
    service: RequestService = Field(
        title='service',
        description='Name of the color detection service',
        default=RequestService.internal,
    )
    source: HttpUrl | str = Field(
        title='source',
        description='HTTP(S) URL to image or reference to file in local image directory',
    )
    foreground_detection: bool = Field(
        title='foreground_detection',
        description='Whether the tool should apply foreground detection for the given area (default=True)',
        default=True,
    )
    selector: ColorSelector = Field(
        title='selector', description='Selector for the image'
    )
    annotation_type: AnnotationType = Field(
        title='annotation_type',
        description='Type of annotation standard to be used',
        default=AnnotationType.internal,
    )


class GoogleSource(BaseModel):
    imageUri: HttpUrl = Field(
        title='Google Image source URI', description='Source URI of the image'
    )


class GoogleImage(BaseModel):
    source: GoogleSource = Field(
        title='Google Image source',
        description='Source of the image',
    )


class GoogleContent(BaseModel):
    content: str = Field(
        title='Base64 encoded image',
        description='The base64 representation (ASCII string) of your binary image data',
        default='',
    )


class GoogleFeature(BaseModel):
    maxResults: int = Field(
        title='Maximum results', description='Maximum results to be retrieved'
    )
    type: GoogleFeatureType = Field(
        title='Feature type', description='Type of feature to be retrieved'
    )


class GoogleVisionRequest(BaseModel):
    image: GoogleImage | GoogleContent = Field(
        title='Google Image (URL) or base64 encoded image content',
        description='Meta data of the image',
    )
    features: List[GoogleFeature] = Field(
        title='Features', description='Features to be applied'
    )


class NtuaCreator(BaseModel):
    id: HttpUrl = Field(
        title='id',
        description='Creator IRI (optional)',
        default=HttpUrl('https://github.com/datable-be/AI4C_ContentAnalysis'),
    )
    type: NtuaEntity = Field(
        title='type', description='Creator type', default=NtuaEntity.software
    )
    name: str = Field(
        title='name',
        description='Creator name (optional)',
    )


class NtuaBody(BaseModel):
    type: str = Field(
        title='type',
        description='Body type',
        default='TextualBody',
    )
    value: str = Field(
        title='value',
        description='Body value',
        default='',
    )
    language: str = Field(
        title='language',
        description='Body language',
        default='en',
    )


class NtuaTarget(BaseModel):
    source: HttpUrl | str = Field(
        title='source',
        description='URI of the object the annotation refers to',
    )


class NtuaValidationReview(BaseModel):
    type: NtuaReviewType = Field(
        title='type',
        description='Review type',
        default=NtuaReviewType.validation,
    )
    recommendation: NtuaRecommendationType = Field(
        title='recommendation',
        description='Review recommendation',
        default=NtuaRecommendationType.accept,
    )


class NtuaRatingReview(BaseModel):
    type: NtuaReviewType = Field(
        title='type',
        description='Review type',
        default=NtuaReviewType.rating,
    )
    score: float = Field(
        title='score',
        description='Review score',
        ge=0,
        le=1,
    )


class NtuaAnnotation(BaseModel):
    id: HttpUrl = Field(
        title='id',
        description='Annotation IRI',
    )
    type: str = Field(
        title='type',
        description="The rdf:type of the annotation object and should normally be 'Annotation'",
        default='Annotation',
    )
    created: str = Field(
        title='created',
        description="The date on which the annotation was created by a tool or a human, format = '2022-07-20T08:08:10'",
    )
    creator: NtuaCreator = Field(
        title='creator', description='Annotation creator'
    )
    body: List[HttpUrl] | List[NtuaBody] = Field(
        title='body',
        description='Actual annotation value (either IRI or body object)',
    )
    confidence: float | None = Field(
        title='confidence',
        description='Confidence of the annotation creator for the particular annotation(s)',
        ge=0,
        le=1,
    )
    target: NtuaTarget = Field(
        title='target',
        description='The object that gave rise to the annotation and the annotation value refers to',
    )
    review: NtuaValidationReview | NtuaRatingReview = Field(
        title='review',
        description='Provides information about the annotation validation status',
    )
    scope: str = Field(
        title='scope',
        description='The property the annotation should be encoded as. Should be an IRI',
        default='dc:spatial',
    )


class NtuaResponse(BaseModel):
    context: Dict = Field(
        title='context',
        serialization_alias='@context',
        description='Context',
        default=NTUA_CONTEXT,
    )
    graph: List[NtuaAnnotation] = Field(
        title='graph',
        serialization_alias='@graph',
        description='Annotation objects',
    )


class EuropeanaCreator(NtuaCreator):
    ...


class EuropeanaValidationReview(NtuaValidationReview):
    ...


class EuropeanaAnnotation(BaseModel):
    id: HttpUrl = Field(
        title='id',
        description='Annotation IRI',
    )
    type: str = Field(
        title='type',
        description="The rdf:type of the annotation object and should normally be 'Annotation'",
        default='Annotation',
    )
    created: str = Field(
        title='created',
        description="The date on which the annotation was created by a tool or a human, format = '2024-01-31T14:08:07Z'",
    )
    creator: EuropeanaCreator = Field(
        title='creator', description='Annotation creator'
    )
    motivation: str = Field(
        title='motivation',
        description='',
        default='tagging',
    )
    body: HttpUrl | str = Field(
        title='body',
        description='Body is the actual annotation value. It can be either a iri or a literal',
    )
    confidence: float | None = Field(
        title='confidence',
        description='Confidence of the annotation creator for the particular annotation(s)',
        ge=0,
        le=1,
    )
    review: EuropeanaValidationReview = Field(
        title='review',
        description='Provides information about the annotation validation status',
    )


class EuropeanaTarget(BaseModel):
    # to do: what is this?
    scope: HttpUrl | str = Field(
        title='scope',
        description='',
    )
    source: HttpUrl | str = Field(
        title='source',
        description='URI of the object the annotation refers to',
    )


class EuropeanaStatement(BaseModel):
    id: HttpUrl = Field(
        title='id',
        description='Statement IRI',
    )
    dctformat: List[HttpUrl | str] = Field(
        title='dct:format',
        description='dct:format statements',
    )


class EuropeanaBody(BaseModel):
    type: str = Field(title='type', description='', default='GraphBody')
    purpose: str = Field(title='purpose', description='', default='asserting')
    statements: EuropeanaStatement = Field(
        title='statements',
        description='statement object',
    )


class EuropeanaResponse(BaseModel):
    context: Dict = Field(
        title='context',
        serialization_alias='@context',
        description='Context',
        default=EUROPEANA_CONTEXT,
    )
    id: HttpUrl = Field(
        title='id',
        description='Annotation IRI',
    )
    type: str = Field(
        title='type',
        description='Annotation type is the rdf:type of the annotation object and should normally be "Annotation"',
        default='Annotation',
    )
    created: str = Field(
        title='created',
        description="The date on which the annotation was created by a tool or a human, format = '2024-01-30T14:09:00Z'",
    )
    creator: EuropeanaCreator = Field(
        title='creator', description='Annotation creator'
    )
    # to do: what is the difference with created/creator?
    generated: str = Field(
        title='generated',
        description='',
    )
    generator: EuropeanaCreator = Field(title='generator', description='')
    motivation: str = Field(
        title='motivation',
        description='',
        default='describing',
    )
    derivedFrom: List[EuropeanaAnnotation] = Field(
        title='derivedFrom',
        description='derivedFrom objects',
    )
    body: EuropeanaBody = Field(title='body', description='Annotation body')
    # to do: what is this?
    target: HttpUrl | str = Field(
        title='target',
        description='',
    )
