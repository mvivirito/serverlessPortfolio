import mimetypes
import zipfile
import boto3
from io import BytesIO


def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:983784055278:DeployGloriaPortfolioTopic')

    location = {
        "bucketName": 'build.www.gloriashulman.info',
        "objectKey": 'gloriabuildbucket.zip'
    }

    job = event.get("CodePipeline.job")

    if job:
        for artifact in job["data"]["inputArtifacts"]:
            if artifact["name"] == "MyAppBuild":
                location = artifact["location"]["s3Location"]

    gloriashulman_bucket = s3.Bucket('www.gloriashulman.info')

    build_bucket = s3.Bucket(location["bucketName"])

    portfolio_zip = BytesIO()


    build_bucket.download_fileobj(location["objectKey"], portfolio_zip)


    with zipfile.ZipFile(portfolio_zip) as myzip:
        listOfFileNames = myzip.namelist()

        for fileName in listOfFileNames:
            obj = myzip.open(fileName)
            gloriashulman_bucket.upload_fileobj(obj, fileName, ExtraArgs={'ContentType': mimetypes.guess_type(fileName) [0]})
            gloriashulman_bucket.Object(fileName).Acl().put(ACL='public-read')

    topic.publish(Message="Portfolio Deplyed!")
    if job:
        codepipeline = boto3.client('codepipeline')
        codepipeline.put_job_success_result(jobId=job["id"])
    return 'Job Complete!'

