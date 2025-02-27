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
from utils.anonymizer import anonymize
from PIL import Image


st.title('Document anonymization')

if file := st.file_uploader('Upload a PDF file', type='jpg'):
    status, filename = upload_file(file)
    st.write('File uploaded')

    response = get_file(os.path.join(config.PREFIX, filename))
    image = Image.open(BytesIO(response.data.content))
    st.image(image)

    file_path = os.path.join(config.PREFIX, filename)
    job_response = extract_text(config.NAMESPACE, config.BUCKET_NAME, file_path, config.PREFIX)
    output_location = get_output_location(job_response)

    results_path = os.path.join(config.PREFIX, job_response.data.id, output_location, "results", os.path.join(config.PREFIX, filename+".json"))

    response = get_file(results_path)

    bytes_json = response.data.content
    json_data = json.loads(bytes_json)
    
    words = json_data["pages"][0]["words"]
    text_in_words = " ".join([word["text"] for word in words])
    st.text(text_in_words)

    pii_entities = detect_language_pii_entities(text_in_words)

    pii_words = [pii_words.text for pii_words in pii_entities.documents[0].entities]
    st.text("Se identificaron las siguientes palabras PII:" + ', '.join(pii_words))

    filtered_pii_words = list(filter(lambda word: word["text"] in pii_words, words))

    anonymized_image = anonymize(image, filtered_pii_words)

    st.image(anonymized_image)


# files = list_files()
# for file in files:
#     st.write(file)

