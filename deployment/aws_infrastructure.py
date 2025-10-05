"""
AWS Infrastructure Setup for MS AI Curriculum System
Deploy to msai.syzygyx.com
"""

import boto3
import json
from typing import Dict, List, Any
import os
from datetime import datetime

class AWSInfrastructureManager:
    """Manages AWS infrastructure for MS AI curriculum system"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.session = boto3.Session(region_name=region)
        self.ec2 = self.session.client('ec2')
        self.rds = self.session.client('rds')
        self.s3 = self.session.client('s3')
        self.cloudfront = self.session.client('cloudfront')
        self.route53 = self.session.client('route53')
        self.acm = self.session.client('acm')
        self.iam = self.session.client('iam')
        
    def create_vpc_and_networking(self) -> Dict[str, str]:
        """Create VPC and networking infrastructure"""
        print("🌐 Creating VPC and networking infrastructure...")
        
        # Create VPC
        vpc_response = self.ec2.create_vpc(
            CidrBlock='10.0.0.0/16',
            TagSpecifications=[
                {
                    'ResourceType': 'vpc',
                    'Tags': [
                        {'Key': 'Name', 'Value': 'msai-vpc'},
                        {'Key': 'Project', 'Value': 'MS-AI-Curriculum'},
                        {'Key': 'Environment', 'Value': 'Production'}
                    ]
                }
            ]
        )
        vpc_id = vpc_response['Vpc']['VpcId']
        
        # Create Internet Gateway
        igw_response = self.ec2.create_internet_gateway(
            TagSpecifications=[
                {
                    'ResourceType': 'internet-gateway',
                    'Tags': [
                        {'Key': 'Name', 'Value': 'msai-igw'},
                        {'Key': 'Project', 'Value': 'MS-AI-Curriculum'}
                    ]
                }
            ]
        )
        igw_id = igw_response['InternetGateway']['InternetGatewayId']
        
        # Attach Internet Gateway to VPC
        self.ec2.attach_internet_gateway(
            InternetGatewayId=igw_id,
            VpcId=vpc_id
        )
        
        # Create public subnet
        public_subnet_response = self.ec2.create_subnet(
            VpcId=vpc_id,
            CidrBlock='10.0.1.0/24',
            AvailabilityZone=f'{self.region}a',
            TagSpecifications=[
                {
                    'ResourceType': 'subnet',
                    'Tags': [
                        {'Key': 'Name', 'Value': 'msai-public-subnet'},
                        {'Key': 'Project', 'Value': 'MS-AI-Curriculum'}
                    ]
                }
            ]
        )
        public_subnet_id = public_subnet_response['Subnet']['SubnetId']
        
        # Create private subnet
        private_subnet_response = self.ec2.create_subnet(
            VpcId=vpc_id,
            CidrBlock='10.0.2.0/24',
            AvailabilityZone=f'{self.region}b',
            TagSpecifications=[
                {
                    'ResourceType': 'subnet',
                    'Tags': [
                        {'Key': 'Name', 'Value': 'msai-private-subnet'},
                        {'Key': 'Project', 'Value': 'MS-AI-Curriculum'}
                    ]
                }
            ]
        )
        private_subnet_id = private_subnet_response['Subnet']['SubnetId']
        
        # Create route table for public subnet
        route_table_response = self.ec2.create_route_table(
            VpcId=vpc_id,
            TagSpecifications=[
                {
                    'ResourceType': 'route-table',
                    'Tags': [
                        {'Key': 'Name', 'Value': 'msai-public-rt'},
                        {'Key': 'Project', 'Value': 'MS-AI-Curriculum'}
                    ]
                }
            ]
        )
        route_table_id = route_table_response['RouteTable']['RouteTableId']
        
        # Add route to Internet Gateway
        self.ec2.create_route(
            RouteTableId=route_table_id,
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=igw_id
        )
        
        # Associate route table with public subnet
        self.ec2.associate_route_table(
            RouteTableId=route_table_id,
            SubnetId=public_subnet_id
        )
        
        return {
            'vpc_id': vpc_id,
            'igw_id': igw_id,
            'public_subnet_id': public_subnet_id,
            'private_subnet_id': private_subnet_id,
            'route_table_id': route_table_id
        }
    
    def create_security_groups(self, vpc_id: str) -> Dict[str, str]:
        """Create security groups for the application"""
        print("🔒 Creating security groups...")
        
        # Web server security group
        web_sg_response = self.ec2.create_security_group(
            GroupName='msai-web-sg',
            Description='Security group for MS AI web servers',
            VpcId=vpc_id,
            TagSpecifications=[
                {
                    'ResourceType': 'security-group',
                    'Tags': [
                        {'Key': 'Name', 'Value': 'msai-web-sg'},
                        {'Key': 'Project', 'Value': 'MS-AI-Curriculum'}
                    ]
                }
            ]
        )
        web_sg_id = web_sg_response['GroupId']
        
        # Add inbound rules for web server
        self.ec2.authorize_security_group_ingress(
            GroupId=web_sg_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 443,
                    'ToPort': 443,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                }
            ]
        )
        
        # Database security group
        db_sg_response = self.ec2.create_security_group(
            GroupName='msai-db-sg',
            Description='Security group for MS AI database',
            VpcId=vpc_id,
            TagSpecifications=[
                {
                    'ResourceType': 'security-group',
                    'Tags': [
                        {'Key': 'Name', 'Value': 'msai-db-sg'},
                        {'Key': 'Project', 'Value': 'MS-AI-Curriculum'}
                    ]
                }
            ]
        )
        db_sg_id = db_sg_response['GroupId']
        
        # Add inbound rule for database
        self.ec2.authorize_security_group_ingress(
            GroupId=db_sg_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 5432,
                    'ToPort': 5432,
                    'UserIdGroupPairs': [{'GroupId': web_sg_id}]
                }
            ]
        )
        
        return {
            'web_sg_id': web_sg_id,
            'db_sg_id': db_sg_id
        }
    
    def create_rds_database(self, subnet_group_name: str, security_group_id: str) -> str:
        """Create RDS PostgreSQL database"""
        print("🗄️ Creating RDS PostgreSQL database...")
        
        # Create DB subnet group
        self.rds.create_db_subnet_group(
            DBSubnetGroupName=subnet_group_name,
            DBSubnetGroupDescription='Subnet group for MS AI database',
            SubnetIds=[],  # Will be populated with private subnets
            Tags=[
                {'Key': 'Name', 'Value': 'msai-db-subnet-group'},
                {'Key': 'Project', 'Value': 'MS-AI-Curriculum'}
            ]
        )
        
        # Create RDS instance
        db_response = self.rds.create_db_instance(
            DBInstanceIdentifier='msai-database',
            DBInstanceClass='db.t3.micro',
            Engine='postgres',
            EngineVersion='15.4',
            MasterUsername='msai_admin',
            MasterUserPassword='MSAI_Admin_2024!',
            AllocatedStorage=20,
            StorageType='gp2',
            VpcSecurityGroupIds=[security_group_id],
            DBSubnetGroupName=subnet_group_name,
            BackupRetentionPeriod=7,
            MultiAZ=False,
            PubliclyAccessible=False,
            StorageEncrypted=True,
            Tags=[
                {'Key': 'Name', 'Value': 'msai-database'},
                {'Key': 'Project', 'Value': 'MS-AI-Curriculum'}
            ]
        )
        
        return db_response['DBInstance']['DBInstanceIdentifier']
    
    def create_s3_bucket(self, bucket_name: str) -> str:
        """Create S3 bucket for static assets"""
        print("🪣 Creating S3 bucket for static assets...")
        
        try:
            self.s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': self.region}
            )
        except self.s3.exceptions.BucketAlreadyExists:
            print(f"Bucket {bucket_name} already exists")
        
        # Configure bucket for static website hosting
        self.s3.put_bucket_website(
            Bucket=bucket_name,
            WebsiteConfiguration={
                'IndexDocument': {'Suffix': 'index.html'},
                'ErrorDocument': {'Key': 'error.html'}
            }
        )
        
        # Set bucket policy for public read access
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }
        
        self.s3.put_bucket_policy(
            Bucket=bucket_name,
            Policy=json.dumps(bucket_policy)
        )
        
        return bucket_name
    
    def create_cloudfront_distribution(self, s3_bucket: str) -> str:
        """Create CloudFront distribution for global content delivery"""
        print("🌍 Creating CloudFront distribution...")
        
        distribution_response = self.cloudfront.create_distribution(
            DistributionConfig={
                'CallerReference': f'msai-{datetime.now().strftime("%Y%m%d%H%M%S")}',
                'Origins': {
                    'Quantity': 1,
                    'Items': [
                        {
                            'Id': 'S3-msai-assets',
                            'DomainName': f'{s3_bucket}.s3.amazonaws.com',
                            'S3OriginConfig': {
                                'OriginAccessIdentity': ''
                            }
                        }
                    ]
                },
                'DefaultCacheBehavior': {
                    'TargetOriginId': 'S3-msai-assets',
                    'ViewerProtocolPolicy': 'redirect-to-https',
                    'TrustedSigners': {
                        'Enabled': False,
                        'Quantity': 0
                    },
                    'ForwardedValues': {
                        'QueryString': False,
                        'Cookies': {'Forward': 'none'}
                    },
                    'MinTTL': 0,
                    'DefaultTTL': 3600,
                    'MaxTTL': 86400
                },
                'Comment': 'MS AI Curriculum System - Static Assets',
                'Enabled': True,
                'PriceClass': 'PriceClass_100'
            }
        )
        
        return distribution_response['Distribution']['Id']
    
    def create_ec2_instance(self, subnet_id: str, security_group_id: str, key_name: str) -> str:
        """Create EC2 instance for the application"""
        print("🖥️ Creating EC2 instance...")
        
        # Get latest Ubuntu AMI
        ami_response = self.ec2.describe_images(
            Owners=['099720109477'],  # Canonical
            Filters=[
                {'Name': 'name', 'Values': ['ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*']},
                {'Name': 'state', 'Values': ['available']}
            ]
        )
        
        latest_ami = sorted(ami_response['Images'], key=lambda x: x['CreationDate'])[-1]
        ami_id = latest_ami['ImageId']
        
        # Create EC2 instance
        instance_response = self.ec2.run_instances(
            ImageId=ami_id,
            MinCount=1,
            MaxCount=1,
            InstanceType='t3.medium',
            KeyName=key_name,
            SecurityGroupIds=[security_group_id],
            SubnetId=subnet_id,
            UserData=self._get_user_data_script(),
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {'Key': 'Name', 'Value': 'msai-web-server'},
                        {'Key': 'Project', 'Value': 'MS-AI-Curriculum'},
                        {'Key': 'Environment', 'Value': 'Production'}
                    ]
                }
            ]
        )
        
        instance_id = instance_response['Instances'][0]['InstanceId']
        
        # Allocate Elastic IP
        eip_response = self.ec2.allocate_address(
            Domain='vpc',
            TagSpecifications=[
                {
                    'ResourceType': 'elastic-ip',
                    'Tags': [
                        {'Key': 'Name', 'Value': 'msai-eip'},
                        {'Key': 'Project', 'Value': 'MS-AI-Curriculum'}
                    ]
                }
            ]
        )
        
        eip_allocation_id = eip_response['AllocationId']
        
        # Associate Elastic IP with instance
        self.ec2.associate_address(
            InstanceId=instance_id,
            AllocationId=eip_allocation_id
        )
        
        return instance_id
    
    def _get_user_data_script(self) -> str:
        """Get user data script for EC2 instance setup"""
        return '''#!/bin/bash
# Update system
apt-get update
apt-get upgrade -y

# Install Python 3.11 and pip
apt-get install -y python3.11 python3.11-pip python3.11-venv

# Install Node.js and npm
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs

# Install Docker
apt-get install -y docker.io
systemctl start docker
systemctl enable docker

# Install nginx
apt-get install -y nginx
systemctl start nginx
systemctl enable nginx

# Install PostgreSQL client
apt-get install -y postgresql-client

# Create application directory
mkdir -p /opt/msai
cd /opt/msai

# Clone application (replace with actual repository)
# git clone https://github.com/your-username/MSAI.git .

# Install Python dependencies
# pip3.11 install -r requirements.txt

# Install Node.js dependencies
# npm install

# Configure nginx
cat > /etc/nginx/sites-available/msai << 'EOF'
server {
    listen 80;
    server_name msai.syzygyx.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /opt/msai/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

ln -s /etc/nginx/sites-available/msai /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx

# Create systemd service for the application
cat > /etc/systemd/system/msai.service << 'EOF'
[Unit]
Description=MS AI Curriculum System
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/msai
Environment=PATH=/opt/msai/venv/bin
ExecStart=/opt/msai/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable msai
# systemctl start msai  # Will be started after application deployment
'''
    
    def setup_domain_dns(self, domain: str, eip_address: str) -> bool:
        """Setup DNS for the domain (requires Route 53 hosted zone)"""
        print(f"🌐 Setting up DNS for {domain}...")
        
        try:
            # Get hosted zone ID (assuming syzygyx.com is already in Route 53)
            hosted_zones = self.route53.list_hosted_zones()
            zone_id = None
            
            for zone in hosted_zones['HostedZones']:
                if zone['Name'] == 'syzygyx.com.':
                    zone_id = zone['Id'].split('/')[-1]
                    break
            
            if not zone_id:
                print("❌ Hosted zone for syzygyx.com not found in Route 53")
                return False
            
            # Create A record for msai.syzygyx.com
            self.route53.change_resource_record_sets(
                HostedZoneId=zone_id,
                ChangeBatch={
                    'Changes': [
                        {
                            'Action': 'UPSERT',
                            'ResourceRecordSet': {
                                'Name': 'msai.syzygyx.com',
                                'Type': 'A',
                                'TTL': 300,
                                'ResourceRecords': [
                                    {'Value': eip_address}
                                ]
                            }
                        }
                    ]
                }
            )
            
            print(f"✅ DNS record created for {domain}")
            return True
            
        except Exception as e:
            print(f"❌ Error setting up DNS: {e}")
            return False
    
    def create_ssl_certificate(self, domain: str) -> str:
        """Create SSL certificate for the domain"""
        print(f"🔒 Creating SSL certificate for {domain}...")
        
        try:
            cert_response = self.acm.request_certificate(
                DomainName=domain,
                ValidationMethod='DNS',
                SubjectAlternativeNames=[f'www.{domain}'],
                Tags=[
                    {'Key': 'Name', 'Value': f'{domain}-cert'},
                    {'Key': 'Project', 'Value': 'MS-AI-Curriculum'}
                ]
            )
            
            cert_arn = cert_response['CertificateArn']
            print(f"✅ SSL certificate requested: {cert_arn}")
            return cert_arn
            
        except Exception as e:
            print(f"❌ Error creating SSL certificate: {e}")
            return None
    
    def deploy_infrastructure(self, domain: str = 'msai.syzygyx.com') -> Dict[str, Any]:
        """Deploy complete infrastructure"""
        print("🚀 Starting AWS infrastructure deployment...")
        
        # Step 1: Create VPC and networking
        networking = self.create_vpc_and_networking()
        
        # Step 2: Create security groups
        security_groups = self.create_security_groups(networking['vpc_id'])
        
        # Step 3: Create S3 bucket
        bucket_name = f'msai-assets-{datetime.now().strftime("%Y%m%d")}'
        s3_bucket = self.create_s3_bucket(bucket_name)
        
        # Step 4: Create CloudFront distribution
        cloudfront_id = self.create_cloudfront_distribution(s3_bucket)
        
        # Step 5: Create EC2 instance
        key_name = 'msai-key'  # Assumes key pair exists
        instance_id = self.create_ec2_instance(
            networking['public_subnet_id'],
            security_groups['web_sg_id'],
            key_name
        )
        
        # Step 6: Get Elastic IP address
        eip_response = self.ec2.describe_addresses()
        eip_address = None
        for address in eip_response['Addresses']:
            if address.get('InstanceId') == instance_id:
                eip_address = address['PublicIp']
                break
        
        # Step 7: Setup DNS
        if eip_address:
            self.setup_domain_dns(domain, eip_address)
        
        # Step 8: Create SSL certificate
        ssl_cert_arn = self.create_ssl_certificate(domain)
        
        return {
            'vpc_id': networking['vpc_id'],
            'instance_id': instance_id,
            'eip_address': eip_address,
            's3_bucket': s3_bucket,
            'cloudfront_id': cloudfront_id,
            'ssl_cert_arn': ssl_cert_arn,
            'domain': domain
        }

def main():
    """Main deployment function"""
    print("🎓 MS AI Curriculum System - AWS Deployment")
    print("=" * 50)
    
    # Initialize infrastructure manager
    infra_manager = AWSInfrastructureManager(region='us-east-1')
    
    # Deploy infrastructure
    deployment_info = infra_manager.deploy_infrastructure('msai.syzygyx.com')
    
    print("\n🎉 Deployment Summary:")
    print("=" * 30)
    print(f"Domain: {deployment_info['domain']}")
    print(f"EC2 Instance: {deployment_info['instance_id']}")
    print(f"Public IP: {deployment_info['eip_address']}")
    print(f"S3 Bucket: {deployment_info['s3_bucket']}")
    print(f"CloudFront: {deployment_info['cloudfront_id']}")
    print(f"SSL Certificate: {deployment_info['ssl_cert_arn']}")
    
    print("\n📋 Next Steps:")
    print("1. Wait for EC2 instance to fully initialize (5-10 minutes)")
    print("2. SSH into the instance and deploy the application")
    print("3. Configure SSL certificate validation")
    print("4. Test the application at https://msai.syzygyx.com")
    
    return deployment_info

if __name__ == "__main__":
    main()