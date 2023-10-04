from classes import ObjectRequest
from cv2.dnn import Net
from api.v1.object.internal import detection as internal_detection
from api.v1.object.google import detection as google_detection


def detection(object_request: ObjectRequest, net: Net, settings: dict):

    if object_request.service == "GoogleVision":
        return google_detection(object_request, settings)
    else:
        return internal_detection(object_request, net, settings)
