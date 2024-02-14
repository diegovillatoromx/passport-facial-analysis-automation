# passport-facial-analysis-automation 
 
```r  
data-pipeline/  
│  
├── image_processing/
│   ├── lambda_function.py      <- Lambda function code for image processing
│
├── notifications/
│   ├── lambda_destination.py   <- Lambda Destinations configuration
│
├── data_retrieval/
│   ├── api_gateway/
│   │   └── lambda_function.py  <- Lambda function code for data retrieval
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
