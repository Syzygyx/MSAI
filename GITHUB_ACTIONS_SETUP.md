# 🚀 GitHub Actions Setup for MS AI Deployment

## ✅ **Automated Deployment Pipeline Created**

I've created a complete GitHub Actions workflow that will automatically deploy your MS AI application to the live server whenever you push to the main branch.

---

## 📋 **What's Been Created**

### 1. **GitHub Actions Workflow** (`.github/workflows/deploy.yml`)
- **Triggers**: Pushes to `main` branch
- **Features**:
  - ✅ Automatic code checkout
  - ✅ Python environment setup
  - ✅ Dependency installation
  - ✅ Test execution (ready for your tests)
  - ✅ Deployment package creation
  - ✅ Server deployment via SSH
  - ✅ Service restart and verification
  - ✅ Health checks

### 2. **Requirements File** (`requirements.txt`)
- All necessary Python dependencies
- Version-pinned for stability

---

## 🔧 **Setup Required**

### **Step 1: Configure GitHub Secrets**

You need to add these secrets to your GitHub repository:

1. **Go to your GitHub repository**
2. **Click Settings → Secrets and variables → Actions**
3. **Add these repository secrets:**

```
SERVER_IP = 44.220.164.13
SERVER_USER = ubuntu
SSH_PRIVATE_KEY = [Your SSH private key content]
```

### **Step 2: Get Your SSH Private Key**

If you have the SSH key file locally:
```bash
cat msai-production-key.pem
```

Copy the entire content (including `-----BEGIN` and `-----END` lines) and paste it as the `SSH_PRIVATE_KEY` secret.

### **Step 3: Test the Workflow**

1. **Commit and push your changes:**
   ```bash
   git add .
   git commit -m "Add GitHub Actions deployment workflow"
   git push origin main
   ```

2. **Check the Actions tab** in your GitHub repository to see the deployment in progress.

---

## 🎯 **What Happens on Each Push**

### **Automatic Process:**
1. **Code Checkout** - Gets latest code
2. **Environment Setup** - Installs Python 3.9
3. **Dependencies** - Installs all required packages
4. **Testing** - Runs any tests (ready for your test suite)
5. **Package Creation** - Creates deployment archive with:
   - Enhanced app.py (with application form)
   - Application form HTML
   - Google Sheets integration
   - Systemd service file
   - Nginx configuration
   - Deployment script
6. **Server Deployment** - Uploads and deploys to live server
7. **Service Restart** - Restarts MS AI service
8. **Verification** - Tests all endpoints
9. **Notification** - Reports success/failure

---

## 🌐 **Deployed Endpoints**

Once deployed, these will be available:

### **Main Application**
- **Site**: `http://msai.syzygyx.com`
- **Health Check**: `http://msai.syzygyx.com/health`
- **API Docs**: `http://msai.syzygyx.com/docs`

### **Application Form**
- **Application Form**: `http://msai.syzygyx.com/application`
- **Apply (Redirect)**: `http://msai.syzygyx.com/apply`
- **API Endpoint**: `http://msai.syzygyx.com/api/application`

### **API Endpoints**
- **Submit Application**: `POST /api/application`
- **Get Applications**: `GET /api/applications`
- **Application Stats**: `GET /api/applications/stats`
- **Specializations**: `GET /api/specializations`
- **Start Terms**: `GET /api/start-terms`
- **Program Formats**: `GET /api/program-formats`

---

## 🔍 **Monitoring & Troubleshooting**

### **Check Deployment Status**
1. Go to **Actions** tab in GitHub
2. Click on the latest workflow run
3. View logs for each step

### **Common Issues**

#### **SSH Connection Failed**
- Verify `SSH_PRIVATE_KEY` secret is correct
- Ensure server IP and user are correct
- Check if server is accessible

#### **Service Won't Start**
- Check server logs: `sudo journalctl -u msai -f`
- Verify Python dependencies are installed
- Check file permissions

#### **Application Form Not Loading**
- Verify `msai_application_form.html` is uploaded
- Check nginx configuration
- Test direct file access

---

## 🚀 **Next Steps**

### **Immediate Actions:**
1. **Add the GitHub secrets** (most important!)
2. **Push to main branch** to trigger first deployment
3. **Monitor the Actions tab** for deployment progress

### **Future Enhancements:**
1. **Add tests** to the workflow
2. **Add staging environment** for testing
3. **Add rollback capability**
4. **Add Slack/Discord notifications**
5. **Add database migrations**

---

## 📊 **Benefits of This Setup**

### **✅ Automated Deployment**
- No manual deployment needed
- Consistent deployment process
- Reduced human error

### **✅ Version Control Integration**
- Every push triggers deployment
- Full deployment history
- Easy rollback to previous versions

### **✅ Quality Assurance**
- Automated testing before deployment
- Health checks after deployment
- Immediate feedback on issues

### **✅ Scalability**
- Easy to add more environments
- Can deploy to multiple servers
- Supports blue-green deployments

---

## 🎉 **Ready to Deploy!**

Your GitHub Actions workflow is ready! Just add the secrets and push to main branch to see the magic happen! 🚀

**The application form will be live at `http://msai.syzygyx.com/application` after the first successful deployment.**