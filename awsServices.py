import boto3
import os
from collections import defaultdict

s3 = boto3.resource('s3')

bucket = s3.Bucket(name="ytsheetmusic")

def uploadFile(filename, bucket):    
    bucket.upload_file(Filename=filename,  Key=filename)

def downloadFile(filename, destination, bucket):
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    bucket.download_file(Key=filename, Filename=destination)
    
def deleteFile(filename, bucket_name='ytsheetmusic'):
    s3.Object(bucket_name, filename).delete()

def getFiles(bucket, prefix=''):
    items = defaultdict(list)
    for item in bucket.objects.filter(Prefix=prefix):
        name = item.key
        if name.startswith(prefix):
            folderpath, delimiter, filename = name.rpartition('/')
            items[folderpath].append(filename)
    return dict(items)