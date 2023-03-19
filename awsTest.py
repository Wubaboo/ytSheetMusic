import boto3
from collections import defaultdict

s3 = boto3.resource('s3')

bucket = s3.Bucket(name="ytsheetmusic")

def uploadFile(filename, bucket):    
    bucket.upload_file(Filename=filename,  Key=filename)

def downloadFile(filename, destination, bucket):
    bucket.download_file(Filename=destination, Key=filename)
    
def deleteFile(filename, bucket):
    pass

def getFiles(bucket):
    items = defaultdict(list)
    for item in bucket.objects.all():
        name = item.key
        folderpath, delimiter, filename = name.rpartition('/')
        items[folderpath].append(filename)
    return items
            