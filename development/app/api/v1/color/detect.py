DUMMY_RESPONSE = {
    "@context": {
        "as": "https://www.w3.org/ns/activitystreams#",
        "dc": "http://purl.org/dc/terms/",
        "dce": "http://purl.org/dc/elements/1.1/",
        "foaf": "http://xmlns.com/foaf/0.1/",
        "oa": "http://www.w3.org/ns/oa#",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "soa": "http://sw.islab.ntua.gr/annotation/",
        "id": {"@id": "@id", "@type": "@id"},
        "type": {"@id": "@type", "@type": "@id"},
        "value": "rdf:value",
        "created": {"@id": "dc:created", "@type": "xsd:dateTime"},
        "creator": {"@id": "dc:creator", "@type": "@id"},
        "language": "dc:language",
        "Software": "as:Application",
        "name": "foaf:name",
        "Annotation": "oa:Annotation",
        "TextPositionSelector": "oa:TextPositionSelector",
        "TextualBody": "oa:TextualBody",
        "body": {"@id": "oa:hasBody", "@type": "@id"},
        "scope": {"@id": "oa:hasScope", "@type": "@id"},
        "selector": {"@id": "oa:hasSelector", "@type": "@id"},
        "source": {"@id": "oa:hasSource", "@type": "@id"},
        "target": {"@id": "oa:hasTarget", "@type": "@id"},
        "Literal": "soa: Literal ",
    },
    "@graph": [
        {
            "id": "http://datable.be/color-annotations/123",
            "type": "Annotation",
            "created": "2023-09-30",
            "creator": {
                "id": "https://github.com/hvanstappen/AI4C_color-detector",
                "type": "Software",
                "name": "AI4C color detector",
            },
            "body": [
                "http://thesaurus.europeanafashion.eu/thesaurus/10403",
                "http://thesaurus.europeanafashion.eu/thesaurus/11098",
                "http://thesaurus.europeanafashion.eu/thesaurus/10404",
            ],
            "target": {
                "source": "http://mint-projects.image.ntua.gr/europeana-fashion/500208081"
            },
        }
    ],
}


def detection():
    return DUMMY_RESPONSE
