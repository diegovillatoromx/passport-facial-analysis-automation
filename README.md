# passport-facial-analysis-automation 
 
```r 
data-pipeline/
│
├── image_processing/
│   ├── lambda_function.py      <- Lambda function code for image processing
│   └── lambda_config.json      <- Lambda function configuration
│
├── notifications/
│   ├── sns_topic_config.json   <- Amazon SNS topic configuration
│   ├── lambda_destination.py   <- Lambda Destinations configuration
│   └── config/
│       └── destination_config.json  <- Lambda Destinations configuration file
│
├── data_retrieval/
│   ├── api_gateway/
│   │   ├── api_config.json     <- Amazon API Gateway configuration
│   │   └── lambda_function.py  <- Lambda function code for data retrieval
│   └── dynamodb/
│       ├── dynamodb_table_config.json  <- DynamoDB table configuration
│       └── config/
│           └── dynamodb_table_config.json  <- DynamoDB table configuration file
│
├── infrastructure/
│   ├── lambda_setup.py         <- Script to set up Lambda function
│   ├── sns_setup.py            <- Script to set up Amazon SNS topic
│   ├── api_gateway_setup.py    <- Script to set up Amazon API Gateway
│   ├── dynamodb_setup.py       <- Script to set up DynamoDB table
│   └── s3_setup.py             <- Script to set up S3 bucket
│   └── config/
│       └── configurations.json <- Configuration file for infrastructure
│
└── README.md                   <- File with information about the project
```
