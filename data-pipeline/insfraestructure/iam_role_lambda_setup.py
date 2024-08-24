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

def update_configurations(iam_role_arn):
    """
    Update configurations in 'config/configurations.json' with the IAM role ARN.

    Args:
    - iam_role_arn: The ARN of the IAM role to be stored in configurations.
    """
    configurations = load_configurations()
    configurations["iam_role_arn"] = iam_role_arn  # Update IAM role ARN in configurations
    
    # Write updated configurations back to the file
    with open(CONFIG_FILE_PATH, "w") as json_file:
        json.dump(configurations, json_file, indent=4)

def create_lambda_role():
    """
    Create a new IAM role for AWS Lambda with configurations provided in 'config/configurations.json'.

    Returns:
    - The ARN of the created IAM role for the Lambda function.
    """
    configurations = load_configurations()
    
    # Initialize Boto3 clients
    iam_client = boto3.client('iam', region_name=configurations["region"],
                              aws_access_key_id=configurations["aws_access_key_id"],
                              aws_secret_access_key=configurations["aws_secret_access_key"])
    
    # Define IAM role parameters
    role_name = configurations["iam_role_name"]  # Use the IAM role name from configurations.json
    assume_role_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }

    # Define policy documents for S3, CloudWatch, Rekognition, and DynamoDB access
    s3_policy_document = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": "*"
        }]
    }

    cloudwatch_policy_document = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": "cloudwatch:*",
            "Resource": "*"
        }]
    }

    rekognition_policy_document = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": "rekognition:*",
            "Resource": "*"
        }]
    }

    dynamodb_policy_document = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": "dynamodb:*",
            "Resource": "*"
        }]
    }

    # Create the IAM role with the specified policies
    response = iam_client.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(assume_role_policy_document),
        Description="Role for AWS Lambda function"
    )

    # Attach policies to the IAM role
    iam_client.put_role_policy(RoleName=role_name, PolicyName='S3_FullAccess', PolicyDocument=json.dumps(s3_policy_document))
    iam_client.put_role_policy(RoleName=role_name, PolicyName='CloudWatch_FullAccess', PolicyDocument=json.dumps(cloudwatch_policy_document))
    iam_client.put_role_policy(RoleName=role_name, PolicyName='Rekognition_FullAccess', PolicyDocument=json.dumps(rekognition_policy_document))
    iam_client.put_role_policy(RoleName=role_name, PolicyName='DynamoDB_FullAccess', PolicyDocument=json.dumps(dynamodb_policy_document))
    
    # Extract and print the ARN of the created IAM role
    role_arn = response["Role"]["Arn"]
    print("IAM Role created for Lambda function:", role_arn)
    
    # Update configurations.json with the IAM role ARN
    update_configurations(role_arn)

if __name__ == "__main__":
    create_lambda_role()

