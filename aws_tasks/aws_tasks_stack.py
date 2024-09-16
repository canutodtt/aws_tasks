from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
)
from constructs import Construct
import logging

logging.getLogger('boto3').setLevel(logging.INFO)
logging.getLogger('botocore').setLevel(logging.INFO)
logging.getLogger('botocore.endpoint').setLevel(logging.DEBUG)


class AwsTasksStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        task_table = dynamodb.Table(
            self,
            "TasksTable",
            partition_key=dynamodb.Attribute(
                name="taskId",
                type=dynamodb.AttributeType.STRING
            ),
            table_name="Tasks",
            billing_mode=dynamodb.BillingMode.PROVISIONED,
            read_capacity=2,
            write_capacity=2,
        )

        self.setup_tasks(task_table)

    def setup_tasks(self, task_table: dynamodb.Table) -> None:
        create_task_lambda = self.create_lambda("CreateTaskFunction", "controller.create", task_table)
        get_task_lambda = self.create_lambda("GetTaskFunction", "controller.get", task_table)
        update_task_lambda = self.create_lambda("UpdateTaskFunction", "controller.update", task_table)
        delete_task_lambda = self.create_lambda("DeleteTaskFunction", "controller.delete", task_table)

        api = apigateway.RestApi(self, "TasksApi", rest_api_name="Tasks Service")

        tasks_resource = api.root.add_resource("tasks")
        task_resource = tasks_resource.add_resource("{taskId}")

        tasks_resource.add_method("POST", apigateway.LambdaIntegration(create_task_lambda))
        task_resource.add_method("GET", apigateway.LambdaIntegration(get_task_lambda))
        task_resource.add_method("PUT", apigateway.LambdaIntegration(update_task_lambda))
        task_resource.add_method("DELETE", apigateway.LambdaIntegration(delete_task_lambda))

    def create_lambda(self, id: str, handler: str, table: dynamodb.Table) -> None:
        lambda_fn = _lambda.Function(
            self, id,
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler=handler,
            code=_lambda.Code.from_asset(
                path="aws_tasks/task",
                bundling={
                    'image': _lambda.Runtime.PYTHON_3_10.bundling_image,
                    'command': [
                        'bash', '-c',
                        'pip install -r requirements.txt -t /asset-output && cp -au . /asset-output'
                    ]
                }
            ),
            environment={
                "TASKS_TABLE": table.table_name
            }
        )
        table.grant_read_write_data(lambda_fn)
        return lambda_fn
