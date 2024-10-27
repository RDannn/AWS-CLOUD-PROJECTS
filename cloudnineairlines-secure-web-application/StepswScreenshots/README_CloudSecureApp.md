![Architecture Diagram](cloudappdia.jpg)


Step 1: Initial Setup
Follow these setup instructions:
Navigate to EC2 in the AWS Console (N. Virginia region preferred). Ensure full administrative access.
![SIGNIN Services Screenshot](screenshots/signin.png)



![EC2 Services Screenshot](screenshots/ec2services.png)



Under "Network & Security," create a new security group:
frontendALB:
![FESGC Services Screenshot](screenshots/fesgc.png)



Inbound Rule: HTTPS, Source: Anywhere (IPv4)
![FEHTTPS Services Screenshot](screenshots/fehttps.png)



Outbound Rule: HTTP to allow secure traffic forwarding to backend EC2 instances.
![FETOBE Services Screenshot](screenshots/fetobe.png)



backendEC2:
Inbound Rule: HTTP, Source: frontendALB security group for secure forwarding.
![BETOFE Services Screenshot](screenshots/betofe.png)



Outbound: Leave default (for Apache installation later).
![BEOUT Services Screenshot](screenshots/beout.png)



🔐 KMS Key Setup:

Search KMS and create a symmetric key, named FFKey.
![KMS Services Screenshot](screenshots/kms.png)



![FFKEY Services Screenshot](screenshots/ffkey.png)




Administrator: Set as your account
![KEYA Services Screenshot](screenshots/keya.png)



Key usage permissions: Assign AWSServiceRoleForAutoScaling
![KEYU Services Screenshot](screenshots/keyu.png)



Use this KMS key to encrypt EC2 instance volumes, which will be set up in an Auto Scaling launch template.

🔗 SSL Certificate:

Open Certificate Manager in a new tab. Request a certificate for your hosted domain (e.g., example.com) and a subdomain (e.g., alb.example.com).
![ACM Services Screenshot](screenshots/acm.png)



![ACMR Services Screenshot](screenshots/acmr.png)



![ACMRR Services Screenshot](screenshots/acmrr.png)



![DOMAIN Services Screenshot](screenshots/domain.png)



![ACMP Services Screenshot](screenshots/acmp.png)



![ACMI Services Screenshot](screenshots/acmi.png)



![ACMV Services Screenshot](screenshots/acmv.png)



Use DNS validation in Route 53 to validate ownership. This single certificate applies to both the CloudFront distribution and ALB.



![R53 Services Screenshot](screenshots/r53.png)



![DNSCN Services Screenshot](screenshots/dnscn.png)




📢 SNS Topic:

Go to SNS > Topics > Create Topic.
![SNS Services Screenshot](screenshots/sns.png)



![SNST Services Screenshot](screenshots/snst.png)



Set as Standard type, name it FrequentFlyerNotify.
![FSNS Services Screenshot](screenshots/fsns.png)



Add a subscription with Email as the protocol and input your email for notifications. Confirm via your email to activate.
![SUB Services Screenshot](screenshots/sub.png)



You're All Set!
This step-by-step guide is just the beginning of your journey with Cloud Nine Airlines' secure AWS architecture. Ready for take-off? ✈️




Step 2: Setting Up VPC Infrastructure, IAM Role, S3 Bucket, and Launch Template
Welcome to Step 2! Let’s build out the core infrastructure components: a VPC, IAM role, S3 bucket, and Launch Template. Let’s create!

1. VPC Setup
Go to VPC in AWS Console and select "Subnets" > Create subnet.
![VPC Services Screenshot](screenshots/vpc.png)



![VPCS Services Screenshot](screenshots/vpcs.png)



Use the Default VPC, and configure your subnets:
Name: "Private-1A" with the next available CIDR block.
![PRIVA Services Screenshot](screenshots/priva.png)



