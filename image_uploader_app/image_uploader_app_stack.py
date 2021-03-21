from aws_cdk import (
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_apigateway as _apigw,
    aws_s3 as _s3,
    core
)
from aws_cdk.aws_apigateway import JsonSchemaVersion, JsonSchemaType


class ImageUploaderAppStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # get bucket name from context i.e. cdk.json
        image_storage_bucket = self.node.try_get_context("image-storage-bucket")
        # create a bucket to upload image
        image_s3_bucket = _s3.Bucket(self,
                                     id='image-uploader-bucket',
                                     bucket_name=image_storage_bucket,
                                     versioned=True,
                                     removal_policy=core.RemovalPolicy.DESTROY)

        image_uploader_lambda = _lambda.Function(self, 'image-uploader-function',
                                                 handler='image-uploader.handler',
                                                 function_name='image-uploader',
                                                 code=_lambda.Code.from_asset('lambda'),
                                                 runtime=_lambda.Runtime.PYTHON_3_7,
                                                 environment={
                                                     'BUCKET_NAME': image_s3_bucket.bucket_name,
                                                 },
                                                 description='Image Uploader Function'
                                                 )
        # grant bucket access to lambda
        image_s3_bucket.grant_read_write(image_uploader_lambda)

        image_lambda_integration = _apigw.LambdaIntegration(image_uploader_lambda, proxy=True, allow_test_invoke=True)

        method_responses = [
            # Successful response from the integration
            {'statusCode': '200',
             # Define what parameters are allowed or not
             'responseParameters': {
                 'method.response.header.Content-Type': True,
                 'method.response.header.Access-Control-Allow-Origin': True,
                 'method.response.header.Access-Control-Allow-Credentials': True
             }}
        ]

        image_api = _apigw.RestApi(self, 'image-uploader-api',
                                   description='Image Uploader Api',
                                   deploy=True,
                                   endpoint_types=[_apigw.EndpointType.REGIONAL]
                                   )

        # Image Model
        image_model_name = "ImageRequest"
        image_model = image_api.add_model('ImageRequest',
                                          content_type='application/json',
                                          model_name=image_model_name,
                                          schema={
                                              "schema": JsonSchemaVersion.DRAFT4,
                                              "title": "OCR Image Schema",
                                              "type": JsonSchemaType.OBJECT,
                                              "required": ["content"],
                                              "properties": {
                                                  "fileName": {"type": JsonSchemaType.STRING, "title": "File Name"},
                                                  "content": {
                                                      "type": JsonSchemaType.STRING,
                                                      "title": "OCR Image base64 encoded content",
                                                      "description": "This field contains an image in base64 encoded format",
                                                  }
                                              },
                                              "additional_properties": True
                                          },
                                          description='Image request should adhere to this json format')

        # Add Image POST method
        image_api.root.add_resource("image").add_method("post", image_lambda_integration,
                                                        operation_name="Upload Image request",
                                                        request_models={"application/json": image_model},
                                                        method_responses=method_responses
                                                        )
