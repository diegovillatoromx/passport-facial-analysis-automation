import boto3
import datetime
import json

def write_result_to_dynamodb(evaluation_result, file_name, face_details):
    # Initialize DynamoDB client
    dynamodb_client = boto3.client('dynamodb')

    # Define the DynamoDB table name
    table_name = 'ValidationsRequests'

    # Set the item attributes
    item_attributes = {
        'FileName': {'S': file_name},
        'ValidationResult': {'S': evaluation_result['result']},
        'FailureReasons': {'S': json.dumps(evaluation_result['failure_reasons'])},
        'Timestamp': {'S': datetime.datetime.now().replace(microsecond=0).isoformat()},
        'FileLocation': {'S': BUCKET_NAME + "/" + file_name},
        'FaceDetails': {'S': json.dumps(face_details)}
    }

    # Write the item to the DynamoDB table
    response = dynamodb_client.put_item(
        TableName=table_name,
        Item=item_attributes
    )

    # Check if the item was added successfully
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print('Item added to DynamoDB table successfully!')
    else:
        print('Error adding item to DynamoDB table.')

# Call the function with appropriate parameters
write_result_to_dynamodb(evaluation_result, file_name, face_details)
