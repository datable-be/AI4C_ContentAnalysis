import os
import cv2

from classes import ObjectRequest
from constants import COCO_LABELS, TEMP_DIR
from api.v1.object.tools import (
    load_cv2_image_from_url,
    extension_from_url,
    housekeeping,
    hash_object
)

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


#      "id": "http://mint-projects.image.ntua.gr/europeana-fashion/500208081",
#      "min_confidence": 0.8,
#      "max_objects": 1,
#      "source": "http://example.com/images/123.jpg",
#      "service":"GoogleVision",
#      "service_key":"****"


def detection(request: ObjectRequest, net: cv2.dnn.Net, settings: dict):

    # Request identifier
    identifier = hash_object(request)

    # Read image
    url = str(request.source)
    image = load_cv2_image_from_url(url)
    # image = cv2.resize(image, (640, 480))
    image_height = image.shape[0]
    image_width = image.shape[1]

    # Create a blob from the image
    blob = cv2.dnn.blobFromImage(
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
        box = [
            int(a * b)
            for a, b in zip(
                detection[3:7],
                [image_width, image_height, image_width, image_height],
            )
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
        annotated_image = cv2.rectangle(
            image_copy, box[:2], box[2:], (0, 255, 0), thickness=2)

        # Extract the ID of the detected object to get its name
        class_id = int(detection[1])

        label = f"{COCO_LABELS[class_id - 1].capitalize()}"

        detected_object = {
            "confidence": confidence,
            "size": size,
            "box": box,
            "label": label,
        }

        if settings.get("debug"):
            # Draw the name of the predicted object together with the probability
            prediction = f"{label} {confidence * 100:.2f}%"
            annotated_image = cv2.putText(
                img=annotated_image,
                text=prediction,
                org=(box[0], box[1] + 15),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5,
                color=(0, 255, 0),
                thickness=2,
            )

            housekeeping(TEMP_DIR)
            basename = identifier + "_" + str(count) + extension_from_url(url)
            filepath = os.path.join(TEMP_DIR, basename)
            cv2.imwrite(filepath, annotated_image)
            detected_object["annotated_image"] = basename

        objects.append(detected_object)

    #  if settings.get("debug"):
    #  cv2.imshow("Image", image)
    #  cv2.waitKey(10000)

    # Sort result on object size
    sorted_objects = sorted(objects, key=lambda x: x["size"], reverse=True)
    # Filter max_objects
    if len(sorted_objects) > request.max_objects:
        sorted_objects = sorted_objects[0:request.max_objects]

    result = {}
    result["id"] = identifier
    result["data"] = sorted_objects

    return result