Click Add new subnet, name it "Private-1B" and add its CIDR block.
Next, navigate to Route Tables > Create route table. Name it "RTPrivate" and associate it with the Default VPC.
![PRRT Services Screenshot](screenshots/prrt.png)



![ROUT Services Screenshot](screenshots/rout.png)



In Subnet associations, link both Private-1A and Private-1B to "RTPrivate."
Go to NAT Gateways and create one for public internet access:
Name it "nat-gw-2day" and select the public subnet in us-east-1a.
Set Connectivity type to "Public" and allocate an Elastic IP.
![NAT Services Screenshot](screenshots/nat.png)



![NATA Services Screenshot](screenshots/nata.png)
In Route Tables, update RTPrivate by adding a route to the NAT gateway:
Destination: 0.0.0.0/0, Target: "nat-gw-2day."
![RONAT Services Screenshot](screenshots/ronat.png)



2. IAM Role for EC2
Open IAM and go to Roles > Create role.
![IAM Services Screenshot](screenshots/iam.png)



![ROLE Services Screenshot](screenshots/role.png)



![EC2T Services Screenshot](screenshots/ec2t.png)
For Use case, choose EC2, then add permissions:
AmazonS3ReadOnlyAccess for S3 file access
AmazonSSMManagedInstanceCore for EC2 management with SSM.
![IAMSSM Services Screenshot](screenshots/iamssm.png)



Name this role "xs-ec2-ssm-s3" and Create role.
3. S3 Bucket Setup
Open S3 and Create bucket:
Name it "sourcefiles-4-ec2-webapp" (ensure the name is unique).
![S3 Services Screenshot](screenshots/s3.png)



![s3c Services Screenshot](screenshots/s3c.png)




Select your new bucket and Upload the following files from Step1: index.html, styles.css, and frequentflyer.jpeg.
![WEBF Services Screenshot](screenshots/webf.png)



These will serve as content for the frequent flyer web app and will be pulled by EC2 instances on launch.
4. Launch Template Configuration
In EC2 under Launch Templates, follow the instructions to set it up.
![SLT Services Screenshot](screenshots/slt.png)


![T2 Services Screenshot](screenshots/t2.png)



![AMI Services Screenshot](screenshots/ami.png)



![SSG Services Screenshot](screenshots/ssg.png)


![FFE Services Screenshot](screenshots/ffe.png)



Prepare the user data script:
Open user-data-bs.md from Step1, and replace "YOUR-BUCKET-HERE" with the name of your S3 bucket.
This script installs the web server, retrieves files from S3, and sets up the web app with metadata from the instance.
Copy and paste this code into the User data field in the launch template, then Create launch template.
![USERD Services Screenshot](screenshots/userd.png)
That’s it for Step 2! We’ve built the foundational AWS infrastructure for our secure, scalable Cloud Nine Airlines Frequent Flyer web application. Ready for the next step? Let’s soar! 🛫










Step 3: Setting Up Auto Scaling Group, ALB, and CloudFront Distribution
We’re almost there! In Step 3, we’ll create an Auto Scaling Group (ASG), Application Load Balancer (ALB), and CloudFront Distribution for our frequent flyer web application. To ensure security, we’ll add a custom header in CloudFront that the ALB requires for access. This keeps our app secure by making CloudFront the only entry point to the backend. Let’s dive in!

1. Auto Scaling Group Setup
In EC2, go to Auto Scaling Groups and click Create an Auto Scaling group.
Name: "ASG1"
Select Launch Template: Choose "SecureLT" from Step 2.
Under Network, ensure the Default VPC is selected.
![ASG Services Screenshot](screenshots/asg.png)



Availability Zones and Subnets: Select "Private-1A" and "Private-1B".
![PRIVAB Services Screenshot](screenshots/privab.png)



