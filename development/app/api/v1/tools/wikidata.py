from constants import WIKIDATA_URIS_FILE, WIKIDATA_SEARCH_API
from fastapi import HTTPException
from requests import get
from json import load, dumps


def check_for_concept(concept: str) -> str:
    """
    Check Wikidata API for URI
    """
    url = (
        WIKIDATA_SEARCH_API
        + f'{concept}&format=json&language=en&uselang=en&type=item&limit=10'
    )
    response = None
    try:
        response = get(url)
    except Exception as e:
        if response:
            code = response.status_code
        else:
            code = 404
        raise HTTPException(status_code=code, detail=str(e))
    data = response.json()

    search_info = data.get('searchinfo', {})
    search_matches = data.get('search', [])
    search_text = search_info.get('search', '')

    for entry in search_matches:
        match = entry.get('match', {})
        if (
            match.get('type') == 'label' or match.get('type') == 'alias'
        ) and match.get('text') == search_text:
            uri = entry.get('concepturi')
            return uri

    return ''


def retrieve_concept_uri(concept: str) -> str:
    """
    Get the Wikidata URI of a concept.
    Check database and update if needed
    """

    with open(WIKIDATA_URIS_FILE, 'r') as reader:
        wikidata_uris = load(reader)

    if concept in wikidata_uris:
        return wikidata_uris[concept]

    uri = check_for_concept(concept)

    if uri == '':
        return uri

    wikidata_uris[concept] = uri
    with open(WIKIDATA_URIS_FILE, 'w') as writer:
        writer.write(dumps(wikidata_uris))

    return uri
