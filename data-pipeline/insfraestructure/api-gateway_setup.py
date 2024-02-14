import boto3
import json

# Load AWS credentials and other configurations from configurations/configurations.json
with open('configurations/configurations.json', 'r') as config_file:
    config_data = json.load(config_file)
    aws_access_key_id = config_data['aws_access_key_id']
    aws_secret_access_key = config_data['aws_secret_access_key']
    aws_region = config_data['region']
    lambda_api_arn = config_data['lambda_arn']

# Configure API Gateway client using the loaded credentials
apigateway_client = boto3.client('apigatewayv2',
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key,
                                 region_name=aws_region)

# Create HTTP API
api_response = apigateway_client.create_api(
    Name='cloudtopia-API',
    ProtocolType='HTTP'
)
api_id = api_response['ApiId']

# Create Stage for the API
stage_response = apigateway_client.create_stage(
    ApiId=api_id,
    StageName='test',
    AutoDeploy=True
)
stage_url = stage_response['ApiGatewayManaged']
invoke_url = f"https://{api_id}.execute-api.{aws_region}.amazonaws.com/{stage_response['StageName']}"

# Update configurations with the invoke URL
config_data['invoke_URL'] = invoke_url

# Write the updated configurations back to configurations.json
with open('configurations/configurations.json', 'w') as config_file:
    json.dump(config_data, config_file)

# Create Integration for the API
integration_response = apigateway_client.create_integration(
    ApiId=api_id,
    IntegrationType='AWS_PROXY',
    IntegrationUri=lambda_api_arn,
    IntegrationMethod='POST',
    PayloadFormatVersion='2.0'
)

# Create Route for the API with the Integration
route_response = apigateway_client.create_route(
    ApiId=api_id,
    RouteKey='GET /images',
    Target=integration_response['IntegrationId']
)

# Attach permissions to Lambda function for API Gateway to invoke it
lambda_client = boto3.client('lambda',
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key,
                             region_name=aws_region)

lambda_client.add_permission(
    FunctionName='ImageRequestHandler',  # Change this to your Lambda function name
    StatementId='apigateway-invoke',
    Action='lambda:InvokeFunction',
    Principal='apigateway.amazonaws.com',
    SourceArn=f"arn:aws:execute-api:{aws_region}:{config_data['aws_account_id']}:{api_id}/*/*/*"
)

print("Invoke URL:", invoke_url)

