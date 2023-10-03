DUMMY_RESPONSE = {
    "@context": {},
    "@graph": [
        {
            "id": "http://datable.be/color-annotations/123",
            "type": "Annotation",
            "created": "2023-09-30",
            "creator": {
                "id": "https://github.com/hvanstappen/AI4C_object-detector",
                "type": "Software",
                "name": "AI4C object detector",
            },
            "body": [
                {"source": "http://www.wikidata.org/entity/Q200539"},
                {
                    "type": "TextualBody",
                    "purpose": "tagging",
                    "value": "dress",
                    "language": "en",
                },
            ],
            "target": {
                "source": "http://mint-projects.image.ntua.gr/europeana-fashion/500208081",
                "selector": {
                    "type": "FragmentSelector",
                    "conformsTo": "http://www.w3.org/TR/media-frags/",
                    "value": "xywh=percent:87,63,9,21",
                },
            },
            "confidence": 0.8,
        },
        {},
    ],
}


def detection(settings: dict):

    return DUMMY_RESPONSE
