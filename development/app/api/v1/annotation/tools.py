from datetime import datetime, timezone
from requests import get, Response

# from constants import WIKIDATA_SPARQL_ENDPOINT

WIKIDATA_SPARQL_ENDPOINT = 'https://query.wikidata.org/sparql'


def get_utc_timestamp():
    # Get the current UTC time
    current_time = datetime.now(tz=timezone.utc)

    # Format the time as xsd:dateTime with "Z" for UTC timezone
    formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'

    return formatted_time


def sparql(query: str, endpoint: str) -> Response:
    """
    Execute a query to a SPARQL endpoint
    """
    try:
        return get(endpoint, params={'format': 'json', 'query': query})
    except Exception as e:
        raise e


def google_mid_to_wikidata(mid: str) -> str:
    """
    Translate a Google "mid" (Freebase) identifier to Wikidata Q entity
    """
    query = f"""SELECT DISTINCT ?item ?itemLabel WHERE {{
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
          {{
            SELECT DISTINCT ?item WHERE {{
              ?item p:P646 ?statement0.
              ?statement0 ps:P646 "{mid}".
            }}
            LIMIT 1
          }}
        }}
        """

    sparql_response = sparql(query, WIKIDATA_SPARQL_ENDPOINT)
    sparql_result = sparql_response.json()
    if not 'bindings' in sparql_result['results']:
        return ''
    else:
        q_entity = sparql_result['results']['bindings'][0]['item']['value']

    return q_entity
