import boto3
import json

# Load AWS credentials and other configurations from configurations/configurations.json
with open('configurations/configurations.json', 'r') as config_file:
    config_data = json.load(config_file)
    aws_access_key_id = config_data['aws_access_key_id']
    aws_secret_access_key = config_data['aws_secret_access_key']
    aws_region = config_data['region']

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

# Create Route for the API
route_response = apigateway_client.create_route(
    ApiId=api_id,
    RouteKey='GET /images',
    Target='integrations/not_defined_yet'
)

print("Invoke URL:", invoke_url)
