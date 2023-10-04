from classes import ObjectRequest
from constants import COCO_LABELS
from cv2.dnn import Net
import cv2
from api.v1.object.tools import load_cv2_image_from_url

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


def detection(object_request: ObjectRequest, net: Net, settings: dict):

    # Read image
    image = load_cv2_image_from_url(str(object_request.source))
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
    for detection in output[0, 0, :, :]:
        confidence = detection[2]

        # Continue if the confidence of the model is lower than 40%,
        if confidence < 0.4:
            continue

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

        # Draw the bounding box of the object
        cv2.rectangle(image, box[:2], box[2:], (0, 255, 0), thickness=2)

        # Extract the ID of the detected object to get its name
        class_id = int(detection[1])

        # Get the object label
        label = f"{COCO_LABELS[class_id - 1].capitalize()}"

        # Add size to object to sublist
        detected_object = [size, box, label]

        # Add to nested list
        objects.append(detected_object)

        if settings.get("debug"):
            # Draw the name of the predicted object together with the probability
            prediction = f"{label} {confidence * 100:.2f}%"
            cv2.putText(
                image,
                prediction,
                (box[0], box[1] + 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

    if settings.get("debug"):
        print("Objects: ", objects)
        cv2.imshow("Image", image)
        cv2.waitKey(10000)

    #  # find largest object
    #  biggest_object = max(objects)
    #  print(biggest_object)
    #
    #  box = biggest_object[1]
    #  print("box of biggest object: ", box)

    return DUMMY_RESPONSE
