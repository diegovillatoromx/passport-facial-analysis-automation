import boto3
import json
import os

CONFIG_FILE_PATH = "config/configurations.json"
LAMBDA_CODE_PATH = "image_processing/lambda_function.zip"

def load_configurations():
    """
    Load configurations from 'config/configurations.json'.

    Returns:
    - A dictionary with the loaded configurations.
    """
    with open(CONFIG_FILE_PATH, "r") as json_file:
        configurations = json.load(json_file)
    return configurations

def create_lambda_function():
    """
    Create a new AWS Lambda function with configurations provided in 'config/configurations.json'.

    Returns:
    - The name of the created Lambda function.
    """
    configurations = load_configurations()
    
    # Initialize Boto3 client for Lambda with specified region and credentials
    lambda_client = boto3.client('lambda', 
                                region_name=configurations["region"],
                                aws_access_key_id=configurations.get("aws_access_key_id"),
                                aws_secret_access_key=configurations.get("aws_secret_access_key"))
    
    # Define Lambda function parameters
    lambda_function_name = "PhotoValidationProcessor"
    runtime = "python3.9"
    architecture = "x86_64"
    iam_role_arn = configurations["iam_role_arn"]  # Extract IAM role ARN from configurations
    
    # Create the Lambda function
    with open(LAMBDA_CODE_PATH, "rb") as file:
        zip_file_content = file.read()

    response = lambda_client.create_function(
        FunctionName=lambda_function_name,
        Runtime=runtime,
        Role=iam_role_arn,  # Use IAM role ARN from configurations
        Handler="lambda_function.lambda_handler",
        Code={
            "ZipFile": zip_file_content
        },
        Description="Lambda function for photo validation processing",
        Timeout=300,
        MemorySize=512,
        Architecture=architecture
    )

    # Extract and print the name of the created Lambda function
    function_name = response["FunctionName"]
    print("The Lambda function", function_name, "has been created successfully.")

    return function_name

def add_s3_trigger_to_lambda(lambda_function_name):
    """
    Add a trigger to the specified Lambda function to invoke it on S3 PUT events.

    Args:
    - lambda_function_name: The name of the Lambda function to add the trigger to.
    """
    configurations = load_configurations()
    
    # Initialize Boto3 client for Lambda with specified region and credentials
    lambda_client = boto3.client('lambda', 
                                region_name=configurations["region"],
                                aws_access_key_id=configurations.get("aws_access_key_id"),
                                aws_secret_access_key=configurations.get("aws_secret_access_key"))

    # Specify the S3 bucket and event type for the trigger
    s3_trigger_configuration = {
        "EventSourceArn": f"arn:aws:s3:::{configurations['bucket_name']}",
        "Events": ["s3:ObjectCreated:*"],
        "LambdaFunctionArn": f"arn:aws:lambda:{configurations['region']}:{os.environ['AWS_ACCOUNT_ID']}:function:{lambda_function_name}",
        "Filter": {
            "Key": {
                "FilterRules": [
                    {
                        "Name": "suffix",
                        "Value": ".jpg"
                    }
                ]
            }
        }
    }

    # Add the S3 trigger to the Lambda function
    lambda_client.create_event_source_mapping(
        FunctionName=lambda_function_name,
        EventSourceArn=f"arn:aws:s3:::{configurations['bucket_name']}",
        StartingPosition="LATEST",
        EventSourceToken="",
        BatchSize=100,
        Enabled=True,
        DestinationConfig={
            "OnSuccess": {
                "Destination": f"arn:aws:lambda:{configurations['region']}:{os.environ['AWS_ACCOUNT_ID']}:function:{lambda_function_name}"
            },
            "OnFailure": {
                "Destination": f"arn:aws:lambda:{configurations['region']}:{os.environ['AWS_ACCOUNT_ID']}:function:{lambda_function_name}"
            }
        }
    )
    print("S3 trigger added to the Lambda function:", lambda_function_name)

if __name__ == "__main__":
    lambda_function_name = create_lambda_function()
    add_s3_trigger_to_lambda(lambda_function_name)



