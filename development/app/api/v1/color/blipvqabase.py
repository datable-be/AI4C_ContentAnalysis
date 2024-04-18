# See https://huggingface.co/Salesforce/blip-vqa-base

from PIL import Image
from pathlib import Path
from cv2.dnn import Net
import torch
from transformers import BlipProcessor, BlipForQuestionAnswering

from api.v1.tools.image import determine_image
from api.v1.tools.path import filename_to_url
from api.v1.tools.color import (
    extract_colors_from_sentence,
    add_URIs,
    is_quasi_monochrome_with_rgb,
)

from classes import ColorRequest
from constants import BW_WARNING


def detection(
    request: ColorRequest,
    net: Net,
    model: BlipForQuestionAnswering,
    processor: BlipProcessor,
    settings: dict,
    url_source: bool,
) -> dict:
    result = {}

    # Switch off foreground detection (is done by model)!
    request.foreground_detection = False

    temp_path = determine_image(request, net, settings, None, url_source)
    if not temp_path:
        return result

    if is_quasi_monochrome_with_rgb(temp_path):
        result.setdefault('warnings', [])
        result['warnings'].append(BW_WARNING)

    # Move the model to GPU if available
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # device = torch.device("cpu")
    model.to(device)

    image = Image.open(temp_path).convert('RGB')

    # Determine object type
    inputs_object = processor(
        image,
        'What is the main foreground subject of the image?',
        return_tensors='pt',
    ).to(device)
    out_object = model.generate(**inputs_object, max_new_tokens=20)
    answer_object = processor.decode(out_object[0], skip_special_tokens=True)

    if answer_object in [
        'man',
        'woman',
        'mannequin',
        'girl',
        'boy',
        'model',
        'blonde woman',
    ]:
        question_color = (
            'Which colors are the clothes of the' + answer_object + '?'
        )
    elif answer_object in ['runway']:
        # Avoid color of the runway (happens with catwalk pictures)
        question_color = (
            'Which colors are the clothes of the model on the runway?'
        )
    else:
        question_color = 'Which colors has the ' + answer_object + '?'

    # Determine color
    inputs_color = processor(image, question_color, return_tensors='pt').to(
        device
    )
    out_color = model.generate(**inputs_color, max_new_tokens=20)
    answer_color = processor.decode(out_color[0], skip_special_tokens=True)

    colors = extract_colors_from_sentence(answer_color)

    # HuggingFace does not allow to determine percentages
    colors_with_fake_percentages = {color: None for color in colors}

    result['data'] = {'colors': add_URIs(colors_with_fake_percentages)}

    result['request_id'] = request.id
    result['source'] = request.source

    # Add image link
    basename = Path(temp_path).name
    result['data']['cropped_image'] = filename_to_url(basename)

    return result
