import json
import os

import config
import numpy as np
import pandas as pd
import streamlit as st
from oci_utils.document_understanding import extract_text, get_output_location
from oci_utils.object_storage import get_file, list_files, upload_file
from oci_utils.ai_language import detect_domain_language, detect_language_key_phrases, detect_language_pii_entities
from io import BytesIO
from utils.anonymizer import anonymize, filter_pii_words
from PIL import Image
from pdf2image import convert_from_bytes

st.set_page_config(layout="wide")
st.title('Document Anonymization')

col1, col2, col3 = st.columns([3, 1, 3])

if file := col1.file_uploader('Upload a PDF file', type='pdf'):
    status, filename = upload_file(file)
    col1.write('File uploaded')

    response = get_file(os.path.join(config.PREFIX, filename))

    image = convert_from_bytes(response.data.content, dpi=200, fmt='jpeg')[0]

    # image = Image.open(BytesIO(response.data.content))
    # col1.image(image)

    file_path = os.path.join(config.PREFIX, filename)
    job_response = extract_text(config.NAMESPACE, config.BUCKET_NAME, file_path, config.PREFIX)
    output_location = get_output_location(job_response)

    results_path = os.path.join(config.PREFIX, job_response.data.id, output_location, "results", os.path.join(config.PREFIX, filename+".json"))

    response = get_file(results_path)

    bytes_json = response.data.content
    json_data = json.loads(bytes_json)
    
    words = json_data["pages"][0]["words"]
    text_in_words = " ".join([word["text"] for word in words])
    col1.header("Extracted text")
    col1.text(text_in_words)

    pii_entities = detect_language_pii_entities(text_in_words)

    pii_words_list = [pii_words.text.split() for pii_words in pii_entities.documents[0].entities]
    pii_words = []
    for sentence in pii_words_list:
        for word in sentence:
            pii_words.append(word)
    col1.header("PII entities")
    col1.text(', '.join(pii_words))

    filtered_pii_words = filter_pii_words(words, pii_words)

    anonymized_image = anonymize(image, filtered_pii_words)

    col3.header("Anonymized image")
    col3.image(anonymized_image)
    col3.header("Original image")
    col3.image(image)


# files = list_files()
# for file in files:
#     st.write(file)

