import json
import pytest

from aws_cdk import core
from image_uploader_app.image_uploader_app_stack import ImageUploaderAppStack


def get_template():
    app = core.App()
    ImageUploaderAppStack(app, "image-uploader-app")
    return json.dumps(app.synth().get_stack("image-uploader-app").template)


def test_s3_bucket_created():
    assert ("AWS::S3::Bucket" in get_template())


def test_lambda_created():
    assert ("AWS::Lambda::Function" in get_template())


def test_api_gateway_created():
    assert ("AWS::ApiGateway::RestApi" in get_template())
