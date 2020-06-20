from storages.backends.s3boto3 import S3Boto3Storage
from django.contrib.staticfiles.storage import ManifestFilesMixin

class CustomS3Storage(ManifestFilesMixin, S3Boto3Storage):
    pass

StaticRootS3Boto3Storage = lambda: CustomS3Storage(location='static')
MediaRootS3Boto3Storage  = lambda: S3Boto3Storage(location='media')