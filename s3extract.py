import zipfile
import boto3
from io import BytesIO

s3 = boto3.resource('s3')

gloriashulman_bucket = s3.Bucket('www.gloriashulman.info')

build_bucket = s3.Bucket('build.www.gloriashulman.info')

portfolio_zip = BytesIO()


build_bucket.download_fileobj('gloriabuildbucket.zip', portfolio_zip)


with zipfile.ZipFile(portfolio_zip) as myzip:
    listOfFileNames = myzip.namelist()

    for fileName in listOfFileNames:
        obj = myzip.open(fileName)
        gloriashulman_bucket.upload_fileobj(obj, fileName)
