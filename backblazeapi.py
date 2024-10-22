import boto3
from botocore.exceptions import ClientError

class BackblazeUploader:
    def __init__(self, key_id, application_key, bucket_name):
        self.key_id = key_id
        self.application_key = application_key
        self.bucket_name = bucket_name
        self.endpoint_url = 'https://s3.us-east-005.backblazeb2.com'
        self.s3_client = self._create_s3_client()

    def _create_s3_client(self):
        return boto3.client(
            service_name='s3',
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.key_id,
            aws_secret_access_key=self.application_key
        )

    def upload_file(self, file_path):
        try:
            file_name = file_path.split('/')[-1]
            with open(file_path, "rb") as file:
                self.s3_client.upload_fileobj(file, self.bucket_name, file_name)
            public_url = f"https://{self.bucket_name}.s3.us-east-005.backblazeb2.com/{file_name}"
            return public_url
        except ClientError as e:
            print(f"An error occurred: {e}")
            return None

if __name__ == "__main__":
    key_id = "0052fc0012fb1e30000000001"
    application_key = "K005XND/ukcRD5RYlhjHuSMARFqE9Ss"
    bucket_name = "UnicornsPrivateVideos"
    uploader = BackblazeUploader(key_id, application_key, bucket_name)
    file_path = "test.mp4"
    url = uploader.upload_file(file_path)
    if url:
        print(f"File uploaded successfully. Public URL: {url}")
    else:
        print("File upload failed.")