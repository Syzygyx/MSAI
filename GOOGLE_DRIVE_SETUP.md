# Google Drive Setup for MSAI Curriculum System

## ✅ Completed Steps

### 1. Google Cloud Authentication
- ✅ Authenticated with dan@syzygyx.com
- ✅ Set project to syzygyx-161202
- ✅ Enabled Google Drive API
- ✅ Created service account: msai-service-account@syzygyx-161202.iam.gserviceaccount.com
- ✅ Generated service account key: msai-service-account-key.json

### 2. Service Account Configuration
- ✅ Service account email: msai-service-account@syzygyx-161202.iam.gserviceaccount.com
- ✅ Service account key file: msai-service-account-key.json
- ✅ Project ID: syzygyx-161202

## 🔧 Manual Setup Required

Due to Google Drive API scope limitations, you'll need to complete the Shared Drive setup manually:

### Step 1: Create Shared Drive
1. Go to [Google Drive](https://drive.google.com)
2. Click "New" → "Shared drive"
3. Name it: "MSAI Curriculum System"
4. Description: "Shared Drive for MSAI Curriculum System - AI-powered education platform"
5. Click "Create"

### Step 2: Add Service Account
1. In the Shared Drive, click the settings gear
2. Click "Manage members"
3. Click "Add members"
4. Add: msai-service-account@syzygyx-161202.iam.gserviceaccount.com
5. Set role to "Manager"
6. Click "Send"

### Step 3: Create Folder Structure
Create these folders in the Shared Drive:
- **Curriculum Materials** - Course materials, syllabi, and educational content
- **Student Projects** - Student assignments, projects, and portfolios
- **AI Generated Content** - AI-generated curriculum, assessments, and learning materials
- **Research and Development** - Research papers, experiments, and development materials
- **Administrative** - Administrative documents, reports, and system configurations

### Step 4: Get Shared Drive ID
1. Open the Shared Drive
2. Copy the ID from the URL: `https://drive.google.com/drive/folders/[SHARED_DRIVE_ID]`
3. Update the configuration file with the ID

## 📄 Configuration File

Once you have the Shared Drive ID, update `msai_drive_config.json`:

```json
{
  "shared_drive_id": "[YOUR_SHARED_DRIVE_ID]",
  "shared_drive_name": "MSAI Curriculum System",
  "service_account_email": "msai-service-account@syzygyx-161202.iam.gserviceaccount.com",
  "service_account_file": "msai-service-account-key.json",
  "folders": {
    "Curriculum Materials": "[FOLDER_ID_1]",
    "Student Projects": "[FOLDER_ID_2]",
    "AI Generated Content": "[FOLDER_ID_3]",
    "Research and Development": "[FOLDER_ID_4]",
    "Administrative": "[FOLDER_ID_5]"
  },
  "drive_url": "https://drive.google.com/drive/folders/[SHARED_DRIVE_ID]"
}
```

## 🧪 Test Setup

Once configured, test the setup:

```bash
python3 test_drive_access.py
```

## 🔑 Service Account Permissions

The service account has been configured with:
- ✅ Google Drive API access
- ✅ Project-level permissions
- ✅ Service account key generated

## 📁 Files Created

- `msai-service-account-key.json` - Service account credentials
- `msai_drive_config.json` - Drive configuration (to be updated)
- `setup_google_drive.py` - Python setup script
- `simple_drive_setup.py` - CLI-based setup script

## 🚀 Next Steps

1. Complete the manual Shared Drive setup
2. Update the configuration file with the Shared Drive ID
3. Test the Google Drive integration
4. Integrate with the MSAI Curriculum System

## 📞 Support

If you encounter issues:
1. Check that the service account has access to the Shared Drive
2. Verify the Shared Drive ID is correct
3. Ensure the Google Drive API is enabled
4. Check the service account permissions