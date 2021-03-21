#!/usr/bin/env python3

from aws_cdk import core

from image_uploader_app.image_uploader_app_stack import ImageUploaderAppStack


app = core.App()

stack = ImageUploaderAppStack(app, "image-uploader-app", env={'region': 'us-east-1'})

# add tags to stack which will add to all resources under it
tags = core.Tags.of(stack)
tags.add("Name", "Harshal Pagar")
tags.add("Project", "Image Uploader App")

app.synth()
