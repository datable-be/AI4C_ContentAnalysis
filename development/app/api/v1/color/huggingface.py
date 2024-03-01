# See https://huggingface.co/Salesforce/blip-vqa-base

from PIL import Image
import torch
from transformers import BlipProcessor, BlipForQuestionAnswering

from api.v1.tools.image import url_to_tempfile
from api.v1.tools.color import extract_colors_from_sentence, add_URIs

from classes import ColorRequest


def detection(
    color_request: ColorRequest,
    model: BlipForQuestionAnswering,
    processor: BlipProcessor,
    settings: dict,
) -> dict:
    result = {}

    # Move the model to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # device = torch.device("cpu")
    model.to(device)

    try:
        url = str(color_request.source)

        # to do: what about color_request.foreground_detection? and min_area and such?
        file_path = url_to_tempfile(url, None)
        image = Image.open(file_path).convert("RGB")

        # Determine object type
        inputs_object = processor(
            image,
            "What is the main foreground subject of the image?",
            return_tensors="pt",
        ).to(device)
        out_object = model.generate(**inputs_object, max_new_tokens=20)
        answer_object = processor.decode(out_object[0], skip_special_tokens=True)

        if answer_object in [
            "man",
            "woman",
            "mannequin",
            "girl",
            "boy",
            "model",
            "blonde woman",
        ]:
            question_color = "Which colors are the clothes of the" + answer_object + "?"
        elif answer_object in ["runway"]:
            # Avoid color of the runway (happens with catwalk pictures)
            question_color = "Which colors are the clothes of the model on the runway?"
        else:
            question_color = "Which colors has the " + answer_object + "?"

        # Determine color
        inputs_color = processor(image, question_color, return_tensors="pt").to(device)
        out_color = model.generate(**inputs_color, max_new_tokens=20)
        answer_color = processor.decode(out_color[0], skip_special_tokens=True)

        colors = extract_colors_from_sentence(answer_color)

        percentages = {color: None for color in colors}
        result = add_URIs(percentages)

    except Exception as e:
        # to do (see also object error handling?)
        pass

    return result
