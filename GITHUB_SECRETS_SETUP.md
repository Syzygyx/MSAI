# 🔐 GitHub Secrets Setup for Automated Deployment

## 🎯 **Goal**
Configure GitHub secrets so the GitHub Actions workflow can automatically deploy the application form to your server.

## 📋 **Required Secrets**

You need to add these 3 secrets to your GitHub repository:

### 1. **SERVER_IP**
- **Value**: `3.84.224.16`
- **Description**: The IP address of your MS AI server

### 2. **SERVER_USER**
- **Value**: `ubuntu`
- **Description**: The username for SSH access to the server

### 3. **SSH_PRIVATE_KEY**
- **Value**: Your SSH private key content
- **Description**: The private key for SSH access to the server

## 🚀 **Step-by-Step Setup**

### **Step 1: Go to GitHub Secrets**
1. Open your browser and go to: `https://github.com/dcmcshan/MSAI`
2. Click on **"Settings"** tab
3. In the left sidebar, click **"Secrets and variables"**
4. Click **"Actions"**

### **Step 2: Add SERVER_IP Secret**
1. Click **"New repository secret"**
2. **Name**: `SERVER_IP`
3. **Secret**: `3.84.224.16`
4. Click **"Add secret"**

### **Step 3: Add SERVER_USER Secret**
1. Click **"New repository secret"**
2. **Name**: `SERVER_USER`
3. **Secret**: `ubuntu`
4. Click **"Add secret"**

### **Step 4: Add SSH_PRIVATE_KEY Secret**
1. Click **"New repository secret"**
2. **Name**: `SSH_PRIVATE_KEY`
3. **Secret**: Copy the content of your SSH private key file
4. Click **"Add secret"**

## 🔑 **Finding Your SSH Private Key**

### **Option A: Use Existing Key**
If you have the key file locally:
```bash
cat msai-production-key.pem
```
Copy the entire output (including `-----BEGIN` and `-----END` lines)

### **Option B: Generate New Key**
If you need to generate a new key:
```bash
ssh-keygen -t rsa -b 4096 -f msai-github-key
```
Then copy the content of `msai-github-key`

## ✅ **Verification**

After adding all 3 secrets, you should see:
- ✅ `SERVER_IP` in the secrets list
- ✅ `SERVER_USER` in the secrets list  
- ✅ `SSH_PRIVATE_KEY` in the secrets list

## 🚀 **Trigger Deployment**

Once secrets are configured:
1. Go to **"Actions"** tab in your repository
2. You should see the **"Deploy to MS AI Server"** workflow
3. Click **"Run workflow"** to trigger deployment
4. Watch the deployment progress in real-time

## 🎯 **Expected Result**

After successful deployment:
- ✅ Application form will be live at: `http://msai.syzygyx.com/application`
- ✅ All API endpoints will be working
- ✅ No more "Not Found" errors
- ✅ Full application form functionality

## 🔧 **Troubleshooting**

### **If SSH Key Doesn't Work:**
1. Make sure the key has proper permissions: `chmod 600 keyfile.pem`
2. Verify the key matches the server's authorized_keys
3. Test SSH connection manually: `ssh -i keyfile.pem ubuntu@3.84.224.16`

### **If Deployment Fails:**
1. Check the GitHub Actions logs for specific errors
2. Verify all secrets are correctly set
3. Ensure the server is accessible

## 📞 **Need Help?**

If you encounter any issues:
1. Check the GitHub Actions logs
2. Verify server connectivity
3. Ensure all secrets are properly configured

---

**Once configured, your application form will be automatically deployed and live!** 🚀