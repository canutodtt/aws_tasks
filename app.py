#!/usr/bin/env python3
import os
from dotenv import load_dotenv

import aws_cdk as cdk

from aws_tasks.aws_tasks_stack import AwsTasksStack

load_dotenv()


app = cdk.App()
AwsTasksStack(
    app,
    "AwsTasksStack",
    env=cdk.Environment(account=os.environ.get('AWS_ACCOUNT_ID'), region=os.environ.get('AWS_REGION')),
)

app.synth()
