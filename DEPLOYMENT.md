# MS AI Deployment Guide

This guide explains how to set up automatic deployment from GitHub to the MS AI server at `msai.syzygyx.com`.

## 🚀 Quick Setup

### 1. Server Configuration

The deployment targets:
- **Server**: `3.84.224.16` (AWS EC2)
- **Domain**: `msai.syzygyx.com`
- **Deploy Path**: `/var/www/msai`
- **Web Server**: Nginx

### 2. GitHub Secrets Setup

You need to configure these secrets in your GitHub repository:

1. Go to your repository → Settings → Secrets and variables → Actions
2. Add these repository secrets:

```
SERVER_SSH_KEY    # Your private SSH key for server access
SERVER_HOST       # 3.84.224.16
SERVER_USER       # ubuntu (or your server username)
```

### 3. SSH Key Setup

Generate an SSH key pair if you don't have one:

```bash
ssh-keygen -t rsa -b 4096 -C "github-actions@msai"
```

Add the public key to your server:
```bash
ssh-copy-id -i ~/.ssh/id_rsa.pub ubuntu@3.84.224.16
```

Add the private key to GitHub Secrets as `SERVER_SSH_KEY`.

## 🔄 Deployment Methods

### Automatic Deployment (Recommended)

The GitHub Action automatically deploys when you push to the `main` branch:

```bash
git add .
git commit -m "Update application form"
git push origin main
```

### Manual Deployment

You can also trigger deployment manually:

1. Go to Actions tab in GitHub
2. Select "Deploy to MS AI Server"
3. Click "Run workflow"
4. Choose environment (production/staging)

### Local Deployment

Use the deployment script for local testing:

```bash
./deploy.sh
```

## 📁 File Structure

The deployment syncs these files to the server:

```
/var/www/msai/
├── index.html              # Main application form
├── msai_with_application.html  # Full site with application
├── .github/workflows/      # GitHub Actions (excluded)
├── test_*.py              # Test files (excluded)
└── ...                    # Other project files
```

## 🔧 Server Setup

### Nginx Configuration

Ensure your Nginx is configured to serve from `/var/www/msai`:

```nginx
server {
    listen 80;
    server_name msai.syzygyx.com;
    
    root /var/www/msai;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
    
    location /apply {
        try_files /index.html =404;
    }
}
```

### Permissions

The deployment script sets proper permissions:
- Files: `755` (readable/executable)
- Owner: `www-data:www-data`

## 🏥 Health Checks

The deployment includes automatic health checks:

1. **Server Response**: Verifies the site responds with HTTP 200
2. **Retry Logic**: Attempts up to 5 times with 10-second delays
3. **Status Check**: Monitors Nginx service status

## 🔄 Rollback

If deployment fails, you can rollback:

```bash
# SSH into server
ssh ubuntu@3.84.224.16

# List available backups
ls -la /var/backups/msai/

# Restore from backup
sudo cp -r /var/backups/msai/backup-YYYYMMDD-HHMMSS/* /var/www/msai/
sudo systemctl reload nginx
```

## 📊 Monitoring

### Deployment Status

Check deployment status in:
- GitHub Actions tab
- Server logs: `/var/log/nginx/error.log`
- Application logs: `/var/log/nginx/access.log`

### Health Monitoring

Monitor site health:
```bash
curl -I http://msai.syzygyx.com
curl -I http://msai.syzygyx.com/apply
```

## 🛠️ Troubleshooting

### Common Issues

1. **SSH Connection Failed**
   - Verify SSH key is correct
   - Check server host and user
   - Ensure server allows SSH connections

2. **Permission Denied**
   - Check file permissions on server
   - Verify user has sudo access
   - Ensure web server user can read files

3. **Site Not Loading**
   - Check Nginx configuration
   - Verify domain DNS settings
   - Check server firewall rules

4. **Deployment Fails**
   - Check GitHub Actions logs
   - Verify all secrets are set
   - Test SSH connection manually

### Debug Commands

```bash
# Test SSH connection
ssh ubuntu@3.84.224.16 "echo 'Connection successful'"

# Check server status
ssh ubuntu@3.84.224.16 "sudo systemctl status nginx"

# Check file permissions
ssh ubuntu@3.84.224.16 "ls -la /var/www/msai/"

# Test site locally
curl -v http://msai.syzygyx.com
```

## 🎯 Next Steps

1. **Set up GitHub Secrets** (required)
2. **Test deployment** with a small change
3. **Monitor first deployment** for any issues
4. **Set up monitoring** for ongoing health checks
5. **Configure notifications** for deployment status

## 📞 Support

If you encounter issues:
1. Check the GitHub Actions logs
2. Review server logs
3. Test SSH connection manually
4. Verify all secrets are configured correctly

---

**Ready to deploy?** Just push to the `main` branch and watch the magic happen! 🚀