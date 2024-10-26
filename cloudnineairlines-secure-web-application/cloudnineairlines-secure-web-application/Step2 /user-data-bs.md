#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
cd /var/www/html
aws s3 cp s3://sourcefiles-4-ec2-webapp/index.html ./
aws s3 cp s3://sourcefiles-4-ec2-webapp/frequentflyer.jpeg ./
aws s3 cp s3://sourcefiles-4-ec2-webapp/styles.css ./
cp index.html index.txt

# Randomly alternate between us-east-1a and us-east-1b
AZ_CHOICE=$(( RANDOM % 2 ))
if [[ "$AZ_CHOICE" -eq 0 ]]; then
    AZ="Content Delivered From: us-east-1a"
else
    AZ="Content Delivered From: us-east-1b"
fi

sed "s/AZID/$AZ/" /var/www/html/index.txt > /var/www/html/index.html
