import json
import requests
import sys


URL = 'http://0.0.0.0:8000/v1/color'


EXAMPLES = {
    'airplane': 'https://github.com/zafarRehan/object_detection_COCO/blob/main/test_image.png?raw=true',
    'pink_image': 'https://github.com/datable-be/AI4C_colordetector/blob/main/examples/RS41124_T3796_0004-hpr_8_enhanced.jpg?raw=true',
    'red_manequin': 'https://github.com/datable-be/AI4C_colordetector/blob/main/examples/M.PL.0047.01.jpg?raw=true',
    'logo_coca_cola': 'https://static.independent.co.uk/s3fs-public/thumbnails/image/2018/08/09/10/coco-cola.jpg',
    'dog_and_horse': 'https://github.com/datable-be/AI4C_colordetector/blob/main/examples/image3.jpg?raw=true',
    'sheep_in_a_meadow': 'https://previews.123rf.com/images/goldika/goldika1310/goldika131000020/23257505-one-sheep-on-green-autumn-to-the-meadow.jpg',
}


REQUEST = """{
    "max_colors": 3,
    "min_area": 0.15,
    "foreground_detection": true,
    "service": "internal",
    "selector" : {
      "type" : "FragmentSelector",
      "conformsTo" : "http://www.w3.org/TR/media-frags/",
      "value" : "xywh=percent:50,50,100,100"
    },
    "ld_source": "Wikidata",
    "source":"https://previews.123rf.com/images/goldika/goldika1310/goldika131000020/23257505-one-sheep-on-green-autumn-to-the-meadow.jpg",
    "annotation_type": "ntua"
}"""


def json_pretty_print(json_string: str):
    print(json.dumps(json.loads(json_string), indent=4))


print('POST', URL)
print('REQUEST = ')
json_pretty_print(REQUEST)

response = requests.post(URL, REQUEST, timeout=30)
if response.status_code == 200:
    print('RESPONSE = ')
    json_pretty_print(response.text)
else:
    sys.exit('ERROR = ' + response.text)
