
📌 Mission Statement
Cloud Nine Airlines values the privacy and security of our customers' personal information. We ensure secure handling of data, including frequent flyer accounts, and have strong guardrails to prevent fraud. Your account is in good hands with Cloud Nine Airlines.

🛫 Welcome Aboard!
This project is a secure, AWS-based architecture for our Frequent Flyer Program. It provides customers safe access to their accounts, tracks miles, companion info, trip details, and more. We'll use various AWS services to keep this environment secure and functional, including security groups, KMS keys, IAM, SNS Topics, and Amazon Certificate Manager.

Architecture Overview:

Private Auto Scaling EC2 Instances (secured by a security group)
Public Application Load Balancer (ALB) in a public subnet, securely linked to the EC2 instances
CloudFront Distribution for our frontend, which forwards customer connections securely to the ALB and retrieves content from the EC2 Auto Scaling group
SSL with AWS Certificate Manager for CloudFront and ALB, for secure data transmission
Network ACLs for additional subnet security and KMS to encrypt EC2 volumes
SNS Notifications for proactive alerts.
