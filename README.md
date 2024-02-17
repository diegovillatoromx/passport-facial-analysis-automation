# Automated Passport Photo Validation: Streamline Processes with Cloudtopia Passport Office

## Table of Contents

1. [Description: Introduction](#description-introduction)
   - [Key Points](#key-points)
2. [Architecture](#architecture)
3. [Dataset](#dataset)
4. [Methodology](#methodology)
5. [Modular Code Overview](#modular-code-overview)
6. [Contribution](#contribution)
7. [Contact](#contact)

## Description: Introduction

As an employee of the Cloudtopia Passport Office, a pivotal Federal agency entrusted with issuing passports to our esteemed citizens, you are at the forefront of revolutionizing the Passport Photo Validation process. Our agency is committed to simplifying and streamlining operations through automation, ensuring a seamless experience for both applicants and staff members.

### Key Points

- **Business Goal:** The primary objective of this project is to eliminate the need for human intervention in evaluating submitted photographs. Through automation, we aim to enhance efficiency and reduce processing times, ultimately improving the overall passport issuance process.

- **Technical Goals:** Our technical objectives encompass storing user images and implementing an automated evaluation system based on predefined rules. Additionally, we seek to integrate notification mechanisms to alert downstream services upon successful image evaluation. Furthermore, the provision of an API will enable client teams to access evaluation results effortlessly.

- **Agency Rules:** Adhering to agency guidelines, submitted portraits must adhere to specific criteria, including clear visibility of the applicant's face, absence of sunglasses, open eyes, and a neutral facial expression without smiling. These rules ensure the integrity and authenticity of passport photographs, aligning with our commitment to security and accuracy.

By embarking on this journey of automation, we strive to enhance the efficiency, accuracy, and security of the Passport Photo Validation process, ultimately serving the needs of our citizens and reinforcing the reputation of the Cloudtopia Passport Office as a beacon of reliability and innovation.


  
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
<p align="center">
  <img src="https://github.com/diegovillatoromx/passport-facial-analysis-automation/blob/main/architecture.gif" alt="architecture-aws" width="800">
</p>


```plaintext
ValidationRequests
-------------------

- FileName: String
- ValidationResult: String
- FailureReasons: List<String> (Optional)
- Timestamp: String (ISO8601 Format)
- FileLocation: String
- FaceDetails: JSON Object
```
