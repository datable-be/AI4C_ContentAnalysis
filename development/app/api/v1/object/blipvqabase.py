from transformers import BlipProcessor, BlipForQuestionAnswering
from torch import device as torch_device
from torch import cuda, softmax
from PIL import Image
from io import BytesIO

from classes import ObjectRequest
from api.v1.tools.source import source_to_tempfile
from api.v1.tools.wikidata import retrieve_concept_uri


def detection(
    request: ObjectRequest,
    model: BlipForQuestionAnswering,
    processor: BlipProcessor,
    settings: dict,
    url_source: bool,
) -> dict:
    if settings.get('dummy'):
        from constants import MODEL_RESPONSE

        return MODEL_RESPONSE

    request.source = str(request.source)

    # Move the model to GPU if available
    device = torch_device('cuda' if cuda.is_available() else 'cpu')
    # device = torch_device("cpu")
    model.to(device)

    _, data = source_to_tempfile(request.source, None, url=url_source)
    raw_image = Image.open(BytesIO(data)).convert('RGB')

    question = 'What is the main subject?'

    # Prepare the input
    pixel_values = processor(
        images=raw_image, return_tensors='pt'
    ).pixel_values.to(device)
    input_ids = processor(text=question, return_tensors='pt').input_ids.to(
        device
    )

    # Generate the answers
    output = model.generate(
        input_ids=input_ids,
        pixel_values=pixel_values,
        max_length=50,
        num_beams=10,
        early_stopping=False,
        output_scores=True,
        return_dict_in_generate=True,
        num_return_sequences=10,
    )

    # Extract the objects and confidence scores
    objects = []
    not_recognized = set()

    for i, sequence in enumerate(output.sequences):
        label = processor.decode(sequence, skip_special_tokens=True)
        label = label.strip().lower()
        if label in not_recognized:
            continue
        try:
            confidence = softmax(output.scores[i], dim=-1).max().item()
        except IndexError:
            continue
        wikidata_uri = retrieve_concept_uri(label)
        if wikidata_uri == '':
            not_recognized.add(label)
            continue
        if confidence < request.min_confidence:
            continue
        detected_object = {
            'confidence': confidence,
            'wikidata': {
                'wikidata_concepturi': wikidata_uri,
                'wikidata_label': label,
                'wikidata_concept': wikidata_uri.split('/')[-1],
            },
        }
        objects.append(detected_object)

    # Sort result on confidence
    sorted_objects = sorted(
        objects, key=lambda x: x['confidence'], reverse=True
    )

    # Filter max_objects
    if len(sorted_objects) > request.max_objects:
        sorted_objects = sorted_objects[0 : request.max_objects]

    result = {}
    result['request_id'] = request.id
    result['source'] = request.source
    result['data'] = {'objects': sorted_objects}

    return result