Group Size: Set Desired Capacity, Minimum, and Maximum to 2.
Skip load balancer setup for now and review settings before clicking Create Auto Scaling Group.
The ASG will now deploy two EC2 instances using our user data script from Step 2. It ensures high availability by adjusting instance count based on load.
2. ALB Configuration
In EC2, scroll to Load Balancers and select Application Load Balancer.
Name: "ALB1"
Scheme: Internet-facing
IP Address Type: IPv4
Select the Default VPC and Availability Zones (us-east-1a and us-east-1b).
Security Group: Use "frontendALB" and configure it for HTTPS (Port 443).
![ALB Services Screenshot](screenshots/alb.png)



![ASGCAPACITY Services Screenshot](screenshots/asgcapacity.png)



Secure Listener: Attach an SSL certificate for your domain under "Secure listener settings."
Next, create a Target Group:
Name: "TG1"
Target Type: Instance, Protocol: HTTP, Port: 80.
Do not register instances manually; the ASG will handle them.
![SECACM Services Screenshot](screenshots/secacm.png)



![TG Services Screenshot](screenshots/tg.png)



![TGH Services Screenshot](screenshots/tgh.png)



In ALB1, select TG1 as the target group, then create the load balancer.
3. CloudFront Distribution
In CloudFront, select Create a CloudFront distribution.
Origin Domain: Choose the ALB1 Elastic Load Balancer.
Protocol Policy: Set to HTTPS Only.
Cache Policy: Caching Disabled (to balance availability across zones without caching).
Alternate Domain Name (CNAME): Add your apex domain (e.g., aafiumuszik.click).
Custom SSL Certificate: Use your ACM certificate.
Default Root Object: "index.html"
Create the distribution (deployment may take a few minutes).
![CF Services Screenshot](screenshots/cf.png)



![CACH Services Screenshot](screenshots/cach.png)



![CFEDIT Services Screenshot](screenshots/cfedit.png)



![ALBC Services Screenshot](screenshots/albc.png)




4. Route 53 Record Creation
In Route 53, go to your hosted zone.
Create a new A Record (Alias):
Alias to CloudFront Distribution: Select your CloudFront distribution.
Record name: Leave blank for apex domain.
Create another A Record for alb.yourdomainname:
Alias to Application and Classic Load Balancer: Select ALB1.
![APEXALC Services Screenshot](screenshots/apexalc.png)



![ALIAS Services Screenshot](screenshots/alias.png)



![CRR Services Screenshot](screenshots/crr.png)



5. Update ASG to Use Target Group
Back in EC2 under Auto Scaling Groups, select ASG1 > Actions > Edit.
In Load balancing, select "Application Load Balancer target groups" and choose TG1.
![APPLO Services Screenshot](screenshots/applo.png)



![AGSEDIT Services Screenshot](screenshots/agsedit.png)



6. Implement CloudFront Header Security
Open CloudFront > Distribution, go to Origins, select Edit.
Add a Custom Header:
Header Name: "FF-Custom-Header"
Header Value: "value-246810"
![ADDCUSTOMHEADCF Services Screenshot](screenshots/addcustomheadcf.png)
Save changes.



7. Configure ALB Rule for Header Security
In EC2 under Load Balancers, select ALB1 > Listeners and Rules.
Select the HTTPS:443 listener and go to Manage Rules, "Add Rule".
Input "http header" for the name then click Next.
![HTTPA Services Screenshot](screenshots/httpa.png)



Click the "Add condition" box.
![ADDCON Services Screenshot](screenshots/addcon.png)
In the "Rule condition types" click the arrow in the box and select "Http header".



![RULECON Services Screenshot](screenshots/rulecon.png)



For HTTP header name: "FF-Custom-Header", HTTP header value is: "value-246810".
Click Confirm, then Next.
![HTTPH Services Screenshot](screenshots/httph.png)



![HV Services Screenshot](screenshots/hv.png)
Routing actions select "Forward to target groups". Under "Target Groups" select "TG1" then Next.
Set rule priority to "1" click Next then Create.

