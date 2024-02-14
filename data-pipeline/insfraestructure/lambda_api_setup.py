import boto3
import json

# Load AWS credentials and other configurations from configurations/configurations.json
with open('configurations/configurations.json', 'r') as config_file:
    config_data = json.load(config_file)
    aws_access_key_id = config_data['aws_access_key_id']
    aws_secret_access_key = config_data['aws_secret_access_key']
    aws_region = config_data['region']

# Configure Lambda client using the loaded credentials
lambda_client = boto3.client('lambda',
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key,
                             region_name=aws_region)

# Define the policy document granting full access to DynamoDB
dynamodb_policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "dynamodb:*",
            "Resource": "*"
        }
    ]
}

# Create an IAM client
iam_client = boto3.client('iam')

# Attach the policy to the role
iam_client.put_role_policy(
    RoleName=config_data['iam_role_name'],  # Replace with the actual role name
    PolicyName='DynamoDBFullAccessPolicy',
    PolicyDocument=json.dumps(dynamodb_policy_document)
)

print("DynamoDB full access policy attached to lambda function role.")

# Read the Lambda function code from the zip file
with open('data_retrieval/lambda_api.zip', 'rb') as zip_file:
    lambda_code = zip_file.read()

# Create Lambda function
lambda_response = lambda_client.create_function(
    FunctionName='ImageRequestHandler',
    Runtime='python3.9',
    Role=config_data['iam_role_arn'],  # Assuming the IAM role is already created
    Handler='lambda_function.lambda_handler',
    Code={
        'ZipFile': lambda_code
    },
    Description='Lambda function for handling image requests',
    Architecture='x86_64'
)

# Update configurations with the Lambda ARN
config_data['lambda_arn'] = lambda_response['FunctionArn']

# Write the updated configurations back to configurations.json
with open('configurations/configurations.json', 'w') as config_file:
    json.dump(config_data, config_file)

print("Lambda function created successfully.")

