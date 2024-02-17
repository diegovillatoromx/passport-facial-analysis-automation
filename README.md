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

### Compute
Our system needs compute capabilities to respond to file uploads effectively. We have two options: polling to detect new images or utilizing an event-driven architecture for automatic invocation of the compute layer upon image upload. Regardless of the approach, reliability and fast performance are critical for this component to ensure timely processing of uploaded images.

### Facial Recognition
At the heart of our application lies facial recognition, responsible for detecting facial features in submitted photos. This component must be scalable to accommodate varying workloads and exhibit low latency to provide near-real-time analysis. Integration with facial recognition libraries that utilize confidence bands is essential for accurate image analysis.

### Database
A performant and scalable database is essential for storing approval/rejection details and references to submitted images. We require a key-value lookup store capable of handling high volumes of data efficiently, ensuring quick access to stored information for evaluation purposes.

### Notifications
Notifications play a crucial role in our architecture, facilitating the dissemination of messages to client services upon image evaluation. Utilizing a notification system enables decoupling of microservices and mitigates reliance on a monolithic database, promoting scalability and fault tolerance in our system.

### API
To provide additional information about evaluation results, we need an API to expose relevant data to client teams. The API serves as a gateway for accessing evaluation outcomes, enabling seamless integration with client applications and enhancing user experience.

These six themes form the foundation of our architecture, guiding the development of our system to meet the requirements of the Passport Photo Validation process effectively.

  
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
