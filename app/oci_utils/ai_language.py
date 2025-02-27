import oci

config = oci.config.from_file()

ai_language_client = oci.ai_language.AIServiceLanguageClient(config)

def detect_domain_language(text):
    language = ai_language_client.detect_dominant_language(oci.ai_language.models.DetectDominantLanguageDetails(text=text)).data
    return language

def detect_language_key_phrases(text):
    key_phrases = ai_language_client.detect_language_key_phrases(oci.ai_language.models.DetectLanguageKeyPhrasesDetails(text=text)).data
    return key_phrases

def detect_language_pii_entities(text):
    pii = ai_language_client.batch_detect_language_pii_entities(oci.ai_language.models.BatchDetectLanguagePiiEntitiesDetails(
        documents=[
            oci.ai_language.models.TextDocument(
                key="1",
                text=text
            )
        ]
    )).data
    return pii