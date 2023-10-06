import json
import cv2

with open("info.json", "r") as f:
    INFO = json.load(f)

with open("settings.json", "r") as f:
    SETTINGS = json.load(f)

DESCRIPTION = """
AI4C API helps you detect objects and colors in images. 🚀

## Object

...

## Color

...
"""

# Tempdir for saving images
# (saved on the machine's filesystem, usually in /var/lib/docker)
# Do not change!

TEMP_DIR = "/tmp"


# Load the MobileNet SSD model trained on the COCO dataset

weights = "ssd_mobilenet/frozen_inference_graph.pb"
model = "ssd_mobilenet/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
NET = cv2.dnn.readNetFromTensorflow(weights, model)


# load the class labels the model was trained on

COCO_LABELS = [
    "person",
    "bicycle",
    "car",
    "motorcycle",
    "airplane",
    "bus",
    "train",
    "truck",
    "boat",
    "traffic light",
    "fire hydrant",
    "street sign",
    "stop sign",
    "parking meter",
    "bench",
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "hat",
    "backpack",
    "umbrella",
    "shoe",
    "eye glasses",
    "handbag",
    "tie",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sports ball",
    "kite",
    "baseball bat",
    "baseball glove",
    "skateboard",
    "surfboard",
    "tennis racket",
    "bottle",
    "plate",
    "wine glass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "carrot",
    "hot dog",
    "pizza",
    "donut",
    "cake",
    "chair",
    "couch",
    "potted plant",
    "bed",
    "mirror",
    "dining table",
    "window",
    "desk",
    "toilet",
    "door",
    "tv",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cell phone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "blender",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddy bear",
    "hair drier",
    "toothbrush",
]

