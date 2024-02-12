import boto3
import json

CONFIG_FILE_PATH = "config/configurations.json"

def load_configurations():
    """
    Load configurations from 'config/configurations.json'.

    Returns:
    - A dictionary with the loaded configurations.
    """
    with open(CONFIG_FILE_PATH, "r") as json_file:
        configurations = json.load(json_file)
    return configurations

def create_s3_put_event():
    """
    Create an S3 PUT event.

    Returns:
    - A dictionary representing the S3 PUT event.
    """
    s3_put_event = {
        "Records": [
            {
                "eventVersion": "2.1",
                "eventSource": "aws:s3",
                "awsRegion": "us-east-1",
                "eventTime": "2022-12-28T20:32:21.737Z",
                "eventName": "ObjectCreated:Put",
                "userIdentity": {
                    "principalId": "AWS:AIDA27XCHXURLYZDGRXJ5"
                },
                "requestParameters": {
                    "sourceIPAddress": "24.150.103.24"
                },
                "responseElements": {
                    "x-amz-request-id": "ACK4EHCW4N9E1VYA",
                    "x-amz-id-2": "0ccWkoGpLTpaHsJD5C3yfEK1sJ9pK5xVEKP4JmKRN9xjavYdTdzaMehhav1S9oCp3Pg7cVjjRRJUsIKgCbldjoXPUsOKRA1f"
                },
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "a801b2a6-90d0-40e9-81e4-97805f54ebda",
                    "bucket": {
                        "name": "cloudtopia-test",
                        "ownerIdentity": {
                            "principalId": "A2LONO3IHMQSYL"
                        },
                        "arn": "arn:aws:s3:::cloudtopia-test"
                    },
                    "object": {
                        "key": "me_normal.png",
                        "size": 441027,
                        "eTag": "835cee46933a96a40cc950ff66798542",
                        "sequencer": "0063ACA7D5A29D0CE0"
                    }
                }
            }
        ]
    }
    
    return s3_put_event

def create_lambda_function(s3_put_event):
    """
    Create a new AWS Lambda function with a trigger S3 PUT event.

    Args:
    - s3_put_event: A dictionary representing the S3 PUT event.

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
    
    # Create the Lambda function with S3 trigger
    response = lambda_client.create_function(
        FunctionName=lambda_function_name,
        Runtime=runtime,
        Role=iam_role_arn,  # Use IAM role ARN from configurations
        Handler="lambda_function.lambda_handler",
        Code={
            "ZipFile": open("image_processing/lambda_function.zip", "rb").read()  # Replace with your Lambda function code
        },
        Description="Lambda function for photo validation processing",
        Timeout=300,
        MemorySize=512,
        Architecture=architecture,
        Environment={
            'Variables': {
                'S3_PUT_EVENT': json.dumps(s3_put_event)
            }
        },
        TracingConfig={
            'Mode': 'Active'
        },
        Layers=[],
        Tags={}
    )

    # Extract and print the name of the created Lambda function
    function_name = response["FunctionName"]
    print("The Lambda function", function_name, "has been created successfully.")

    return function_name

if __name__ == "__main__":
    s3_put_event = create_s3_put_event()
    lambda_function_name = create_lambda_function(s3_put_event)

