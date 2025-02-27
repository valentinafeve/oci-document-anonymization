import oci 
from hashlib import md5
from io import BytesIO
import os 


config = oci.config.from_file()

object_storage_client = oci.object_storage.ObjectStorageClient(config)
NAMESPACE = object_storage_client.get_namespace().data

#Name of Bucket for this demo
BUCKET_NAME = 'bucket-pruebas'

PREFIX = "anonymization"

def get_file(path):
    response = object_storage_client.get_object(NAMESPACE, BUCKET_NAME, path)
    return response

def upload_file(file: BytesIO):
    filename = md5(file.getvalue()).hexdigest()
    response = object_storage_client.put_object(NAMESPACE, BUCKET_NAME, os.path.join(PREFIX, filename), file)
    return response.status, filename

def list_files():
    files = []
    objetcs = object_storage_client.list_objects(NAMESPACE, BUCKET_NAME, prefix=PREFIX)
    for obj in objetcs.data.objects:
        files.append(obj.name)
    return files