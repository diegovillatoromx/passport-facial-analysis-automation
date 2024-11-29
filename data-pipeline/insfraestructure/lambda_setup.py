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
    lambda_function_params = configurations["aws_lambda"]
    
    # Extract code and environment from configurations
    code = configurations.get("code", {})
    environment = configurations.get("environment", {})
    
    # Attach IAM role to Lambda function parameters
    lambda_function_params["Role"] = configurations["iam_role_arn"]  # Use IAM role ARN from configurations
    
    # Create the Lambda function
    response = lambda_client.create_function(
        **lambda_function_params,
        Code=code,
        Environment=environment
    )

    # Extract and print the name of the created Lambda function
    function_name = response["FunctionName"]
    print("The Lambda function", function_name, "has been created successfully.")

    return function_name

if __name__ == "__main__":
    create_lambda_function()
