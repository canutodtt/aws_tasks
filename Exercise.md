## Assignment:

Create a Serverless CRUD API for "Tasks" Using AWS CDK, Lambda, API Gateway, and DynamoDB

## Problem Statement:

You are tasked with creating a serverless CRUD (Create, Read, Update, Delete) API for managing a simple "Tasks" service. Each task contains the following attributes:

- `taskId` (string) – unique identifier for the task.
- `title` (string) – the title of the task.
- `description` (string) – a brief description of the task.
- `status` (string) – the current status of the task (`"pending"`, `"in-progress"`, or `"completed"`).

You will use AWS CDK to define the infrastructure and deploy the following:

1. API Gateway – To expose the REST API.
2. Lambda Function(s) – To handle the CRUD operations (Create, Read, Update, Delete).
3. DynamoDB Table – To store task data.

## Requirements:

1. Create a DynamoDB table named `TasksTable` with the following properties:
   - Partition key: `taskId` (string).
   - Define a table with appropriate read and write capacity (on-demand or provisioned).

2. Create Lambda function(s) for each operation (CRUD):
   - Create Task (`POST /tasks`): Add a new task to the `TasksTable`.
   - Get Task (`GET /tasks/{taskId}`): Fetch a task by `taskId` from the `TasksTable`.
   - Update Task (`PUT /tasks/{taskId}`): Update a task’s attributes (e.g., title, description, status).
   - Delete Task (`DELETE /tasks/{taskId}`): Remove a task from the `TasksTable`.

3. Create an API Gateway REST API:
   - Integrate the Lambda functions with appropriate HTTP methods (`POST`, `GET`, `PUT`, `DELETE`).
   - The API should accept and return data in JSON format.

4. Use AWS CDK to define all resources:
   - DynamoDB table.
   - Lambda functions.
   - API Gateway.

## Task Details:

1. Create Task (POST /tasks):
   - Request body example:
     ```
     {
       "title": "Task 1",
       "description": "This is task 1",
       "status": "pending"
     }
     ```
   - Response:
     ```
     {
       "taskId": "generated-unique-id",
       "title": "Task 1",
       "description": "This is task 1",
       "status": "pending"
     }
     ```

2. Get Task (GET /tasks/{taskId}):
   - Response example:
     ```
     {
       "taskId": "123",
       "title": "Task 1",
       "description": "This is task 1",
       "status": "in-progress"
     }
     ```

3. Update Task (PUT /tasks/{taskId}):
   - Request body example:
     ```
     {
       "title": "Updated Task 1",
       "description": "This task has been updated",
       "status": "completed"
     }
     ```

4. Delete Task (DELETE /tasks/{taskId}):
  - Response: `204 No Content`.

## Evaluation Criteria:
1. **Correctness**: The solution must correctly create, read, update, and delete tasks using the API.
2. **AWS CDK Usage**: The solution should use AWS CDK to define and deploy the infrastructure (Lambda, API Gateway, and DynamoDB).
3. **Lambda and API Gateway Integration**: The candidate should demonstrate proper integration between Lambda and API Gateway (using appropriate HTTP methods and status codes).
4. **DynamoDB Access**: The candidate should handle DynamoDB operations using the AWS SDK in the Lambda functions.
5. **Code Structure**: The code should be well-structured, readable, and follow good practices for infrastructure-as-code and serverless design.
6. **Error Handling**: Handle common errors such as missing data, incorrect task IDs, etc., with appropriate HTTP status codes and messages.
7. **Testing (optional)**: Bonus points if the candidate uses libraries like AWS Powertools, Pydantic and writes tests (unit or integration) to ensure their solution works as expected.

## Deliverables:
 - A **GitHub repository** (or a zip)
 - Lambda function code
 - README with setup instructions and how to deploy the stack using CDK.
 - Clear instructions on how to:
 - Deploy the solution (including how to install dependencies and use CDK).
 - Test the API using tools like `curl`, Postman, or similar.

## Additional Guidance:

- You can generate unique `taskId`s using a random string generator or a UUID.
- Ensure that all Lambda functions have the necessary permissions to access the DynamoDB table.
- Feel free to use a framework (e.g., AWS SDK for DynamoDB) to interact with DynamoDB from Lambda.
- Consider handling edge cases like missing or invalid task IDs.

hablar de pyenv,
installar cdk, y awscli por brew
instalar docker desktop
crear usuario en AWS
correr cdk init app --languge python
ajustar credenciales