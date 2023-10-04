# Test object detection on local machine, i.e. show detected images

from constants import NET
from classes import ObjectRequest
from api.v1.object.internal import detection as internal_detection

settings = {}
settings["debug"] = True

request = ObjectRequest(
    id="http://example.com/images/123",
    min_confidence=0.8,
    max_objects=1,
    source="https://github.com/datable-be/AI4C_ContentAnalysis/blob/da9995b6a2a2795bb2d2cce0695417efc5b674f3/scripts/color-detector/examples/39355scr_0ed48a9fe99bfe5_e183b86fc24d9855178e546b5f96c28a.jpg?raw=true",
    service="internal",
    service_key="****",
)

print(internal_detection(request, NET, settings))
