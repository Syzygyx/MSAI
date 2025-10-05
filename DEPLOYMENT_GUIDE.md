# MS AI Curriculum System - AWS Deployment Guide
## Deploy to msai.syzygyx.com

This guide will help you deploy the MS AI Curriculum System to AWS and host it at `msai.syzygyx.com`.

---

## 🚀 Quick Start Deployment

### Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** configured with credentials
3. **Docker** and **Docker Compose** installed
4. **Domain** `syzygyx.com` configured in Route 53 (or external DNS)

### One-Command Deployment

```bash
# Run the complete deployment script
python deployment/deploy_to_aws.py
```

This will automatically:
- ✅ Create AWS infrastructure (VPC, EC2, RDS, S3, CloudFront)
- ✅ Deploy the application to EC2
- ✅ Configure DNS for msai.syzygyx.com
- ✅ Set up SSL certificate (manual step)
- ✅ Create production-ready Docker containers

---

## 🏗️ Infrastructure Overview

### AWS Resources Created

| Resource | Purpose | Configuration |
|----------|---------|---------------|
| **VPC** | Network isolation | 10.0.0.0/16 CIDR |
| **EC2 Instance** | Application server | t3.medium Ubuntu 22.04 |
| **RDS PostgreSQL** | Database | db.t3.micro, 20GB |
| **S3 Bucket** | Static assets | Public read access |
| **CloudFront** | CDN | Global content delivery |
| **Route 53** | DNS | msai.syzygyx.com |
| **ACM Certificate** | SSL/TLS | HTTPS encryption |

### Network Architecture

```
Internet → CloudFront → EC2 (nginx) → FastAPI App
                    ↓
                 S3 (static files)
                    ↓
                 RDS (database)
```

---

## 📋 Manual Deployment Steps

If you prefer to deploy manually or need to customize the setup:

### Step 1: Prepare Environment

```bash
# Clone the repository
git clone https://github.com/your-username/MSAI.git
cd MSAI

# Install dependencies
pip install boto3 docker-compose

# Configure AWS credentials
aws configure
```

### Step 2: Generate Docker Configuration

```bash
# Generate all Docker files
python deployment/docker_setup.py

# Configure environment variables
cp deployment/.env.template deployment/.env
# Edit deployment/.env with your values
```

### Step 3: Deploy Infrastructure

```bash
# Deploy AWS infrastructure
python deployment/aws_infrastructure.py
```

### Step 4: Deploy Application

```bash
# Deploy to EC2
python deployment/deploy_to_aws.py
```

---

## 🔧 Configuration

### Environment Variables

Key environment variables in `.env`:

```bash
# Database
DATABASE_URL=postgresql://msai_user:password@db:5432/msai_db
DB_PASSWORD=your_secure_password

# Security
SECRET_KEY=your_secret_key_minimum_32_characters
JWT_SECRET_KEY=your_jwt_secret_key

# Domain
DOMAIN=msai.syzygyx.com
ALLOWED_HOSTS=msai.syzygyx.com,www.msai.syzygyx.com

# AWS
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
S3_BUCKET_NAME=msai-assets-production
```

### SSL Certificate Setup

After deployment, complete SSL setup:

```bash
# SSH into EC2 instance
ssh -i deployment/msai-production-key.pem ubuntu@your-ec2-ip

# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d msai.syzygyx.com

# Test automatic renewal
sudo certbot renew --dry-run
```

---

## 🐳 Docker Services

The deployment uses Docker Compose with the following services:

### Web Application
- **FastAPI** backend server
- **Port**: 8000
- **Health Check**: `/health`

### Database
- **PostgreSQL 15** with Alpine Linux
- **Port**: 5432 (internal)
- **Data Persistence**: Docker volume

### Redis
- **Caching** and session storage
- **Port**: 6379 (internal)

### Nginx
- **Reverse proxy** and load balancer
- **Ports**: 80 (HTTP), 443 (HTTPS)
- **SSL termination**

### Worker Processes
- **Celery workers** for background tasks
- **Celery beat** for scheduled tasks

---

## 📊 Monitoring & Logging

### Health Checks

- **Application**: `https://msai.syzygyx.com/health`
- **Database**: Internal PostgreSQL health check
- **Redis**: Internal Redis ping check

### Logs

```bash
# View application logs
docker-compose logs -f web

# View all service logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f nginx
```

### Monitoring Endpoints

- **Metrics**: `https://msai.syzygyx.com/metrics`
- **Status**: `https://msai.syzygyx.com/status`
- **API Docs**: `https://msai.syzygyx.com/docs`

---

## 🔒 Security Features

