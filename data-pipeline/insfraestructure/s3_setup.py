import boto3
import json
import os

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

def save_configurations(configurations):
    """
    Save configurations to 'config/configurations.json'.

    Args:
    - configurations: A dictionary with configurations to be saved.
    """
    with open(CONFIG_FILE_PATH, "w") as json_file:
        json.dump(configurations, json_file, indent=4)

def create_s3_bucket():
    """
    Create a new bucket in Amazon S3 with configurations provided in 'config/configurations.json'.

    Returns:
    - The ARN of the created bucket.
    """
    configurations = load_configurations()

    try:
        # Create an S3 client
        s3_client = boto3.client('s3', region_name=configurations["region"],
                                 aws_access_key_id=configurations["aws_access_key_id"],
                                 aws_secret_access_key=configurations["aws_secret_access_key"])

        # Create the bucket in the specified region
        s3_client.create_bucket(Bucket=configurations["bucket_name"])

        print(f"Bucket '{configurations['bucket_name']}' created successfully in the region '{configurations['region']}'.")
        
        # Get the ARN of the created bucket
        bucket_arn = f"arn:aws:s3::{configurations['bucket_name']}"
        configurations["bucket_arn"] = bucket_arn
        save_configurations(configurations)
        
        print("Bucket ARN saved to 'config/configurations.json'.")
        
        return bucket_arn
    except Exception as e:
        print(f"Error creating bucket '{configurations['bucket_name']}': {str(e)}")
        return None

if __name__ == "__main__":
    create_s3_bucket()

