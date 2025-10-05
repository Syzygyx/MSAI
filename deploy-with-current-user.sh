#!/bin/bash
# Deploy MS AI Curriculum System with Current User Permissions

set -e

echo "🚀 Deploying MS AI Curriculum System with current user..."

# Check current user
echo "Current AWS user:"
aws sts get-caller-identity --query 'Arn' --output text

# Check available instances
echo "Current EC2 instances:"
aws ec2 describe-instances --query 'Reservations[*].Instances[*].{ID:InstanceId,State:State.Name,IP:PublicIpAddress}' --output table

# Check DNS status
echo "Current DNS for msai.syzygyx.com:"
nslookup msai.syzygyx.com || echo "DNS not resolving"

# Create a working deployment
echo "Creating new EC2 instance with working deployment..."

# Terminate any existing instances
EXISTING_INSTANCES=$(aws ec2 describe-instances --query 'Reservations[*].Instances[?State.Name==`running`].InstanceId' --output text)
if [ ! -z "$EXISTING_INSTANCES" ]; then
    echo "Terminating existing instances: $EXISTING_INSTANCES"
    aws ec2 terminate-instances --instance-ids $EXISTING_INSTANCES
    sleep 30
fi

# Create new instance
echo "Launching new instance..."
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id ami-0c02fb55956c7d316 \
    --count 1 \
    --instance-type t3.medium \
    --key-name msai-production-key \
    --security-group-ids sg-0e019bce3a4c6cde4 \
    --user-data file://clean_deploy.sh \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=msai-curriculum-working}]' \
    --query 'Instances[0].InstanceId' \
    --output text)

echo "Instance created: $INSTANCE_ID"

# Wait for instance to start
echo "Waiting for instance to start..."
aws ec2 wait instance-running --instance-ids $INSTANCE_ID

# Get public IP
PUBLIC_IP=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)
echo "Public IP: $PUBLIC_IP"

# Update DNS
echo "Updating DNS..."
aws route53 change-resource-record-sets --hosted-zone-id Z3NYTS7HNUXA87 --change-batch "{
  \"Changes\": [
    {
      \"Action\": \"UPSERT\",
      \"ResourceRecordSet\": {
        \"Name\": \"msai.syzygyx.com\",
        \"Type\": \"A\",
        \"TTL\": 300,
        \"ResourceRecords\": [
          {
            \"Value\": \"$PUBLIC_IP\"
          }
        ]
      }
    }
  ]
}"

echo "DNS updated to point to $PUBLIC_IP"

# Wait for deployment to complete
echo "Waiting for application deployment..."
sleep 120

# Test the application
echo "Testing application..."
curl -s http://$PUBLIC_IP:8000/health || echo "Direct IP test failed"
curl -s http://msai.syzygyx.com:8000/health || echo "Domain test failed"

echo "✅ Deployment complete!"
echo "🌐 Application should be available at: http://msai.syzygyx.com"
echo "📊 API Documentation: http://msai.syzygyx.com/docs"
echo "🔍 Health Check: http://msai.syzygyx.com/health"