### Network Security
- **VPC** with private subnets
- **Security groups** with minimal access
- **SSL/TLS** encryption (HTTPS only)

### Application Security
- **Rate limiting** on API endpoints
- **CORS** configuration
- **Security headers** (HSTS, XSS protection)
- **Input validation** and sanitization

### Data Security
- **Database encryption** at rest
- **Secure password** hashing
- **JWT token** authentication
- **Environment variable** protection

---

## 🚨 Troubleshooting

### Common Issues

#### 1. EC2 Instance Not Accessible
```bash
# Check security group rules
aws ec2 describe-security-groups --group-ids sg-xxxxxxxxx

# Verify instance status
aws ec2 describe-instances --instance-ids i-xxxxxxxxx
```

#### 2. Database Connection Issues
```bash
# Check RDS status
aws rds describe-db-instances --db-instance-identifier msai-database

# Test connection from EC2
psql -h your-rds-endpoint -U msai_user -d msai_db
```

#### 3. SSL Certificate Issues
```bash
# Check certificate status
sudo certbot certificates

# Renew certificate manually
sudo certbot renew --force-renewal
```

#### 4. Application Not Starting
```bash
# Check Docker containers
docker-compose ps

# View application logs
docker-compose logs web

# Restart services
docker-compose restart
```

### Debug Commands

```bash
# SSH into EC2 instance
ssh -i deployment/msai-production-key.pem ubuntu@your-ec2-ip

# Check service status
sudo systemctl status msai

# View application logs
sudo journalctl -u msai -f

# Check Docker containers
docker ps -a

# Test application locally
curl http://localhost:8000/health
```

---

## 📈 Scaling & Performance

### Horizontal Scaling

```bash
# Scale web services
docker-compose up -d --scale web=3

# Scale worker processes
docker-compose up -d --scale worker=2
```

### Vertical Scaling

```bash
# Upgrade EC2 instance type
aws ec2 modify-instance-attribute --instance-id i-xxxxxxxxx --instance-type t3.large
```

### Database Scaling

```bash
# Enable Multi-AZ for RDS
aws rds modify-db-instance --db-instance-identifier msai-database --multi-az
```

---

## 💰 Cost Optimization

### Estimated Monthly Costs (US East 1)

| Resource | Type | Cost/Month |
|----------|------|------------|
| **EC2** | t3.medium | ~$30 |
| **RDS** | db.t3.micro | ~$15 |
| **S3** | 100GB storage | ~$3 |
| **CloudFront** | 1TB transfer | ~$10 |
| **Route 53** | Hosted zone | ~$0.50 |
| **Total** | | **~$58.50** |

### Cost Optimization Tips

1. **Use Spot Instances** for non-critical workloads
2. **Enable S3 Intelligent Tiering** for storage optimization
3. **Use CloudFront caching** to reduce origin requests
4. **Schedule RDS** for development environments
5. **Monitor usage** with AWS Cost Explorer

---

## 🔄 Backup & Recovery

### Automated Backups

```bash
# RDS automated backups (7 days retention)
# S3 versioning enabled
# EBS snapshots for EC2
```

### Manual Backup

```bash
# Database backup
pg_dump -h your-rds-endpoint -U msai_user msai_db > backup.sql

# Application backup
tar -czf msai-backup.tar.gz /opt/msai/
```

### Disaster Recovery

1. **RDS Point-in-Time Recovery**
2. **S3 Cross-Region Replication**
3. **EC2 AMI Creation**
4. **Infrastructure as Code** (Terraform/CloudFormation)

---

## 📞 Support & Maintenance

### Regular Maintenance Tasks

- **Weekly**: Security updates and patches
- **Monthly**: Performance monitoring review
- **Quarterly**: Cost optimization analysis
- **Annually**: Security audit and penetration testing

### Support Contacts

- **Technical Issues**: Check logs and monitoring
- **AWS Support**: Use AWS Support Center
- **Application Issues**: Review application documentation

---

## 🎯 Success Metrics

### Deployment Success Criteria

- ✅ **HTTPS** accessible at msai.syzygyx.com
- ✅ **All services** running and healthy
- ✅ **Database** connected and responsive
- ✅ **SSL certificate** valid and auto-renewing
- ✅ **Monitoring** and logging configured
- ✅ **Backup** strategies implemented

### Performance Targets

- **Response Time**: < 2 seconds
- **Uptime**: > 99.9%
- **SSL Grade**: A+ rating
- **Page Load**: < 3 seconds

---

*This deployment guide ensures the MS AI Curriculum System is properly deployed to AWS with production-ready configurations, security measures, and monitoring capabilities.*