# Step 1 - Create Security Groups, KMS Key, ACM Certificate, and SNS Topic

## Create Security Groups

Name: frontendALB
Inbound rule: HTTPS from anywhere IPv4
Outbound rule: HTTP to the backendEC2 SG

Name: backendEC2
Inbound rule: HTTP from the frontendALB SG
Outbound rule: All traffic to 0.0.0.0/0 (for downloading installation files)

## AWS KMS

1. Create a Symmetric key called FFKey
2. Set your individual account as the key administrator
3. For key usage set your individual account and 'AWSServiceRoleForAutoScaling'

## AWS Certificate Manager

1. Request a public certificate
2. Add your domain name, e.g. cloudnine.com and add another name to the certificate for alb.cloudnine.com (replacing with your domain name)
3. Use DNS validation option and submit the validation to create the records in Route 53

## Create an SNS Topic

1. Create a standard topic called "FrequentFlyerNotify"
2. Create an email subscription for your email address

# Step 2 - Create VPC infra, IAM Role, S3 Bucket, and Launch Template

## Create VPC infrastructure

- Create two private subnets in us-east-1 default VPC

Name: Private-1A
CIDR: 172.31.96.0/20
AZ: us-east-1a

Name: Private-1B
CIDR: 172.31.112.0/20
AZ: us-east-1b

- Create a route table

Name: RTPrivate
Associations: the two private subnets

- Create a NAT gateway

Name: nat-gw-2day
Subnet: Public subnet in the default VPC
Routes: Add a route to the private route table

## Create IAM Role

Name: xs-ec2-ssm-s3
Use Case: EC2
Permissions policies:
- 'AmazonS3ReadOnlyAccess'
- 'AmazonSSMManagedInstanceCore'

## Create S3 Bucket

Name: sourcefiles-4-ec2-webapp (add numbers/characters to make it unique or add your own bucket name)
Objects: Add the following objects from the Code > cloudnineairlines-secure-web-application > Step2 directory:
- index.html
- styles.css
- frequentflyer.jpeg

## Create a Launch Template

1. Add your bucket name to the user-data-bs.md file from the Step2 directory
2. Create a launch template named SecureLT
3. Choose the Amazon Linux 2023 AMI
4. Select a t2.micro instance type
5. Don't include a key pair
6. Choose the backendEC2 security group
7. Encrypt the EBS volume using the KMS key created earlier
8. Select the 'xs-ec2-ssm-s3' instance profile
9. Paste the user data (make sure bucket name is updated)

# Step 3 - Create Auto Scaling Group, ALB, and CloudFront Distribution

## Create ASG

1. Call it "ASG1"
2. Select the launch template created earlier
3. Select the two private subnets in the default VPC
4. Set group size values to 2 for each option

## Create an ALB

1. Call it "ALB1"
2. Make it internet facing
3. Select the public subnets in us-east-1a and us-east-1b in the default VPC
4. Select the "frontendALB" security group
5. Configure an HTTPS listener with the public certificate from ACM
6. Forward to a new TG called "TG1"
7. Attach the TG to the ASG

## Create a CloudFront Distribution

1. Select the ALB
2. Set the origin domain to your ALB subdomain, e.g. alb.cloudnine.com
3. Set protocol  to "HTTPS only"
4. Set cache policy to "CachingDisabled"
5. Do not protect with AWS WAF
6. Select the SSL/TLS certificate from ACM
7. Add the apex domain name in the alternate domain name (CNAMEs) field, e.g. cloudnine.com
8. Add the index.html as the default root object


## Create records in Route 53

- Create two records

Name: apex, e.g. cloudnine.com
Type: A
Value/Route traffic to: CloudFront distribution

Name: ALB subdomain, e.g. alb.cloudnine.com
Type: A
Value/Route traffic to: ALB

Go to the EC2 tab, then Auto Scaling Groups.
Select ASG1 > Actions > Edit.
Scroll to Load Balancers and select Application or Gateway Load Balancer target groups.
Choose TG1 and click Update.
Navigate to Target Groups > Targets to view your instances. They’ll show Initial health status, then switch to Healthy if configured correctly.

## Configure Custom Header

1. Edit CloudFront origin
2. For "Origin Custom Headers" add the following header:
- Header Name: FF-Custom-Header
- Value: value-246810




## Configure conditional forwarding rule in ALB 

1. EC2 under Load Balancers, select ALB1 > Listeners and Rules.
2. Select the HTTPS:443 listener and go to Manage Rules, "Add Rule".
3. Input "http header" for the name then click Next.
4. "Add condition" box.
5. "Rule condition types" click the arrow in the box and select "Http header".
6. HTTP header name: "FF-Custom-Header", HTTP header value is: "value-246810".
7. Click Confirm, then Next.
8. Routing actions select "Forward to target groups". Under "Target Groups" select "TG1" then Next.
9. Set rule priority to "1" click Next then Create.
10. Edit the Default Rule for HTTPS:443 listener:
11. Select "Default" then "Actions" then "Edit Rule".
12. For "Routing actions" select "Return fixed response" 
13. Action: In "Response body" input: "DO NOT ENTER!! NO ENTRY NO ACCESS! DENIED!!!!!!!". Then click Save changes.



Testing and Verification 
Test CloudFront Access:
Open your apex domain in a browser (e.g., https://aafiumuszik.click). You should see the Cloud Nine Frequent Flyer webpage with availability zone rotation.
Test ALB Access without CloudFront:
Enter the subdomain (https://alb.yourdomainname). The fixed response should display "DO NOT ENTER!! NO ENTRY NO ACCESS! DENIED!!!!!!!".

# Step 4 - Enable logging, configuration management, and security inspection

## Enable logging for the ALB

1. Create an S3 bucket for logging (my-frequentflyer-log) e.g.
2. Add the following bucket policy (modify ONLY the BUCKET-NAME and YOUR-ACCOUNT-ID fields)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::127311923021:root"
      },
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::BUCKET-NAME/AWSLogs/YOUR-ACCOUNT-ID/*"
    }
  ]
}
```

3. Edit load balancer attributes
4. Enable access logs
5. Select the S3 bucket and save

## Enable logging for the CloudFront distribution

1. Edit the distrubition
2. Enable standard logging
3. Configure the same bucket as the ALB logging
4. Enable ACLs
5. Specify the prefix "cloudfront"

## Configure rules in AWS Config

1. Create two rules in AWS Config using the following managed rules:

- 's3-bucket-logging-enabled'
- 'alb-waf-enabled'
- 'cloudfront-accesslogs-enabled'


## Setup Inspector using Systems Manager

1. In SSM Run Command check that the inspector agent updates have run
2. Go to Amazon Inspector and specify your account ID for delegated administrator account and activate the trial
3. Check the findings for the EC2 instances

# Step 5 - Add AWS WAF

## Create an AWS WAF WebACL

1. Create a WebACL

Name: SecureWebACL
Resource type: CloudFront distributions
Associated resources: select the distribution

2. Create a rule for the WebACL

Name: Rate150
Type: Rate-based rule
Rate limit: 150
Action: Block

3. Use the following command on CloudShell to trip the WAF rule (modify the domain name)

```bash
for i in {1..140}; do curl https://YOUR-DOMAIN-NAME/; done
```



