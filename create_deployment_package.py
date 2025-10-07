#!/usr/bin/env python3
"""
Create deployment package for manual upload
"""

import os
import tarfile
import shutil

def main():
    print("📦 Creating deployment package for manual upload...")
    
    # Create deployment directory
    deploy_dir = "manual_deployment"
    if os.path.exists(deploy_dir):
        shutil.rmtree(deploy_dir)
    os.makedirs(deploy_dir)
    
    # Copy our files
    print("📋 Copying files...")
    shutil.copy2("app_updated.py", os.path.join(deploy_dir, "app.py"))
    shutil.copy2("index.html", deploy_dir)
    shutil.copy2("msai_application_form.html", deploy_dir)
    
    # Create requirements.txt
    requirements = """fastapi==0.104.1
uvicorn[standard]==0.24.0
"""
    with open(os.path.join(deploy_dir, "requirements.txt"), "w") as f:
        f.write(requirements)
    
    # Create deployment instructions
    instructions = """# Manual Deployment Instructions

## Files included:
- app.py (updated FastAPI app with embedded HTML content)
- index.html (main page)
- msai_application_form.html (application form)
- requirements.txt (Python dependencies)

## Deployment steps:
1. Upload all files to /opt/msai/ on the server
2. Install dependencies: pip install -r requirements.txt
3. Restart the service: sudo systemctl restart msai
4. Reload nginx: sudo systemctl reload nginx

## Verification:
- Main page: http://msai.syzygyx.com/
- Application form: http://msai.syzygyx.com/application
- Health check: http://msai.syzygyx.com/health

## Service management:
- Check status: sudo systemctl status msai
- View logs: sudo journalctl -u msai -f
- Restart: sudo systemctl restart msai
"""
    
    with open(os.path.join(deploy_dir, "DEPLOYMENT_INSTRUCTIONS.md"), "w") as f:
        f.write(instructions)
    
    # Create tar.gz package
    print("📦 Creating tar.gz package...")
    with tarfile.open("msai_deployment_package.tar.gz", "w:gz") as tar:
        tar.add(deploy_dir, arcname=".")
    
    print("✅ Deployment package created!")
    print(f"📁 Package: msai_deployment_package.tar.gz")
    print(f"📁 Contents: {deploy_dir}/")
    print("")
    print("🚀 To deploy manually:")
    print("   1. Upload msai_deployment_package.tar.gz to the server")
    print("   2. Extract: tar -xzf msai_deployment_package.tar.gz")
    print("   3. Follow instructions in DEPLOYMENT_INSTRUCTIONS.md")
    print("")
    print("🌐 Expected results after deployment:")
    print("   - Main page with comprehensive program information")
    print("   - Professional application form")
    print("   - White paper section")
    print("   - Faculty profiles and research opportunities")

if __name__ == "__main__":
    main()