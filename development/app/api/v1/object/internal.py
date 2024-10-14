efrom os.path import join

from cv2 import rectangle, putText, imwrite, FONT_HERSHEY_SIMPLEX
from cv2.dnn import blobFromImage, Net

from classes import ObjectRequest
from constants import COCO_LABELS, COCO_2_WIKIDATA, TEMP_DIR
from api.v1.tools.source import (
    load_cv2_image_from_source,
    identify_image_type,
)
from api.v1.tools.path import filename_to_url
from api.v1.tools.tools import hash_object


ANNOTATION_COLOR = (0, 255, 0)  # bright green


def detection(
    request: ObjectRequest, net: Net, settings: dict, url_source: bool
) -> dict:
    if settings.get('dummy'):
        from constants import MODEL_RESPONSE

        return MODEL_RESPONSE

    request.source = str(request.source)

    # Request identifier
    identifier = hash_object(request)

    # Read image, resize (height value)
    extension, data = identify_image_type(request.source, url=url_source)
    image = load_cv2_image_from_source(data, resize_pixels=200, url=url_source)
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

        # Calculate relative box size
        rel_size_width = horizontal_bottom_right - horizontal_top_left
        rel_size_height = vertical_bottom_right - vertical_top_left
        rel_size = rel_size_width * rel_size_height
        rel_size = rel_size / 10000

        # Add data to result
        if rel_size > 0.2: #select only larger images

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


            detected_object = {
                'confidence': confidence,
                'size': rel_size,
                'box_px': box,
                'box_%': percentages,
                'coco_label': label,
                'wikidata': COCO_2_WIKIDATA.get(label),
            }

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
            basename = identifier + '_' + str(count) + extension
            filepath = join(TEMP_DIR, basename)
            imwrite(filepath, annotated_image)
            print(filepath, ' saved')
            detected_object['annotated_image'] = filename_to_url(basename)

            objects.append(detected_object)

    # Sort result on object size
    sorted_objects = sorted(objects, key=lambda x: x['confidence'], reverse=True)


    # Filter max_objects
    if len(sorted_objects) > request.max_objects:
        sorted_objects = sorted_objects[0 : request.max_objects]

    result = {}
    result['request_id'] = request.id
    result['source'] = request.source
    result['data'] = {'objects': sorted_objects}

    return result
