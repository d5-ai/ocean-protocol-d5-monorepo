from google.cloud import storage


def list_gcs_files(bucket, prefix):
    client = storage.Client()
    for blob in client.list_blobs(bucket, prefix=prefix):
        # print(blob)
        yield {
            'public_url': blob.public_url,
            'size': blob.size,
            'md5_hash': blob.md5_hash
        }
