# SmartParcel AWS Serverless Project

NET 214 - Network Programming  
Student: Khalid Al Marri  
Student ID: 20200001899  
Region: ap-southeast-2  

## Project Overview
SmartParcel is a serverless parcel delivery system deployed on AWS. It allows drivers to create parcels and update parcel status, customers to check parcel status, and administrators to list active deliveries.

## AWS Services Used
- API Gateway
- AWS Lambda
- DynamoDB
- S3
- SQS
- SNS
- IAM
- VPC
- CloudWatch
- CloudTrail
- CloudFormation

## Architecture
Customers, drivers, and admins send HTTPS requests to API Gateway. API Gateway invokes the API Lambda function. The API Lambda stores parcel data in DynamoDB, accesses S3 for proof photos, and sends status update events to SQS. SQS triggers the notifier Lambda, which publishes email notifications through SNS.

## Main Resources
- DynamoDB table: smartparcel-parcels-khalid20200001899
- S3 bucket: smartparcel-photos-khalid20200001899
- API Lambda: smartparcel-api-khalid20200001899
- Notifier Lambda: smartparcel-notifier-khalid20200001899
- SQS queue: smartparcel-events-khalid20200001899
- SQS DLQ: smartparcel-events-dlq-khalid20200001899
- SNS topic: smartparcel-alerts-khalid20200001899
- API Gateway: SmartParcel-API-khalid20200001899
- VPC: smartparcel-vpc-khalid20200001899

## API Endpoints
- POST /parcels
- GET /parcels/{id}
- GET /parcels
- PUT /parcels/{id}/status
- DELETE /parcels/{id}

## Deployment
The infrastructure is deployed using CloudFormation.

## Testing
Testing was performed using curl from AWS CloudShell. A concurrent load test was also performed using ThreadPoolExecutor with 20 workers, and all 20 requests returned 201 Created.

## Files
- cloudformation/smartparcel20200001899_khalid.yaml
- lambda/api_lambda.py
- lambda/notifier_lambda.py
- tests/load_test.py
- docs/architecture_diagram.png
- docs/SmartParcel_Final_Report_20200001899_Khalid.pdf
