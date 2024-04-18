# ask what the contents of an image is, retrieve the Wikidata ID of the concepts
# store wikidata concepts in CSV, so it has to be retrieved only once

import requests
import torch
import csv
import os
from PIL import Image
from transformers import BlipProcessor, BlipForQuestionAnswering

# retrieve the Wikidata URI for the subject from a CSV
# if the concept is not in the CSV, get it from Wikidata and add to the list

# Get the Wikidata ID of a concept
def retrieve_concept_uri(concept):
    # CSV file name and path
    csv_file = 'wikidata_uris.csv'

    # Check if the CSV file exists
    if os.path.isfile(csv_file):
        # Check if the concept is already in the CSV file
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['concept'] == concept:
                    print(f"'{concept}' is in Wikidata")
                    return row['uri']
            else:
                # Construct the URL
                print(f"checking concept '{concept}' in Wikidata..")
                url = f'https://www.wikidata.org/w/api.php?action=wbsearchentities&search={concept}&format=json&language=en&uselang=en&type=item&limit=10'

                try:
                    response = requests.get(url)
                    response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
                    json_data = response.json()

                    # Extract conceptURI based on the specified criteria
                    search_info = json_data.get('searchinfo', {})
                    search_matches = json_data.get('search', [])
                    search_text = search_info.get('search', '')

                    for entry in search_matches:
                        match = entry.get('match', {})
                        if (
                            match.get('type') == 'label'
                            or match.get('type') == 'alias'
                        ) and match.get('text') == search_text:
                            uri = entry.get('concepturi')

                            # Write the concept and URI to the CSV file
                            with open(csv_file, 'a', newline='') as file:
                                fieldnames = ['concept', 'uri']
                                writer = csv.DictWriter(
                                    file, fieldnames=fieldnames
                                )
                                if os.path.getsize(csv_file) == 0:
                                    writer.writeheader()
                                writer.writerow(
                                    {'concept': concept, 'uri': uri}
                                )

                            return uri

                except requests.exceptions.RequestException as e:
                    print(f'Error: {e}')

                return None


# Get the subjects of an image
def get_subject(url, confidence_threshold):
    processor = BlipProcessor.from_pretrained('Salesforce/blip-vqa-base')
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    print(f'running with {device}')
    model = BlipForQuestionAnswering.from_pretrained(
        'Salesforce/blip-vqa-base'
    ).to(device)

    raw_image = Image.open(requests.get(img_url, stream=True).raw).convert(
        'RGB'
    )
    confidence_threshold = confidence_threshold

    question = 'What is the main subject?'
    print(f'\nQuestion: {question}\n')

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

    # Extract the answers and confidence scores
    answers = []
    confidence_scores = []
    wd_uris = []

    for i in range(len(output.sequences)):
        try:
            answer = processor.decode(
                output.sequences[i], skip_special_tokens=True
            )
            score = torch.softmax(output.scores[i], dim=-1).max().item()
            wd_uri = retrieve_concept_uri(answer)
            if score >= confidence_threshold and wd_uri:
                answers.append(answer)
                confidence_scores.append(score)
                # wd_uri = retrieve_concept_uri(answer)
                wd_uris.append(wd_uri)
        except IndexError:
            # Handle cases where there are no answers with confidence >= threshold
            pass

    if len(answers) == 0:
        print(f'\nNo answers with confidence score >= {confidence_threshold}')

    return zip(answers, confidence_scores, wd_uris)


# TEST
imagefile_path = 'path/to/csv/w/urls/sample100.csv'
resultfile_path = '/path/to/results/sample100_BLIP_result.csv'
confidence_threshold = 0.1

with open(imagefile_path, 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row:  # Skip empty rows
            results = []
            img_url = row[1].strip()
            coco_annotation = row[2].strip()
            coco_annotation_count = row[3].strip()
            # get annotations
            subjects = get_subject(img_url, confidence_threshold)
            # print annotations
            for answer, score, wd_uri in subjects:
                print(f'Subject: {answer}')
                print(f'Confidence score: {score:.2f}')
                print(f'Wikidata uri: {wd_uri}\n')
                results.append(
                    [
                        img_url,
                        coco_annotation,
                        coco_annotation_count,
                        answer,
                        f'{score:.2f}',
                        wd_uri,
                    ]
                )
                with open(resultfile_path, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    # Write data
                    writer.writerows(results)

# # Set parameters
# img_url = 'https://example.com/image.jpg'
# confidence_threshold = 0.1
# imagefile_path = 'input.csv'
# resultfile_path = 'output.csv'
#
# # Process images from input CSV file
# with open(imagefile_path, 'r', newline='') as csvfile:
#     reader = csv.reader(csvfile)
#     for row in reader:
#         if row:  # Skip empty rows
#             img_url = row[1].strip()
#             subjects = get_subject(img_url, confidence_threshold)
#             for answer, score, wd_uri in subjects:
#                 print(f"Subject: {answer}")
#                 print(f"Confidence score: {score:.2f}")
#                 print(f"Wikidata uri: {wd_uri}\n")
#                 # Write results to output CSV file
#                 with open(resultfile_path, mode='a', newline='') as file:
#                     writer = csv.writer(file)
#                     writer.writerow([img_url, answer, f"{score:.2f}", wd_uri])
