import oci
import os

config = oci.config.from_file()

# Initialize service client with default config file
ai_document_client = oci.ai_document.AIServiceDocumentClient(config)

def extract_text(namespace, bucket_name, filename, prefix):
    # Send the request to service, some parameters are not required, see API
    # doc for more info
    create_processor_job_response = ai_document_client.create_processor_job(
        create_processor_job_details=oci.ai_document.models.CreateProcessorJobDetails(
            input_location=oci.ai_document.models.ObjectStorageLocations(
                source_type="OBJECT_STORAGE_LOCATIONS",
                object_locations=[
                    oci.ai_document.models.ObjectLocation(
                        namespace_name=namespace,
                        bucket_name=bucket_name,
                        object_name=filename)]),
            output_location=oci.ai_document.models.OutputLocation(
                namespace_name=namespace,
                bucket_name=bucket_name,
                prefix=prefix),
            compartment_id=config["compartment_id"],
            processor_config=oci.ai_document.models.GeneralProcessorConfig(
                processor_type="GENERAL",
                features=[
                    oci.ai_document.models.DocumentTextExtractionFeature(
                        feature_type="TEXT_EXTRACTION",
                        generate_searchable_pdf=True)],
                document_type="OTHERS",
                is_zip_output_enabled=True,
                language="es"),
            display_name="EXAMPLE-displayName-Value"),
        opc_retry_token="EXAMPLE-opcRetryToken-Value",
        opc_request_id="MOZIJVR14UCLBIBEOUH8<unique_ID>")

    return create_processor_job_response

def get_output_location(job_response):
    output_location = "{}_{}".format(job_response.data.output_location.namespace_name, job_response.data.output_location.bucket_name)
    return output_location
