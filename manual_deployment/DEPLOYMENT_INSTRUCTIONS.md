# Manual Deployment Instructions

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
