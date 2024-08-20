import boto3
import json 

# Load AWS credentials and other configurations from configurations/configurations.json
with open('configurations/configurations.json', 'r') as config_file:
    config_data = json.load(config_file)
    aws_access_key_id = config_data['aws_access_key_id']
    aws_secret_access_key = config_data['aws_secret_access_key']
    aws_region = config_data['aws_region']

# Configure SNS client using the loaded credentials
sns_client = boto3.client('sns',
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          region_name=aws_region)

# Create the SNS topic
topic_response = sns_client.create_topic(Name='ValidationResult')
topic_arn = topic_response['TopicArn']

# Update the configurations with the latest ARN
config_data['arn_topic_sns'] = topic_arn

# Write the updated configurations back to configurations.json
with open('configurations/configurations.json', 'w') as config_file:
    json.dump(config_data, config_file)

# Create a subscription to the topic using the created topic ARN
subscription_response = sns_client.subscribe(
    TopicArn=topic_arn,
    Protocol='email-json',
    Endpoint='test@example.com'
)

print("Topic ARN:", topic_arn)
print("Subscription ARN:", subscription_response['SubscriptionArn'])
