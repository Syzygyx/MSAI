# MS AI User Setup Guide

## 🎯 **Objective**
Create a dedicated AWS user (`msai`) with appropriate permissions for managing the MS AI Curriculum System deployment and infrastructure.

## 📋 **Prerequisites**
- AWS Admin account access (to create IAM users)
- AWS CLI configured with admin credentials
- Access to AWS Console or CLI

## 🚀 **Setup Process**

### **Step 1: Run the Setup Script**
```bash
# Make the script executable
chmod +x setup-msai-user.sh

# Run with admin credentials
./setup-msai-user.sh
```

### **Step 2: Configure AWS CLI**
```bash
# Configure AWS CLI with msai profile
aws configure --profile msai

# Enter the credentials from msai-access-keys.json when prompted
```

### **Step 3: Test Configuration**
```bash
# Verify the user identity
aws --profile msai sts get-caller-identity

# Test EC2 access
aws --profile msai ec2 describe-instances

# Test Route 53 access
aws --profile msai route53 list-hosted-zones
```

## 🔐 **Permissions Included**

The `msai` user will have the following permissions:

### **EC2 Full Access**
- Create, terminate, and manage instances
- Manage security groups and key pairs
- Access instance metadata and console output

### **Route 53 Full Access**
- Manage DNS records and hosted zones
- Update A records for msai.syzygyx.com

### **S3 Access**
- Access MS AI curriculum buckets
- Upload and download application files

### **CloudWatch Logs**
- Create and manage log groups
- Monitor application logs

### **Systems Manager (SSM)**
- Access EC2 instances via SSM
- Execute commands remotely
- Manage sessions

## 📁 **Files Created**

1. **`msai-user-policy.json`** - IAM policy document
2. **`setup-msai-user.sh`** - Automated setup script
3. **`msai-access-keys.json`** - Generated access keys (keep secure!)
4. **`msai-aws-config-template.txt`** - Configuration instructions

## 🔧 **Usage Examples**

### **Deploy MS AI System**
```bash
# Create EC2 instance
aws --profile msai ec2 run-instances \
    --image-id ami-0c02fb55956c7d316 \
    --instance-type t3.medium \
    --key-name msai-production-key

# Update DNS
aws --profile msai route53 change-resource-record-sets \
    --hosted-zone-id Z3NYTS7HNUXA87 \
    --change-batch file://dns-update.json
```

### **Monitor System**
```bash
# Check instance status
aws --profile msai ec2 describe-instances \
    --query 'Reservations[0].Instances[0].{State:State.Name,IP:PublicIpAddress}'

# Access logs
aws --profile msai logs describe-log-groups \
    --log-group-name-prefix "/aws/ec2/msai"
```

### **SSM Access**
```bash
# List instances for SSM
aws --profile msai ssm describe-instance-information

# Start SSM session
aws --profile msai ssm start-session \
    --target i-1234567890abcdef0
```

## ⚠️ **Security Notes**

1. **Keep Access Keys Secure**: Store `msai-access-keys.json` securely
2. **Rotate Keys Regularly**: Update access keys periodically
3. **Principle of Least Privilege**: Only grant necessary permissions
4. **Monitor Usage**: Check CloudTrail for user activity

## 🎉 **Benefits**

- **Dedicated Permissions**: Tailored for MS AI system needs
- **Better Security**: Separate from admin account
- **Easier Management**: Clear ownership and responsibility
- **Audit Trail**: Track all MS AI-related activities

## 🔄 **Next Steps After Setup**

1. **Test All Permissions**: Verify each service works
2. **Deploy Application**: Use msai user for deployment
3. **Set Up Monitoring**: Configure CloudWatch alarms
4. **Document Access**: Share credentials securely with team

---

**Note**: This setup requires AWS Admin permissions. If you don't have admin access, share these files with someone who does, or request the permissions to be added to your current account.