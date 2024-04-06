from os.path import join

from cv2 import rectangle, putText, imwrite, FONT_HERSHEY_SIMPLEX
from cv2.dnn import blobFromImage, Net

from classes import ObjectRequest
from constants import COCO_LABELS, COCO_2_WIKIDATA, TEMP_DIR
from api.v1.tools.source import (
    load_cv2_image_from_source,
    extension_from_source,
)
from api.v1.tools.path import housekeeping
from api.v1.tools.tools import hash_object


ANNOTATION_COLOR = (0, 255, 0)  # bright green

MODEL_RESPONSE = {
    '@context': {},
    '@graph': [
        {
            'id': 'http://datable.be/color-annotations/123',
            'type': 'Annotation',
            'created': '2023-09-30',
            'creator': {
                'id': 'https://github.com/hvanstappen/AI4C_object-detector',
                'type': 'Software',
                'name': 'AI4C object detector',
            },
            'body': [
                {'source': 'http://www.wikidata.org/entity/Q200539'},
                {
                    'type': 'TextualBody',
                    'purpose': 'tagging',
                    'value': 'dress',
                    'language': 'en',
                },
            ],
            'target': {
                'source': 'http://mint-projects.image.ntua.gr/europeana-fashion/500208081',
                'selector': {
                    'type': 'FragmentSelector',
                    'conformsTo': 'http://www.w3.org/TR/media-frags/',
                    'value': 'xywh=percent:87,63,9,21',
                },
            },
            'confidence': 0.8,
        },
        {},
    ],
}


# ObjectRequest =
#      "id": "http://mint-projects.image.ntua.gr/europeana-fashion/500208081",
#      "min_confidence": 0.8,
#      "max_objects": 1,
#      "source": "http://example.com/images/123.jpg",
#      "service":"internal",
#      "service_key":"****"
def detection(
    request: ObjectRequest, net: Net, settings: dict, url_source: bool
) -> dict:
    if settings.get('dummy'):
        return MODEL_RESPONSE

    request.source = str(request.source)

    # Request identifier
    identifier = hash_object(request)

    # Read image, resize (height value)
    image = load_cv2_image_from_source(
        request.source, resize_pixels=200, url=url_source
    )
    image_height = image.shape[0]
    image_width = image.shape[1]

    # Create a blob from the image
    blob = blobFromImage(
        image=image,
        scalefactor=1.0 / 127.5,
        size=(320, 320),
        mean=[127.5, 127.5, 127.5],
    )

    # Pass the blob through our network and get the output predictions
    net.setInput(blob)
    output = net.forward()  # shape: (1, 1, 100, 7)

    # Loop over the number of detected objects
    # output[0, 0, :, :] has a shape of: (100, 7)
    objects = []
    count = 0

    for detection in output[0, 0, :, :]:
        confidence = float(detection[2])

        if confidence < request.min_confidence:
            continue

        count += 1

        # Perform element-wise multiplication to get
        # the (x, y) coordinates of the bounding box
        # Meaning of box [0, 1, 2, 3] indices
        # 0 = horizontal position (left-to-right) of the top-left corner (in px)
        # 1 = vertical position (top-to-bottom) of the top-left corner (in px)
        # 2 = horizontal position (left-to-right) of the bottom-right corner (in px)
        # 3 = vertical position (top-to-bottom) of the bottom-right corner (in px)
        box = [
            int(a * b)
            for a, b in zip(
                detection[3:7],
                [image_width, image_height, image_width, image_height],
            )
        ]
        horizontal_top_left = round((box[0] / image_width * 100), 2)
        vertical_top_left = round((box[1] / image_height * 100), 2)
        horizontal_bottom_right = round((box[2] / image_width * 100), 2)
        vertical_bottom_right = round((box[3] / image_height * 100), 2)
        percentages = [
            horizontal_top_left,
            vertical_top_left,
            horizontal_bottom_right,
            vertical_bottom_right,
        ]

        # Calculate box size
        size_width = box[2] - box[0]
        size_height = box[3] - box[1]
        size = size_width * size_height

        # Before altering image, make a deep copy,
        # because cv2 uses pointers under the hood,
        # so the original image is changed!
        image_copy = image.copy()

        # Draw the bounding box of the object
        # pt1 represents the top-left corner, and pt2 represents the bottom-right corner of the rectangle.
        annotated_image = rectangle(
            img=image_copy,
            pt1=box[:2],
            pt2=box[2:],
            color=ANNOTATION_COLOR,
            thickness=2,
        )

        # Extract the ID of the detected object to get its name
        class_id = int(detection[1])

        label = COCO_LABELS[class_id - 1]

        # Add data to result
        detected_object = {
            'confidence': confidence,
            'size': size,
            'box_px': box,
            'box_%': percentages,
            'coco_label': label,
            'wikidata': COCO_2_WIKIDATA.get(label),
        }

        if settings.get('debug'):
            # Draw the name of the predicted object together with the probability
            prediction = f'{label} {confidence * 100:.2f}%'
            annotated_image = putText(
                img=annotated_image,
                text=prediction,
                org=(box[0], box[1] + 15),
                fontFace=FONT_HERSHEY_SIMPLEX,
                fontScale=0.5,
                color=ANNOTATION_COLOR,
                thickness=2,
            )

            # Save image
            housekeeping(TEMP_DIR)
            basename = (
                identifier
                + '_'
                + str(count)
                + extension_from_source(request.source)
            )
            filepath = join(TEMP_DIR, basename)
            print(filepath, ' saved')
            imwrite(filepath, annotated_image)
            url = (
                settings['host']
                + ':'
                + str(settings['port'])
                + '/image?img='
                + basename
            )
            detected_object['annotated_image'] = url

        objects.append(detected_object)

    # Sort result on object size
    sorted_objects = sorted(objects, key=lambda x: x['size'], reverse=True)

    # Filter max_objects
    if len(sorted_objects) > request.max_objects:
        sorted_objects = sorted_objects[0 : request.max_objects]

    result = {}
    result['request_id'] = request.id
    result['source'] = request.source
    result['data'] = sorted_objects

    return result