Edit the Default Rule for HTTPS:443 listener:
Select "Default" then "Actions" then "Edit Rule".
For "Routing actions" select "Return fixed response" 
Action: In "Response body" input: "DO NOT ENTER!! NO ENTRY NO ACCESS! DENIED!!!!!!!". Then click Save changes.
![RETURNFIXED Services Screenshot](screenshots/returnfixed.png)



Testing and Verification
Test CloudFront Access:
Open your apex domain in a browser (e.g., https://aafiumuszik.click). You should see the Cloud Nine Frequent Flyer webpage with availability zone rotation.
Test ALB Access without CloudFront:
Enter the subdomain (https://alb.yourdomainname). The fixed response should display "DO NOT ENTER!! NO ENTRY NO ACCESS! DENIED!!!!!!!".
![APEXWEB Services Screenshot](screenshots/apexweb.png)



![WEBA Services Screenshot](screenshots/weba.png)



![WEBB Services Screenshot](screenshots/webb.png)



![ALBWEB Services Screenshot](screenshots/albweb.png)



![DONOT Services Screenshot](screenshots/donot.png)
Congratulations! You’ve secured your Cloud Nine application, ensuring CloudFront is the sole access point. The architecture is coming together beautifully! But there’s more to secure—let’s move forward!




Step 4: Adding Logging, AWS Config, and Amazon Inspector for Enhanced Security
We’re continuing to strengthen the security of our Cloud Nine web application! In this step, we’ll add S3 buckets to log traffic from both the ALB and CloudFront. We’ll also use AWS Config to check for compliance with best practices, and Amazon Inspector to scan for vulnerabilities in our EC2 instances. Let’s get started!

1. Create a Logging Bucket in S3
In the S3 console, create a new bucket for logging traffic:

Name the bucket: my-frequentflyer-log (or something unique).
Complete the bucket creation and then open it.
Go to Permissions for the bucket and paste the following bucket policy to allow logging:

json
Copy code
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
Replace BUCKET-NAME with your bucket’s name and YOUR-ACCOUNT-ID with your AWS Account ID. Click Save changes.
![BUCKETLOG Services Screenshot](screenshots/bucketlog.png)

2. Enable ALB Logging
In EC2, go to Load Balancers, select ALB1, then Actions > Edit Load Balancer Attributes.
Scroll to Access logs and enable them:
Browse S3 and select the logging bucket you created.
Click Save Changes to start logging traffic information to the S3 bucket.
![ALBLOG Services Screenshot](screenshots/alblog.png)



3. Enable CloudFront Logging
In CloudFront, select your distribution and click Edit.
Scroll to Standard logging and enable it:
Logging bucket: Select the same logging bucket.
Log Prefix: Enter cloudfront for easy file organization.
Enable ACLs and click Save changes.
![CFLOG Services Screenshot](screenshots/cflog.png)
Now, go to your apex domain in a browser (e.g., https://aafiumuszik.click) and refresh it a few times to generate traffic logs. In a few minutes, check your S3 bucket under AWSLogs to confirm the logging files from ALB and CloudFront.

4. Enable AWS Config Rules
In the Config service, select Rules > Add Rule.
![CONFIGRULES Services Screenshot](screenshots/configrules.png)



Add the following AWS Managed Rules to monitor security settings:
s3-bucket-logging-enabled
alb-waf-enabled (will show as non-compliant until we configure WAF later)
cloudfront-accesslogs-enabled
![S3BEN Services Screenshot](screenshots/s3ben.png)



For each rule, click Next and Save. AWS Config will now monitor these settings for compliance, and you can check the Rules page to see if any resources are non-compliant.
5. Check EC2 Instances in Systems Manager (SSM)
In Systems Manager (SSM), go to Fleet Manager and verify that your EC2 instances appear.
Since we configured the EC2 instance role in the Launch Template (Step 2), our instances are managed by SSM.
Click Run Command to confirm SSM access for instance management.
![SSM Services Screenshot](screenshots/ssm.png)



![SSMRUN Services Screenshot](screenshots/ssmrun.png)



6. Amazon Inspector for Vulnerability Scanning
Open the Inspector service and start the free 15-day trial if needed.
Under Findings or By instance, check if your EC2 instances are listed and monitored.
Inspector will run periodic scans for vulnerabilities, patch requirements, and other security best practices. Check the findings regularly to maintain a secure environment.
![INSPECTORP Services Screenshot](screenshots/inspectorp.png)



![INSPECTORI Services Screenshot](screenshots/inspectori.png)



7. Review Logs for ALB and CloudFront
Go back to S3 > my-frequentflyer-log and open AWSLogs to view logs for ALB and CloudFront:
Drill down into ALB logs to view HTTPS traffic data, including URLs and IP addresses.
Open CloudFront logs for details on GET requests, user-agent data, and request sources.
8. Review Config Compliance
Return to AWS Config to confirm compliance with security best practices.
You should see results indicating whether your resources comply with rules such as s3-bucket-logging-enabled and cloudfront-accesslogs-enabled.
![ALBD Services Screenshot](screenshots/albd.png)



![ALBALOGS Services Screenshot](screenshots/albalogs.png)
Great work! You’re now actively logging and monitoring your infrastructure for compliance and vulnerabilities. We’re not done yet, though—let’s move on to enable AWS WAF for even stronger web application security.




Step 5: Finalizing Security with AWS WAF
Congratulations! We’ve successfully built a secure architecture for the Cloud Nine Airlines frequent flyer application. Our multi-layered approach prioritizes security, ensuring a seamless and protected experience for our users. In this final step, we’ll add a Web ACL with AWS WAF to manage connection rates and guard against IP exhaustion attacks.

1. Set Up AWS WAF Web ACL
Go to AWS WAF by typing "WAF" in the search bar, then open the service in a new tab.
Click Create Web ACL and configure it as follows:
Scope: Select Amazon CloudFront.
Web ACL name: Enter SecureWebACL.
![WAF Services Screenshot](screenshots/waf.png)



![WEBACL Services Screenshot](screenshots/webacl.png)



![REACL Services Screenshot](screenshots/reacl.png)



Click Add AWS Resources and choose your CloudFront distribution. Click Next.
2. Create a Rate-Based Rule
Select Add my own rules and groups > Rule builder:
Rule name: Enter Rate150.
Rule type: Choose Rate-based rule.
Rate limit: Set this to 150 requests per 5 minutes.
Action: Block any IP address exceeding this rate to prevent high traffic from a single source.
Click Add rule, then proceed through the remaining setup pages by selecting Next. Finally, click Create Web ACL to activate it.
3. Test the WAF Rate-Based Rule in CloudShell
Open CloudShell in the AWS Console (cloud icon in the top navigation).
![RATE150 Services Screenshot](screenshots/rate150.png)



![BLOCK Services Screenshot](screenshots/block.png)



Run the following command to simulate high traffic from a single IP (CloudShell) by requesting the site 150 times:

bash
Copy code
for i in {1..150}; do curl https://YOUR-DOMAIN-NAME/; done
Note: Replace YOUR-DOMAIN-NAME with your actual CloudFront distribution domain.
![FOR Services Screenshot](screenshots/for.png)



After running the command, you should receive messages like "Request could not be satisfied" due to the WAF rule blocking excessive requests. However, accessing the web app in a standard browser should still function normally within typical request limits.
![FORLOOPERROR Services Screenshot](screenshots/forlooperror.png)



Clean-Up Reminder
Before you finish, remember to delete all resources (like EC2 instances, S3 buckets, WAF, and CloudFront) to avoid unwanted charges.

By following these steps, you’ve achieved a secure, high-performing architecture for Cloud Nine Airlines, providing passengers with a safe and enjoyable experience while accessing their frequent flyer information. ✈️ Fly high ✈️ in the sky ☁️ on Cloud Nine Airlines! 



Reference:
https://github.com/nealdct



