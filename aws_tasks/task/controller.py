import boto3
import logging
import json
import os

from model import Task
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TASKS_TABLE'])

logger = logging.getLogger(__name__)


def create(event, context):
    body = json.loads(event['body'])
    task = Task(**body)

    try:
        table.put_item(Item=task.dict())
    except ClientError as err:
        logger.error(
            "Couldn't add task to table %s. Here's why: %s: %s",
            table.name,
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        return {
            "statusCode": 409,
            "body": "Something happen between the creation"
        }
    else:
        return {
            "statusCode": 201,
            "body": task.json()
        }


def get(event, context):
    task_id = event['pathParameters']['taskId']
    task = Task.get_task(task_id, table)
    if not task:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Task not found"})
        }
    else:
        return {
            "statusCode": 200,
            "body": task.json()
        }


def update(event, context):
    task_id = event['pathParameters']['taskId']
    task = Task.get_task(task_id, table)
    if not task:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Task not exists"})
        }

    body = json.loads(event['body'])

    task = Task(task_id=task_id, **body)

    update_expression = "SET title=:t, description=:d, #stus=:s"
    expression_attribute_names = {
        "#stus": "status"
    }
    expression_values = {
        ":t": task.title,
        ":d": task.description,
        ":s": task.status,
    }

    try:
        table.update_item(
            Key={'taskId': task_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_values
        )
    except ClientError as err:
        logger.error(
            "Couldn't update task %s. Here's why: %s: %s",
            task_id,
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        return {
            "statusCode": 409,
            "body": "Something happen between the update"
        }
    else:
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Task updated successfully"})
        }


def delete(event, context):
    task_id = event['pathParameters']['taskId']

    task = Task.get_task(task_id, table)
    if not task:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Task not exists"})
        }

    try:
        table.delete_item(Key={'taskId': task_id})
    except ClientError as err:
        logger.error(
            "Couldn't delete task %s. Here's why: %s: %s",
            task_id,
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        return {
            "statusCode": 409,
            "body": "Something happen between deleting the resource"
        }

    return {
        "statusCode": 204,
        "body": "No Content"
    }