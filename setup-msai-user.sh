#!/bin/bash
# Setup MS AI User - Run with AWS Admin credentials

set -e

echo "🚀 Setting up MS AI User..."

# Create the msai user
echo "Creating msai user..."
aws iam create-user \
    --user-name msai \
    --tags Key=Project,Value=MS-AI-Curriculum Key=Environment,Value=Production Key=CreatedBy,Value=Admin

# Create and attach the policy
echo "Creating MS AI policy..."
aws iam create-policy \
    --policy-name MS-AI-Curriculum-Policy \
    --policy-document file://msai-user-policy.json \
    --description "Policy for MS AI Curriculum System deployment and management"

# Get the policy ARN
POLICY_ARN=$(aws iam list-policies --query 'Policies[?PolicyName==`MS-AI-Curriculum-Policy`].Arn' --output text)

echo "Attaching policy to msai user..."
aws iam attach-user-policy \
    --user-name msai \
    --policy-arn $POLICY_ARN

# Create access keys
echo "Creating access keys for msai user..."
aws iam create-access-key --user-name msai > msai-access-keys.json

echo "✅ MS AI user setup complete!"
echo "📋 Access keys saved to: msai-access-keys.json"
echo ""
echo "🔧 Next steps:"
echo "1. Configure AWS CLI with new credentials:"
echo "   aws configure --profile msai"
echo "2. Use the profile for MS AI operations:"
echo "   aws --profile msai ec2 describe-instances"
echo ""
echo "⚠️  Keep the access keys secure!"