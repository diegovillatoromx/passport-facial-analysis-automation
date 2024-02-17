# Automated Passport Photo Validation: Streamline Processes with Cloudtopia Passport Office

## Table of Contents

1. [Description: Introduction](#description-introduction)
   - [Key Points](#key-points)
2. [Design Components](#design-components)
3. [Architecture](#architecture)
4. [Dataset](#dataset)
5. [Methodology](#methodology)
6. [Modular Code Overview](#modular-code-overview)
7. [Contribution](#contribution)
8. [Contact](#contact)

## Description: Introduction

As an employee of the Cloudtopia Passport Office, a pivotal Federal agency entrusted with issuing passports to our esteemed citizens, you are at the forefront of revolutionizing the Passport Photo Validation process. Our agency is committed to simplifying and streamlining operations through automation, ensuring a seamless experience for both applicants and staff members.

### Key Points

- **Business Goal:** The primary objective of this project is to eliminate the need for human intervention in evaluating submitted photographs. Through automation, we aim to enhance efficiency and reduce processing times, ultimately improving the overall passport issuance process.

- **Technical Goals:** Our technical objectives encompass storing user images and implementing an automated evaluation system based on predefined rules. Additionally, we seek to integrate notification mechanisms to alert downstream services upon successful image evaluation. Furthermore, the provision of an API will enable client teams to access evaluation results effortlessly.

- **Agency Rules:** Adhering to agency guidelines, submitted portraits must adhere to specific criteria, including clear visibility of the applicant's face, absence of sunglasses, open eyes, and a neutral facial expression without smiling. These rules ensure the integrity and authenticity of passport photographs, aligning with our commitment to security and accuracy.

By embarking on this journey of automation, we strive to enhance the efficiency, accuracy, and security of the Passport Photo Validation process, ultimately serving the needs of our citizens and reinforcing the reputation of the Cloudtopia Passport Office as a beacon of reliability and innovation.


## Design Components

The high-level design components of our system are as follows:

### Image Storage
We require a robust image storage solution to retain user-submitted photos. Our storage component must be capable of handling images of varying sizes efficiently, ensuring fast uploads with minimal latency and high throughput. Additionally, durability of stored images is paramount to ensure data integrity.

#### Technologies Considered:
- **EFS:** Elastic File System provides easy integration of disk drivers onto compute instances.
- **S3*:** Simple Storage Service is chosen for its versatility in storing blob files of varying sizes and formats. S3 offers integration with other AWS services, APIs for data management, and features like event notifications.

### Compute
Our system needs compute capabilities to respond to file uploads effectively. We have two options: polling to detect new images or utilizing an event-driven architecture for automatic invocation of the compute layer upon image upload. Regardless of the approach, reliability and fast performance are critical for this component to ensure timely processing of uploaded images.

#### Technologies Considered:
- **EC2:** Elastic Cloud Compute offers hosted servers on AWS. While EC2 requires a polling mechanism for file upload detection, it provides flexibility in server management.
- **Fargate:** Fargate, a serverless compute service on Amazon Elastic Container Service (ECS), supports one-off tasks and maintains "warm" compute nodes for job execution.
- **Lambda*:** Lambda, a serverless Function as a Service (FaaS), eliminates infrastructure maintenance, allowing focus on business logic implementation.

### Facial Recognition
At the heart of our application lies facial recognition, responsible for detecting facial features in submitted photos. This component must be scalable to accommodate varying workloads and exhibit low latency to provide near-real-time analysis. Integration with facial recognition libraries that utilize confidence bands is essential for accurate image analysis.

#### Technologies Considered:
- **Rekognition*:** Rekognition employs machine learning for facial detection and analysis, providing accurate results for our application.

### Database
A performant and scalable database is essential for storing approval/rejection details and references to submitted images. We require a key-value lookup store capable of handling high volumes of data efficiently, ensuring quick access to stored information for evaluation purposes.

#### Technologies Considered:
- **RDS:** Relational Database Service offers various RDBMS engines, suitable for use cases requiring data relations.
- **Aurora:** Aurora, an in-house RDBMS developed by AWS, supports serverless variations and offers seamless integration with MySQL and Postgres engines.
- **DynamoDB*:** DynamoDB, a popular NoSQL database on AWS, excels in ultra-fast key-value lookups and seamless scalability.

### Notifications
Notifications play a crucial role in our architecture, facilitating the dissemination of messages to client services upon image evaluation. Utilizing a notification system enables decoupling of microservices and mitigates reliance on a monolithic database, promoting scalability and fault tolerance in our system.

#### Technologies Considered:
- **SQS:** Simple Queue Service provides distributed queuing with data persistence until processed by another compute layer.
- **Eventbridge:** Eventbridge offers a message bus concept for message publishing and delivery, supporting content-based filtering for routing messages.
- **SNS*:** Simple Notification Service is a highly scalable pub/sub service, foundational in AWS, facilitating subscription-based updates for topic owners and subscribers.

### API
To provide additional information about evaluation results, we need an API to expose relevant data to client teams. The API serves as a gateway for accessing evaluation outcomes, enabling seamless integration with client applications and enhancing user experience.

#### Technologies Considered:
- **AppSync:** Managed service for GraphQL users.
- **API Gateway:** Offers extensive features for building HTTP or Websocket-based APIs, including authorization, content validation, and rate limiting.

These design choices were made based on their suitability and alignment with the requirements of our Passport Photo Validation system. Services marked with an asterisk (*) were utilized in the creation of the project.

## Architecture

The architecture of our Passport Photo Validation system is designed to leverage cloud-native services provided by AWS, ensuring scalability, reliability, and cost-effectiveness. The system follows a microservices architecture, comprising loosely coupled components that communicate via APIs and event-driven mechanisms.

<p align="center">
  <img src="https://github.com/diegovillatoromx/passport-facial-analysis-automation/blob/main/architecture.gif" alt="architecture-aws" width="800">
</p>


### High-Level Overview

1. **Image Submission:** Users submit passport photos through a web interface or mobile application. The images are uploaded to Amazon S3, where they are securely stored and made available for processing.

2. **Image Processing:** Upon upload, images trigger an event that invokes AWS Lambda functions responsible for image processing tasks. These functions perform facial recognition using Amazon Rekognition, ensuring compliance with passport photo guidelines.

3. **Data Storage:** Approved/rejected photos and associated metadata are stored in Amazon DynamoDB, providing a highly scalable and performant storage solution for our application's requirements.

4. **Notifications:** Evaluation results are published to Amazon SNS topics, allowing client services to subscribe and receive updates in real-time. This decoupled architecture enables seamless integration with downstream systems.

5. **API Gateway:** An API Gateway serves as the entry point for client applications to access evaluation results and additional information. It provides a secure, managed interface for communication with our system.

### Benefits of Architecture

- **Scalability:** Cloud-native services enable automatic scaling to accommodate fluctuating workloads, ensuring consistent performance under varying demand.
- **Reliability:** Built-in redundancy and fault tolerance mechanisms of AWS services enhance the reliability of our system, minimizing downtime and ensuring data integrity.
- **Cost-Effectiveness:** Pay-as-you-go pricing model of AWS allows us to optimize costs by only paying for the resources consumed, without upfront investment in infrastructure.

## Dataset

The dataset used in our Passport Photo Validation system comprises a diverse collection of passport photos submitted by users. Each photo is associated with metadata including the applicant's name, date of submission, and evaluation status (approved/rejected).

### Data Collection

Passport photos are collected from users during the passport application process via the Cloudtopia Passport Office's web portal or mobile application. The submission process ensures adherence to guidelines for passport photo specifications, including clarity, facial visibility, and absence of accessories.

### Data Storage

Submitted photos are securely stored in Amazon S3 buckets, ensuring durability and accessibility. Metadata associated with each photo, such as applicant details and evaluation results, are stored in Amazon DynamoDB tables, providing fast and scalable data storage for efficient retrieval and processing.

### Data Security

Data security is paramount in our system. AWS Identity and Access Management (IAM) roles and policies are employed to enforce least privilege access controls, ensuring that only authorized entities can access and modify data. Additionally, encryption at rest and in transit mechanisms provided by AWS services protect data integrity and confidentiality.


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
