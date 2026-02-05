import json
import requests
import sys

URL = 'http://0.0.0.0:8000/v1/object'

EXAMPLES = {
    'airplane': 'https://github.com/zafarRehan/object_detection_COCO/blob/main/test_image.png?raw=true',
    'pink_image': 'https://github.com/datable-be/AI4C_colordetector/blob/main/examples/RS41124_T3796_0004-hpr_8_enhanced.jpg?raw=true',
    'red_manequin': 'https://github.com/datable-be/AI4C_colordetector/blob/main/examples/M.PL.0047.01.jpg?raw=true',
    'logo_coca_cola': 'https://static.independent.co.uk/s3fs-public/thumbnails/image/2018/08/09/10/coco-cola.jpg',
    'dog_and_horse': 'https://github.com/datable-be/AI4C_colordetector/blob/main/examples/image3.jpg?raw=true',
    'sheep_in_a_meadow': 'https://previews.123rf.com/images/goldika/goldika1310/goldika131000020/23257505-one-sheep-on-green-autumn-to-the-meadow.jpg',
    'local_file': 'example.jpg',
}

BASE_REQUEST = {
    'min_confidence': 0.4,
    'max_objects': 10,
    'service': 'internal',
    'service_key': '****',
    'annotation_type': 'europeana',
}


def json_pretty_print(data):
    print(json.dumps(data, indent=4))


print('POST', URL)

for name, source in EXAMPLES.items():
    print(f'\n=== Example: {name} ===')

    payload = {
        **BASE_REQUEST,
        'source': source,
    }

    print('REQUEST =')
    json_pretty_print(payload)

    try:
        response = requests.post(URL, json=payload, timeout=10)
    except requests.RequestException as e:
        print('REQUEST FAILED:', e)
        continue

    if response.status_code == 200:
        print('RESPONSE =')
        json_pretty_print(response.json())
    else:
        print(f'ERROR ({response.status_code}) = {response.text}')
