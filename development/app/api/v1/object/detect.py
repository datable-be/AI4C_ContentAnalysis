from classes import ObjectRequest, RequestService
from cv2.dnn import Net
from api.v1.object.internal import detection as internal_detection
from api.v1.object.google import detection as google_detection


def detection(object_request: ObjectRequest, net: Net, settings: dict):
    # internal service if key is invalid
    if object_request.service_key == "" or not object_request.service_key:
        object_request.service = RequestService.internal
        return internal_detection(object_request, net, settings)

    if object_request.service == RequestService.googlevision:
        return google_detection(object_request, settings)
    else:
        return internal_detection(object_request, net, settings)
