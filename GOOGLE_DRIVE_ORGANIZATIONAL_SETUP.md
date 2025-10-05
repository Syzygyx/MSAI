# MSAI Google Drive Organizational Setup

## 🎯 **Organizational Structure**

The MSAI Google Drive is organized into five main categories:

### 📝 **Applicants**
- **Application Materials** - Application forms and documents
- **Admission Essays** - Personal statements and essays
- **Recommendation Letters** - Letters of recommendation
- **Transcripts** - Academic transcripts and records
- **Test Scores** - GRE, GMAT, and other test scores
- **Interview Records** - Interview notes and recordings
- **Admission Decisions** - Decision letters and notifications
- **Waitlist** - Waitlisted applicants
- **Rejected Applications** - Declined applications
- **Recruitment Materials** - Marketing and recruitment content
- **Scholarship Applications** - Financial aid applications
- **International Applicants** - International student materials

### 📚 **Students**
- **Current Students** - Active student records and materials
- **Graduated Students** - Alumni records and portfolios
- **Student Projects** - Individual and group projects
- **Student Portfolios** - Student work collections
- **Student Records** - Academic and personal records
- **Assignments** - Course assignments and submissions
- **Grades** - Grade records and transcripts

### 👨‍🏫 **Faculty**
- **Faculty Profiles** - Faculty information and bios
- **Research Papers** - Faculty research publications
- **Teaching Materials** - Course preparation materials
- **Course Development** - New course creation materials
- **Faculty Meetings** - Meeting notes and minutes
- **Professional Development** - Training and development materials
- **Publications** - Faculty publications and articles

### 👥 **Staff**
- **Administrative Documents** - General administrative files
- **HR Records** - Human resources documentation
- **Budget and Finance** - Financial planning and budgets
- **IT Resources** - Technology and system documentation
- **Facilities** - Building and equipment management
- **Policies and Procedures** - Institutional policies
- **Staff Training** - Training materials and records

### 📖 **Courses**
- **Course Syllabi** - Course outlines and descriptions
- **Lecture Materials** - Presentation slides and notes
- **Assignments** - Course assignments and rubrics
- **Exams and Quizzes** - Assessment materials
- **Course Resources** - Additional learning resources
- **AI Generated Content** - AI-created curriculum materials
- **Course Evaluations** - Student feedback and assessments

## 🔧 **Additional Folders**

### 📁 **Administrative**
General administrative documents and system configurations

### 🔬 **Research and Development**
Research papers, experiments, and development materials

### 🤖 **AI Generated Content**
AI-generated curriculum, assessments, and learning materials

### 📋 **Templates**
Document templates and forms for consistent formatting

### 🗄️ **Archives**
Archived documents and historical records

## 🚀 **Setup Instructions**

### Automated Setup
```bash
python3 setup_msai_drive_structure.py
```

### Manual Setup
1. Create Shared Drive: "MSAI Curriculum System"
2. Add service account: `msai-service-account@syzygyx-161202.iam.gserviceaccount.com`
3. Create the organizational folder structure as described above

## 📊 **Folder Permissions**

### Applicants Folder
- **Admissions Staff**: Full access to all applicant materials
- **Faculty Reviewers**: Access to assigned applications
- **Staff**: Administrative access to application processing
- **Students**: No access (confidential)
- **Faculty**: Limited access to recruitment materials only

### Students Folder
- **Students**: View and edit their own subfolder
- **Faculty**: Full access to all student materials
- **Staff**: Administrative access to student records

### Faculty Folder
- **Faculty**: Full access to their own materials
- **Staff**: Administrative access to faculty information
- **Students**: Limited access to public faculty materials

### Staff Folder
- **Staff**: Full access to administrative materials
- **Faculty**: Limited access to relevant staff materials
- **Students**: No access (confidential)

### Courses Folder
- **Faculty**: Full access to course materials
- **Students**: Access to their enrolled courses
- **Staff**: Administrative access to all courses

## 🔐 **Security Considerations**

1. **Confidential Information**: Staff and HR records are restricted
2. **Student Privacy**: Student records follow FERPA guidelines
3. **Applicant Privacy**: Applicant materials are highly confidential
4. **Research Data**: Research materials may have additional restrictions
5. **Access Control**: Regular review of folder permissions
6. **Admission Data**: Applicant information requires special handling

## 📱 **Integration with MSAI System**

The folder structure integrates with the MSAI Curriculum System:

- **Course Management**: Automatic folder creation for new courses
- **Student Portfolios**: AI-generated portfolio suggestions
- **Faculty Collaboration**: Shared research and teaching materials
- **Administrative Workflow**: Automated document routing

## 🧪 **Testing**

Test the setup with:
```bash
python3 test_drive_access.py
```

## 📞 **Support**

For issues with the Google Drive setup:
1. Check service account permissions
2. Verify Shared Drive access
3. Review folder structure
4. Contact system administrator