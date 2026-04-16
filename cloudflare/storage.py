from storages.backends.s3boto3 import S3Boto3Storage  # MUDOU AQUI!

class StaticFileStorage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"

class MediaFileStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False
    default_acl = "public-read"