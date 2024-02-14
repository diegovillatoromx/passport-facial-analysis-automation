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

# Create Lambda function
lambda_response = lambda_client.create_function(
    FunctionName='ImageRequestHandler',
    Runtime='python3.9',
    Role=config_data['iam_role_arn'],  # Assuming the IAM role is already created
    Handler='lambda_function.lambda_handler',
    Code={
        'ZipFile': open('lambda_function.zip', 'rb').read()  # Assuming you have a ZIP file with your Lambda code
    },
    Description='Lambda function for handling image requests',
    Architecture='x86_64'
)

# Update configurations with the Lambda ARN
config_data['lambda_arn'] = lambda_response['FunctionArn']

# Write the updated configurations back to configurations.json
with open('configurations/configurations.json', 'w') as config_file:
    json.dump(config_data, config_file)

print("Lambda ARN:", lambda_response['FunctionArn'])
