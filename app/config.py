import oci

config = oci.config.from_file()

object_storage_client = oci.object_storage.ObjectStorageClient(config)
NAMESPACE = object_storage_client.get_namespace().data

#Name of Bucket for this demo
BUCKET_NAME = 'bucket-pruebas'

PREFIX = "anonymization"

DATASET_PATH = "sample_documents"