COCO_2_WIKIDATA = {
    "airplane": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q197",
        "wikidata_label": "airplane",
        "wikidata_description": "powered fixed-wing aircraft",
        "wikidata_concept": "Q197",
    },
    "apple": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q89",
        "wikidata_label": "apple",
        "wikidata_description": "fruit of the apple tree",
        "wikidata_concept": "Q89",
    },
    "backpack": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q5843",
        "wikidata_label": "backpack",
        "wikidata_description": "bag carried on one's back",
        "wikidata_concept": "Q5843",
    },
    "banana": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q503",
        "wikidata_label": "banana",
        "wikidata_description": "elongated, edible fruit produced by several kinds of large herbaceous flowering plants in the genus Musa",
        "wikidata_concept": "Q503",
    },
    "baseball bat": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q809910",
        "wikidata_label": "baseball bat",
        "wikidata_description": "club used for baseball, or as a weapon",
        "wikidata_concept": "Q809910",
    },
    "baseball glove": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q809894",
        "wikidata_label": "baseball glove",
        "wikidata_description": "large leather glove worn by baseball players",
        "wikidata_concept": "Q809894",
    },
    "bear": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q30090244",
        "wikidata_label": "bear",
        "wikidata_description": "large carnivoran mammal of the family Ursidae",
        "wikidata_concept": "Q30090244",
    },
    "bed": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q42177",
        "wikidata_label": "bed",
        "wikidata_description": "piece of furniture used as a place to sleep or relax",
        "wikidata_concept": "Q42177",
    },
    "bench": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q204776",
        "wikidata_label": "bench",
        "wikidata_description": "piece of furniture on which several people may sit at the same time",
        "wikidata_concept": "Q204776",
    },
    "bicycle": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q11442",
        "wikidata_label": "bicycle",
        "wikidata_description": "pedal-driven two-wheel vehicle",
        "wikidata_concept": "Q11442",
    },
    "bird": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q5113",
        "wikidata_label": "bird",
        "wikidata_description": "class of vertebrates",
        "wikidata_concept": "Q5113",
    },
    "blender": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q501862",
        "wikidata_label": "blender",
        "wikidata_description": "type of home appliance",
        "wikidata_concept": "Q501862",
    },
    "boat": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q35872",
        "wikidata_label": "boat",
        "wikidata_description": "smaller watercraft",
        "wikidata_concept": "Q35872",
    },
    "book": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q571",
        "wikidata_label": "book",
        "wikidata_description": "medium for recording information (words or images) typically on bound pages or more abstractly in electronic or audio form",
        "wikidata_concept": "Q571",
    },
    "bottle": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q80228",
        "wikidata_label": "bottle",
        "wikidata_description": "cylindrical container",
        "wikidata_concept": "Q80228",
    },
    "bowl": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q153988",
        "wikidata_label": "bowl",
        "wikidata_description": "round, open-top container frequently used as tableware",
        "wikidata_concept": "Q153988",
    },
    "broccoli": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q47722",
        "wikidata_label": "broccoli",
        "wikidata_description": "edible green plant in the cabbage family",
        "wikidata_concept": "Q47722",
    },
    "bus": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q5638",
        "wikidata_label": "bus",
        "wikidata_description": "large road vehicle for transporting people",
        "wikidata_concept": "Q5638",
    },
    "cake": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q13276",
        "wikidata_label": "cake",
        "wikidata_description": "baked dessert",
        "wikidata_concept": "Q13276",
    },
    "car": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q1420",
        "wikidata_label": "motor car",
        "wikidata_description": "motorized road vehicle designed to carry one to eight people rather than primarily goods",
        "wikidata_concept": "Q1420",
    },
    "carrot": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q81",
        "wikidata_label": "carrot",
        "wikidata_description": "root vegetable, usually orange in color",
        "wikidata_concept": "Q81",
    },
    "cat": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q146",
        "wikidata_label": "house cat",
        "wikidata_description": "domesticated feline",
        "wikidata_concept": "Q146",
    },
    "chair": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q15026",
        "wikidata_label": "chair",
        "wikidata_description": "piece of furniture for sitting on",
        "wikidata_concept": "Q15026",
    },
    "clock": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q376",
        "wikidata_label": "clock",
        "wikidata_description": "instrument that measures the passage of time",
        "wikidata_concept": "Q376",
    },
    "couch": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q131514",
        "wikidata_label": "couch",
        "wikidata_description": "piece of furniture for seating two or more persons in the form of a bench with armrests",
        "wikidata_concept": "Q131514",
    },
    "cow": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q11748378",
        "wikidata_label": "cow",
        "wikidata_description": "adult female cattle",
        "wikidata_concept": "Q11748378",
    },
    "cup": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q81727",
        "wikidata_label": "cup",
        "wikidata_description": "vessel for liquids",
        "wikidata_concept": "Q81727",
    },
    "desk": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q1064858",
        "wikidata_label": "desk",
        "wikidata_description": "case furniture used as a worksurface, often in a school or office setting",
        "wikidata_concept": "Q1064858",
    },
    "dining table": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q115665141",
        "wikidata_label": "dining table",
        "wikidata_description": "table for dining, usually for formal meals",
        "wikidata_concept": "Q115665141",
    },
    "dog": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q144",
        "wikidata_label": "dog",
        "wikidata_description": "domestic animal",
        "wikidata_concept": "Q144",
    },
    "door": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q36794",
        "wikidata_label": "door",
        "wikidata_description": "flat, movable structure used to open and close an entrance",
        "wikidata_concept": "Q36794",
    },
    "elephant": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q7378",
        "wikidata_label": "elephant",
        "wikidata_description": "large terrestrial mammals with trunks from Africa and Asia",
        "wikidata_concept": "Q7378",
    },
    "fire hydrant": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q634299",
        "wikidata_label": "fire hydrant",
        "wikidata_description": "connection point by which firefighters can tap into a water supply",
        "wikidata_concept": "Q634299",
    },
    "fork": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q81881",
        "wikidata_label": "fork",
        "wikidata_description": "utensil to spear food",
        "wikidata_concept": "Q81881",
    },
    "giraffe": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q15083",
        "wikidata_label": "giraffe",
        "wikidata_description": "umbrella species of Giraffa",
        "wikidata_concept": "Q15083",
    },
    "handbag": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q467505",
        "wikidata_label": "handbag",
        "wikidata_description": "handled medium-to-large bag that is often fashionably designed, typically used by women, to hold personal items",
        "wikidata_concept": "Q467505",
    },
    "hat": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q80151",
        "wikidata_label": "hat",
        "wikidata_description": "shaped head covering, having a brim and a crown, or one of these",
        "wikidata_concept": "Q80151",
    },
    "horse": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q726",
        "wikidata_label": "horse",
        "wikidata_description": "domesticated four-footed mammal from the equine family",
        "wikidata_concept": "Q726",
    },
    "hot dog": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q181055",
        "wikidata_label": "hot dog",
        "wikidata_description": "sausage in bun, usually with toppings",
        "wikidata_concept": "Q181055",
    },
    "keyboard": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q1921606",
        "wikidata_label": "keyboard",
        "wikidata_description": "data input device",
        "wikidata_concept": "Q1921606",
    },
    "kite": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q42861",
        "wikidata_label": "kite",
        "wikidata_description": "tethered aircraft often tied with a rope or string.",
        "wikidata_concept": "Q42861",
    },
    "knife": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q32489",
        "wikidata_label": "knife",
        "wikidata_description": "tool with a cutting edge or blade",
        "wikidata_concept": "Q32489",
    },
    "laptop": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q3962",
        "wikidata_label": "laptop",
        "wikidata_description": "foldable portable personal computer for mobile use",
        "wikidata_concept": "Q3962",
    },
    "microwave": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q127956",
        "wikidata_label": "microwave oven",
        "wikidata_description": "kitchen cooking appliance",
        "wikidata_concept": "Q127956",
    },
    "mirror": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q146701",
        "wikidata_label": "mirror",
        "wikidata_description": "transparent structure in the eye",
        "wikidata_concept": "Q146701",
    },
    "motorcycle": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q34493",
        "wikidata_label": "motorcycle",
        "wikidata_description": "two- or three-wheeled motor vehicle",
        "wikidata_concept": "Q34493",
    },
    "mouse": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q7987",
        "wikidata_label": "mouse",
        "wikidata_description": "hand-held device used to move a pointer on a computer display",
        "wikidata_concept": "Q7987",
    },
    "orange": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q13191",
        "wikidata_label": "orange",
        "wikidata_description": "citrus fruit of the orange tree",
        "wikidata_concept": "Q13191",
    },
    "oven": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q36539",
        "wikidata_label": "oven",
        "wikidata_description": "enclosed chamber for heating other objects, often used to prepare food, finish ceramics, and purify substances",
        "wikidata_concept": "Q36539",
    },
    "parking meter": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q953960",
        "wikidata_label": "parking meter",
        "wikidata_description": "device",
        "wikidata_concept": "Q953960",
    },
    "person": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q215627",
        "wikidata_label": "person",
        "wikidata_description": "being that has certain capacities or attributes constituting personhood (avoid use with P31; use Q5 for humans)",
        "wikidata_concept": "Q215627",
    },
    "pizza": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q177",
        "wikidata_label": "pizza",
        "wikidata_description": "popular Italian dish with a flat dough-based base and toppings",
        "wikidata_concept": "Q177",
    },
    "plate": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q57216",
        "wikidata_label": "plate",
        "wikidata_description": "flat vessel on which food can be served",
        "wikidata_concept": "Q57216",
    },
    "potted plant": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q27993793",
        "wikidata_label": "potted plant",
        "wikidata_description": "plant grown in a container",
        "wikidata_concept": "Q27993793",
    },
    "refrigerator": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q37828",
        "wikidata_label": "refrigerator",
        "wikidata_description": "household or industrial appliance for preserving food at a low temperature",
        "wikidata_concept": "Q37828",
    },
    "remote": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q185091",
        "wikidata_label": "remote control",
        "wikidata_description": "system or device used to control other device remotely (or wirelessly)",
        "wikidata_concept": "Q185091",
    },
    "sandwich": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q28803",
        "wikidata_label": "sandwich",
        "wikidata_description": "any dish wherein bread serves as a container or wrapper for another food type; not to be confused with Q111836983 (the narrower sense of 'sandwich')",
        "wikidata_concept": "Q28803",
    },
    "scissors": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q40847",
        "wikidata_label": "scissors",
        "wikidata_description": "hand-operated cutting instrument",
        "wikidata_concept": "Q40847",
    },
    "sheep": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q7368",
        "wikidata_label": "sheep",
        "wikidata_description": "domesticated ruminant bred for meat, wool, and milk",
        "wikidata_concept": "Q7368",
    },
    "shoe": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q22676",
        "wikidata_label": "shoe",
        "wikidata_description": "footwear",
        "wikidata_concept": "Q22676",
    },
    "sink": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q140565",
        "wikidata_label": "sink",
        "wikidata_description": "bowl-shaped plumbing fixture used for washing hands",
        "wikidata_concept": "Q140565",
    },
    "skateboard": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q15783",
        "wikidata_label": "skateboard",
        "wikidata_description": "wheeled board used for skateboarding",
        "wikidata_concept": "Q15783",
    },
    "snowboard": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q2000617",
        "wikidata_label": "snowboard",
        "wikidata_description": "winter sport equipment",
        "wikidata_concept": "Q2000617",
    },
    "spoon": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q81895",
        "wikidata_label": "spoon",
        "wikidata_description": "utensil consisting of a small shallow bowl, oval or round, at the end of a handle",
        "wikidata_concept": "Q81895",
    },
    "stop sign": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q250429",
        "wikidata_label": "stop sign",
        "wikidata_description": "A sign representing a temporary stop traffic regulation",
        "wikidata_concept": "Q250429",
    },
    "suitcase": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q200814",
        "wikidata_label": "suitcase",
        "wikidata_description": "form of luggage",
        "wikidata_concept": "Q200814",
    },
    "surfboard": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q457689",
        "wikidata_label": "surfboard",
        "wikidata_description": "platform board used in the sport of surfing",
        "wikidata_concept": "Q457689",
    },
    "teddy bear": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q213477",
        "wikidata_label": "teddy bear",
        "wikidata_description": "soft toy in the form of a bear",
        "wikidata_concept": "Q213477",
    },
    "tie": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q44416",
        "wikidata_label": "necktie",
        "wikidata_description": "clothing item, traditionally worn by boys and men with dress shirt",
        "wikidata_concept": "Q44416",
    },
    "toaster": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q14890",
        "wikidata_label": "toaster",
        "wikidata_description": "small oven for cooking bread",
        "wikidata_concept": "Q14890",
    },
    "toilet": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q7857",
        "wikidata_label": "toilet",
        "wikidata_description": "sanitation fixture",
        "wikidata_concept": "Q7857",
    },
    "toothbrush": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q134205",
        "wikidata_label": "toothbrush",
        "wikidata_description": "oral hygiene instrument used to clean the teeth, gums, and tongue",
        "wikidata_concept": "Q134205",
    },
    "traffic light": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q8004",
        "wikidata_label": "traffic light",
        "wikidata_description": "signalling device to control competing flows of traffic",
        "wikidata_concept": "Q8004",
    },
    "train": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q870",
        "wikidata_label": "train",
        "wikidata_description": "form of rail transport consisting of a series of connected vehicles",
        "wikidata_concept": "Q870",
    },
    "truck": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q43193",
        "wikidata_label": "truck",
        "wikidata_description": "commercial or utilitarian large motor vehicle",
        "wikidata_concept": "Q43193",
    },
    "umbrella": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q41607",
        "wikidata_label": "umbrella",
        "wikidata_description": "canopy designed to protect against rain or sun",
        "wikidata_concept": "Q41607",
    },
    "vase": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q191851",
        "wikidata_label": "vase",
        "wikidata_description": "open container, often used to hold cut flowers",
        "wikidata_concept": "Q191851",
    },
    "window": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q35473",
        "wikidata_label": "window",
        "wikidata_description": "opening to admit light or air",
        "wikidata_concept": "Q35473",
    },
    "wine glass": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q1531435",
        "wikidata_label": "wine glass",
        "wikidata_description": "drinking vessel",
        "wikidata_concept": "Q1531435",
    },
    "zebra": {
        "wikidata_concepturi": "http://www.wikidata.org/entity/Q32789",
        "wikidata_label": "zebra",
        "wikidata_description": "Group of African mammal species in the genus Equus of the horse family",
        "wikidata_concept": "Q32789",
    },
}
