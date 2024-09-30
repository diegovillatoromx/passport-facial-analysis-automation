# Automated Passport Photo Validation: Streamline Processes with Cloudtopia Passport Office

## Table of Contents 
 
1. [Description](#description)
2. [Architecture](#architecture) 
3. [Dataset](#dataset)
4. [Methodology and Modular Code Overview](#methodology-and-modular-code-overview)
5. [Data Modeling](#data-modeling)
6. [Contribution](#contribution)
7. [Contact](#contact)

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


## Methodology and Modular Code Overview

Our methodology for developing the Passport Photo Validation system emphasizes modularity, scalability, and maintainability. We follow industry best practices and utilize modern software engineering principles to ensure the robustness and flexibility of our codebase.


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

### Agile Development Approach

We adopt an agile development approach, breaking down the development process into iterative sprints, each focused on delivering specific functionalities or components of the system. This iterative approach allows us to adapt to changing requirements, incorporate feedback, and deliver incremental value to stakeholders.

### Continuous Integration and Deployment (CI/CD)

We implement a CI/CD pipeline to automate the build, test, and deployment processes, ensuring the reliability and consistency of our codebase. With automated testing and deployment, we can rapidly iterate on new features and enhancements while maintaining code quality and stability.

### Modular Code Design

Our codebase is structured into modular components, each responsible for specific functionalities or tasks within the system. By adhering to the principles of modularity, we promote code reuse, facilitate maintainability, and enable scalability as our system evolves.

#### Component Breakdown:

1. **Image Processing Module:** Located in the `image_processing/` directory, this module encapsulates the logic for processing uploaded images. The `lambda_function.py` file contains the code for the Lambda function responsible for image processing tasks.

2. **Notifications Service:** The notifications service, found in the `notifications/` directory, handles the publishing of evaluation results. The `lambda_destination.py` file configures Lambda Destinations for message delivery.

3. **Data Retrieval Module:** Within the `data_retrieval/` directory, the `api_gateway/` subdirectory contains the code for the Lambda function responsible for data retrieval tasks via API Gateway.

### Infrastructure as Code

Our infrastructure is defined and managed using Infrastructure as Code (IaC) principles. The `infrastructure/` directory contains scripts for setting up various AWS resources required by our system.

- **Lambda Setup:** The `lambda_setup.py` script sets up Lambda functions.
- **SNS Setup:** The `sns_setup.py` script configures Amazon SNS topics.
- **API Gateway Setup:** The `api_gateway_setup.py` script provisions Amazon API Gateway.
- **DynamoDB Setup:** The `dynamodb_setup.py` script creates DynamoDB tables.
- **S3 Setup:** The `s3_setup.py` script initializes S3 buckets.

Additionally, the `config/` directory contains a `configurations.json` file, serving as a configuration file for infrastructure setup.

### Version Control and Collaboration

We utilize version control systems such as Git and collaborative development platforms like GitHub to manage code changes, track issues, and facilitate collaboration among team members. Version control ensures code consistency, enables code review processes, and provides a centralized repository for project assets.

By adhering to these methodologies and adopting a modular code design approach, we aim to build a robust, scalable, and maintainable Passport Photo Validation system that meets the evolving needs of our users and stakeholders.

## Data Modeling

Data modeling plays a crucial role in designing the schema for storing and accessing data efficiently in DynamoDB. We utilize a NoSQL approach to model our data, leveraging the flexibility and scalability offered by DynamoDB.

### Table Structure

We model our data in DynamoDB using the following attributes:

| Attribute        | Description                                              |
|------------------|----------------------------------------------------------|
| FileName         | Name of the uploaded file                                |
| ValidationResult| Result of the photo validation process (e.g., approved/rejected)|
| FailureReasons   | Reasons for rejection, if any (stored as JSON)          |
| Timestamp        | Timestamp indicating when the validation occurred        |
| FileLocation     | Location of the file in the S3 bucket                   |
| FaceDetails      | Facial details extracted during image processing (stored as JSON)|

### Sample Item Attributes

```json
{
    "FileName": "example.jpg",
    "ValidationResult": "approved",
    "FailureReasons": "{\"reason\": \"None\"}",
    "Timestamp": "2022-02-20T12:00:00",
    "FileLocation": "s3://bucket-name/example.jpg",
    "FaceDetails": "{\"eyes\": \"open\", \"smile\": \"none\"}"
}
```

## Contribution

We would love to receive contributions from the community to improve and expand our Passport Photo Validation project! If you have ideas, suggestions for improvements, or would like to collaborate on development, please let us know! You can contribute in various ways, including:

- Reporting issues or bugs you encounter.
- Proposing new features or enhancements.
- Submitting pull requests with code to address issues or implement new features.

We look forward to working with you to grow this project and make it even better!

## Contact

If you have any questions, comments, or simply want to get in touch with us, please feel free to do so. You can find us on the following platforms:

- **GitHub:** [Link to Repository]([https://github.com/diegovillatoromx/passport-facial-analysis-automation/edit/main/README.md])
- **Email:** diegovillatoromx@gmail.com
- **Twitter:** [@diegovillatomx](https://twitter.com/diegovillatomx)
- **LinkedIn:** [DiegoVillatoromx](https://www.linkedin.com/in/diegovillatoromx)

We look forward to hearing from you soon!


