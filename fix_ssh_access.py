#!/usr/bin/env python3
"""
Fix SSH Access to MS AI EC2 Instance
This script will diagnose and fix SSH connectivity issues
"""

import boto3
import json
import time
from botocore.exceptions import ClientError, NoCredentialsError

class SSHFixer:
    def __init__(self):
        """Initialize AWS clients"""
        try:
            self.ec2 = boto3.client('ec2')
            self.ssm = boto3.client('ssm')
            print("✅ AWS clients initialized successfully")
        except NoCredentialsError:
            print("❌ AWS credentials not found. Please configure AWS CLI or set environment variables.")
            exit(1)
        except Exception as e:
            print(f"❌ Error initializing AWS clients: {e}")
            exit(1)
    
    def find_msai_instance(self):
        """Find the MS AI EC2 instance"""
        print("🔍 Searching for MS AI EC2 instance...")
        
        try:
            # Search for instances with MS AI tags or by IP
            response = self.ec2.describe_instances(
                Filters=[
                    {
                        'Name': 'tag:Project',
                        'Values': ['MS-AI-Curriculum', 'MSAI']
                    }
                ]
            )
            
            instances = []
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    if instance['State']['Name'] in ['running', 'stopped']:
                        instances.append(instance)
            
            if not instances:
                # Try to find by IP address
                print("🔍 Searching by IP address 44.220.164.13...")
                response = self.ec2.describe_instances()
                for reservation in response['Reservations']:
                    for instance in reservation['Instances']:
                        if instance.get('PublicIpAddress') == '44.220.164.13':
                            instances.append(instance)
            
            if instances:
                instance = instances[0]
                print(f"✅ Found MS AI instance: {instance['InstanceId']}")
                print(f"   State: {instance['State']['Name']}")
                print(f"   Public IP: {instance.get('PublicIpAddress', 'N/A')}")
                print(f"   Private IP: {instance.get('PrivateIpAddress', 'N/A')}")
                return instance
            else:
                print("❌ No MS AI instance found")
                return None
                
        except ClientError as e:
            print(f"❌ Error finding instance: {e}")
            return None
    
    def check_security_groups(self, instance):
        """Check and fix security group rules"""
        print("🔍 Checking security groups...")
        
        try:
            security_groups = instance['SecurityGroups']
            
            for sg in security_groups:
                sg_id = sg['GroupId']
                print(f"🔍 Checking security group: {sg_id}")
                
                # Get security group details
                response = self.ec2.describe_security_groups(GroupIds=[sg_id])
                security_group = response['SecurityGroups'][0]
                
                print(f"   Group Name: {security_group['GroupName']}")
                print(f"   Description: {security_group['Description']}")
                
                # Check for SSH access (port 22)
                ssh_rules = []
                for rule in security_group['IpPermissions']:
                    if rule.get('FromPort') == 22 and rule.get('ToPort') == 22:
                        ssh_rules.append(rule)
                
                if not ssh_rules:
                    print("   ❌ No SSH rules found - adding SSH access...")
                    self.add_ssh_rule(sg_id)
                else:
                    print("   ✅ SSH rules found:")
                    for rule in ssh_rules:
                        for ip_range in rule.get('IpRanges', []):
                            print(f"      - {ip_range.get('CidrIp', 'N/A')}: {ip_range.get('Description', 'No description')}")
                
                # Check for HTTP access (port 80)
                http_rules = []
                for rule in security_group['IpPermissions']:
                    if rule.get('FromPort') == 80 and rule.get('ToPort') == 80:
                        http_rules.append(rule)
                
                if not http_rules:
                    print("   ❌ No HTTP rules found - adding HTTP access...")
                    self.add_http_rule(sg_id)
                else:
                    print("   ✅ HTTP rules found")
                
        except ClientError as e:
            print(f"❌ Error checking security groups: {e}")
    
    def add_ssh_rule(self, security_group_id):
        """Add SSH access rule to security group"""
        try:
            self.ec2.authorize_security_group_ingress(
                GroupId=security_group_id,
                IpPermissions=[
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 22,
                        'ToPort': 22,
                        'IpRanges': [
                            {
                                'CidrIp': '0.0.0.0/0',
                                'Description': 'SSH access from anywhere'
                            }
                        ]
                    }
                ]
            )
            print("   ✅ SSH rule added successfully")
        except ClientError as e:
            if 'already exists' in str(e).lower():
                print("   ⚠️  SSH rule already exists")
            else:
                print(f"   ❌ Error adding SSH rule: {e}")
    
    def add_http_rule(self, security_group_id):
        """Add HTTP access rule to security group"""
        try:
            self.ec2.authorize_security_group_ingress(
                GroupId=security_group_id,
                IpPermissions=[
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 80,
                        'ToPort': 80,
                        'IpRanges': [
                            {
                                'CidrIp': '0.0.0.0/0',
                                'Description': 'HTTP access from anywhere'
                            }
                        ]
                    }
                ]
            )
            print("   ✅ HTTP rule added successfully")
        except ClientError as e:
            if 'already exists' in str(e).lower():
                print("   ⚠️  HTTP rule already exists")
            else:
                print(f"   ❌ Error adding HTTP rule: {e}")
    
    def check_instance_status(self, instance):
        """Check instance status and start if stopped"""
        instance_id = instance['InstanceId']
        state = instance['State']['Name']
        
        print(f"🔍 Instance state: {state}")
        
        if state == 'stopped':
            print("🚀 Starting stopped instance...")
            try:
                self.ec2.start_instances(InstanceIds=[instance_id])
                
                # Wait for instance to start
                print("⏳ Waiting for instance to start...")
                waiter = self.ec2.get_waiter('instance_running')
                waiter.wait(InstanceIds=[instance_id])
                
                # Get updated instance info
                response = self.ec2.describe_instances(InstanceIds=[instance_id])
                instance = response['Reservations'][0]['Instances'][0]
                print("✅ Instance started successfully")
                
            except ClientError as e:
                print(f"❌ Error starting instance: {e}")
                return instance
        elif state == 'running':
            print("✅ Instance is running")
        else:
            print(f"⚠️  Instance is in {state} state")
        
        return instance
    
    def test_ssh_connection(self, instance):
        """Test SSH connection to instance"""
        public_ip = instance.get('PublicIpAddress')
        if not public_ip:
            print("❌ No public IP address found")
            return False
        
        print(f"🔍 Testing SSH connection to {public_ip}...")
        
        import subprocess
        try:
            # Test SSH connection
            result = subprocess.run([
                'ssh', '-i', 'msai-production-key.pem', 
                '-o', 'ConnectTimeout=10',
                '-o', 'StrictHostKeyChecking=no',
                f'ubuntu@{public_ip}',
                'echo "SSH connection successful"'
            ], capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                print("✅ SSH connection successful")
                return True
            else:
                print(f"❌ SSH connection failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ SSH connection timed out")
            return False
        except FileNotFoundError:
            print("❌ SSH key file not found: msai-production-key.pem")
            return False
        except Exception as e:
            print(f"❌ Error testing SSH: {e}")
            return False
    
    def fix_ssh_access(self):
        """Main function to fix SSH access"""
        print("🚀 MS AI SSH Access Fixer")
        print("=" * 50)
        
        # Find the instance
        instance = self.find_msai_instance()
        if not instance:
            print("❌ Cannot proceed without finding the instance")
            return False
        
        # Check and fix instance status
        instance = self.check_instance_status(instance)
        
        # Check and fix security groups
        self.check_security_groups(instance)
        
        # Test SSH connection
        if self.test_ssh_connection(instance):
            print("\n🎉 SSH access fixed successfully!")
            print(f"🌐 You can now SSH to: ubuntu@{instance.get('PublicIpAddress')}")
            print("🔑 Using key: msai-production-key.pem")
            return True
        else:
            print("\n❌ SSH access still not working")
            print("🔍 Additional troubleshooting needed:")
            print("   1. Check if SSH service is running on the instance")
            print("   2. Verify the key file permissions")
            print("   3. Check if the instance has a public IP")
            print("   4. Try using AWS Systems Manager Session Manager")
            return False
    
    def use_ssm_session(self, instance):
        """Use AWS Systems Manager Session Manager as alternative"""
        instance_id = instance['InstanceId']
        print(f"🔍 Trying AWS Systems Manager Session Manager for {instance_id}...")
        
        try:
            # Check if SSM agent is running
            response = self.ssm.describe_instance_information(
                Filters=[
                    {
                        'Key': 'InstanceIds',
                        'Values': [instance_id]
                    }
                ]
            )
            
            if response['InstanceInformationList']:
                print("✅ SSM agent is running - you can use Session Manager")
                print(f"🔗 Start session with: aws ssm start-session --target {instance_id}")
                return True
            else:
                print("❌ SSM agent not running on instance")
                return False
                
        except ClientError as e:
            print(f"❌ Error checking SSM: {e}")
            return False

def main():
    """Main function"""
    fixer = SSHFixer()
    
    # Try to fix SSH access
    if fixer.fix_ssh_access():
        print("\n✅ SSH access restored!")
    else:
        print("\n🔄 Trying alternative access method...")
        instance = fixer.find_msai_instance()
        if instance and fixer.use_ssm_session(instance):
            print("✅ You can use AWS Systems Manager Session Manager instead")
        else:
            print("❌ Both SSH and SSM access failed")
            print("🔍 Manual intervention required")

if __name__ == "__main__":
    main()