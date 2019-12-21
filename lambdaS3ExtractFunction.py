import mimetypes
import zipfile
import boto3
from io import BytesIO




def lambda_handler(event, context):
    s3 = boto3.resource('s3')

    gloriashulman_bucket = s3.Bucket('www.gloriashulman.info')

    build_bucket = s3.Bucket('build.www.gloriashulman.info')

    portfolio_zip = BytesIO()


    build_bucket.download_fileobj('gloriabuildbucket.zip', portfolio_zip)


    with zipfile.ZipFile(portfolio_zip) as myzip:
        listOfFileNames = myzip.namelist()

        for fileName in listOfFileNames:
            obj = myzip.open(fileName)
            gloriashulman_bucket.upload_fileobj(obj, fileName, ExtraArgs={'ContentType': mimetypes.guess_type(fileName) [0]})
            gloriashulman_bucket.Object(fileName).Acl().put(ACL='public-read')

    return 'Hello from Lambda!'
