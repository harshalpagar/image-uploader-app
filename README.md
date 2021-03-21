
# Welcome to Image Uploader project!

This project aims to create REST API to upload an image to s3 bucket using AWS Api-Gateway backed by AWS Lambda, 
which is developed using AWS CDK. 

It demonstrates a CDK app with an instance of a stack (`image_uploader_app_stack`)
which contains an Amazon API Gateway to expose REST API , which calls AWS Lambda function to upload image to S3 bucket.

# Things to Change

 - Update bucket name in `cdk.json` file as per you.
 - Update tags in `app.py` file as per you.

# How to deploy

Prerequisite : you should have AWS CLI [to configure enviroment] and AWS CDK on you machine to execute following command

Build the project
````
cdk synth
````
Deploy the project
````
cdk deploy image-uploader-app
````

# CDK details
The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization process also creates
a virtualenv within this project, stored under the .venv directory.  To create the virtualenv
it assumes that there is a `python3` executable in your path with access to the `venv` package.
If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv
manually once the init process completes.

To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

You can now begin exploring the source code, contained in the hello directory.
There is also a very trivial test included that can be run like this:

```
$ pytest
```

To add additional dependencies, for example other CDK libraries, just add to
your requirements.txt file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
