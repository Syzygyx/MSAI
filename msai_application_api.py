#!/usr/bin/env python3
"""
MSAI Application API - Backend for handling application form submissions
Integrates with Google Sheets and Google Drive
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
import json
import os
from datetime import datetime
import uuid
from pathlib import Path

# Import our Google Sheets integration
from google_sheets_integration import MSAIApplicationSheets

# Create FastAPI app
app = FastAPI(
    title="MSAI Application API",
    description="API for handling MSAI application form submissions",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Google Sheets integration
sheets_integration = MSAIApplicationSheets()

# Pydantic models for form validation
class ApplicationData(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    phone: str
    dateOfBirth: str
    gender: Optional[str] = None
    address: str
    undergraduateDegree: str
    undergraduateGPA: float
    undergraduateInstitution: str
    graduationYear: int
    graduateDegree: Optional[str] = None
    greScore: Optional[int] = None
    toeflScore: Optional[int] = None
    specialization: str
    startTerm: str
    programFormat: str
    interests: List[str] = []
    statementOfPurpose: str
    personalStatement: str
    diversityStatement: str
    researchExperience: str
    careerGoals: str
    additionalInfo: Optional[str] = None
    currentEmployer: Optional[str] = None
    currentPosition: Optional[str] = None
    workExperience: Optional[str] = None
    relevantExperience: Optional[str] = None
    # Reference 1
    reference1Name: str
    reference1Title: str
    reference1Email: EmailStr
    reference1Phone: Optional[str] = None
    reference1Institution: str
    reference1Relationship: str
    reference1YearsKnown: str
    # Reference 2
    reference2Name: str
    reference2Title: str
    reference2Email: EmailStr
    reference2Phone: Optional[str] = None
    reference2Institution: str
    reference2Relationship: str
    reference2YearsKnown: str
    # Reference 3
    reference3Name: str
    reference3Title: str
    reference3Email: EmailStr
    reference3Phone: Optional[str] = None
    reference3Institution: str
    reference3Relationship: str
    reference3YearsKnown: str
    howDidYouHear: Optional[str] = None
    additionalComments: Optional[str] = None
    agreeTerms: bool
    agreeMarketing: bool = False

class ApplicationResponse(BaseModel):
    success: bool
    message: str
    application_id: Optional[str] = None
    timestamp: str

class ApplicationStats(BaseModel):
    total_applications: int
    by_specialization: Dict[str, int]
    by_status: Dict[str, int]
    by_term: Dict[str, int]
    by_format: Dict[str, int]

# Initialize Google Sheets on startup
@app.on_event("startup")
async def startup_event():
    """Initialize Google Sheets integration on startup"""
    print("🚀 Starting MSAI Application API...")
    
    if sheets_integration.authenticate():
        print("✅ Google Sheets authentication successful")
        
        # Try to find existing spreadsheet or create new one
        try:
            # This would need to be configured with your actual spreadsheet ID
            # For now, we'll create a new one
            spreadsheet = sheets_integration.create_spreadsheet("MSAI Applications 2024")
            if spreadsheet:
                sheets_integration.setup_worksheet("Applications")
                print("✅ Google Sheets setup complete")
        except Exception as e:
            print(f"⚠️  Google Sheets setup issue: {e}")
    else:
        print("❌ Google Sheets authentication failed")

@app.get("/", response_class=HTMLResponse)
async def get_application_form():
    """Serve the application form"""
    try:
        with open("msai_application_form.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Application form not found</h1>", status_code=404)

@app.post("/api/application", response_model=ApplicationResponse)
async def submit_application(application: ApplicationData):
    """Submit a new application"""
    try:
        # Convert Pydantic model to dict
        form_data = application.dict()
        
        # Generate application ID
        application_id = str(uuid.uuid4())
        form_data['application_id'] = application_id
        
        # Submit to Google Sheets
        success = sheets_integration.submit_application(form_data)
        
        if success:
            # TODO: Send confirmation email
            # TODO: Upload files to Google Drive
            # TODO: Send notification to admissions staff
            
            return ApplicationResponse(
                success=True,
                message="Application submitted successfully",
                application_id=application_id,
                timestamp=datetime.now().isoformat()
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to submit application")
            
    except Exception as e:
        print(f"❌ Error submitting application: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/application/upload")
async def upload_documents(
    application_id: str = Form(...),
    transcript: UploadFile = File(...),
    resume: UploadFile = File(...),
    additional_docs: List[UploadFile] = File([])
):
    """Upload application documents"""
    try:
        # Create upload directory for this application
        upload_dir = Path(f"uploads/{application_id}")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        uploaded_files = {}
        
        # Save transcript
        if transcript:
            transcript_path = upload_dir / f"transcript_{transcript.filename}"
            with open(transcript_path, "wb") as f:
                content = await transcript.read()
                f.write(content)
            uploaded_files['transcript'] = str(transcript_path)
        
        # Save resume
        if resume:
            resume_path = upload_dir / f"resume_{resume.filename}"
            with open(resume_path, "wb") as f:
                content = await resume.read()
                f.write(content)
            uploaded_files['resume'] = str(resume_path)
        
        # Save additional documents
        additional_paths = []
        for i, doc in enumerate(additional_docs):
            doc_path = upload_dir / f"additional_{i}_{doc.filename}"
            with open(doc_path, "wb") as f:
                content = await doc.read()
                f.write(content)
            additional_paths.append(str(doc_path))
        
        uploaded_files['additional_docs'] = additional_paths
        
        # TODO: Upload to Google Drive
        # TODO: Update application record with file paths
        
        return {
            "success": True,
            "message": "Documents uploaded successfully",
            "files": uploaded_files
        }
        
    except Exception as e:
        print(f"❌ Error uploading documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/applications", response_model=List[Dict[str, Any]])
async def get_applications(status: Optional[str] = None):
    """Get all applications or filter by status"""
    try:
        applications = sheets_integration.get_applications(status)
        return applications
    except Exception as e:
        print(f"❌ Error retrieving applications: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/applications/stats", response_model=ApplicationStats)
async def get_application_stats():
    """Get application statistics"""
    try:
        stats = sheets_integration.get_application_stats()
        return ApplicationStats(**stats)
    except Exception as e:
        print(f"❌ Error getting application stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/applications/{email}/status")
async def update_application_status(
    email: str,
    status: str,
    notes: Optional[str] = None
):
    """Update application status"""
    try:
        success = sheets_integration.update_application_status(email, status, notes or "")
        
        if success:
            return {"success": True, "message": f"Application status updated to {status}"}
        else:
            raise HTTPException(status_code=404, detail="Application not found")
            
    except Exception as e:
        print(f"❌ Error updating application status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/applications/export")
async def export_applications():
    """Export applications to CSV"""
    try:
        csv_file = sheets_integration.export_to_csv()
        
        if csv_file:
            return {
                "success": True,
                "message": "Applications exported successfully",
                "filename": csv_file
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to export applications")
            
    except Exception as e:
        print(f"❌ Error exporting applications: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "MSAI Application API",
        "version": "1.0.0"
    }

@app.get("/api/specializations")
async def get_specializations():
    """Get available specializations"""
    return {
        "specializations": [
            "Machine Learning & Data Science",
            "Natural Language Processing",
            "Computer Vision & Robotics",
            "General AI"
        ]
    }

@app.get("/api/start-terms")
async def get_start_terms():
    """Get available start terms"""
    return {
        "terms": [
            "Fall 2024",
            "Spring 2025",
            "Fall 2025",
            "Spring 2026"
        ]
    }

@app.get("/api/program-formats")
async def get_program_formats():
    """Get available program formats"""
    return {
        "formats": [
            "Full-time",
            "Part-time",
            "Online",
            "Hybrid"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)