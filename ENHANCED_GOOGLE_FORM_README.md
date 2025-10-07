# Enhanced Google Form Creator for MS AI Application

A comprehensive, production-ready solution for creating Google Forms programmatically with advanced features including validation, analytics, and MCP integration.

## 🚀 Features

### Core Functionality
- **Multiple Authentication Methods**: OAuth 2.0 and Service Account
- **Comprehensive Form Creation**: Complete MS AI application form with 60+ questions
- **Configuration Management**: JSON-based configuration system
- **Error Handling**: Robust error handling and logging
- **Batch Processing**: Efficient form creation with batch updates

### Advanced Features
- **Form Validation**: Real-time validation with detailed feedback
- **Analytics Engine**: Response analysis and insights generation
- **Visualization**: Automatic chart and graph generation
- **MCP Integration**: Google Docs MCP server setup and configuration
- **Sample Data**: Built-in sample data for testing and demos

## 📁 Project Structure

```
MSAI/
├── enhanced_google_form_creator.py    # Main form creator class
├── form_validator.py                  # Form validation engine
├── form_analytics.py                  # Analytics and insights
├── run_enhanced_creator.py            # Main runner script
├── form_config.json                   # Configuration file
├── requirements.txt                   # Python dependencies
├── setup_mcp_server.sh               # MCP server setup script
├── MCP_SETUP_GUIDE.md                # Detailed MCP setup guide
└── ENHANCED_GOOGLE_FORM_README.md    # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Node.js 18+ (for MCP server)
- Google Cloud Project with APIs enabled

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Google Cloud Credentials

#### Option A: Service Account (Recommended)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable required APIs:
   - Google Forms API
   - Google Drive API
   - Google Sheets API
   - Google Docs API
4. Create a service account:
   - Go to IAM & Admin > Service Accounts
   - Click "Create Service Account"
   - Name: `msai-form-creator`
   - Grant roles: Editor, Google Forms API User, Google Drive API User
5. Generate and download JSON key
6. Save as `msai-service-key.json` in project root

#### Option B: OAuth 2.0
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create OAuth 2.0 credentials
3. Download JSON file
4. Save as `credentials.json` in project root

### 3. Set Up MCP Server (Optional)
```bash
# Run the automated setup script
./setup_mcp_server.sh

# Or follow the manual guide
# See MCP_SETUP_GUIDE.md for detailed instructions
```

## 🚀 Quick Start

### Run the Enhanced Creator
```bash
python run_enhanced_creator.py
```

### Available Options
1. **Create Google Form** - Create a new MS AI application form
2. **Run Validation Demo** - Test form validation with sample data
3. **Run Analytics Demo** - Analyze responses and generate insights
4. **Run All** - Complete demo with form creation, validation, and analytics
5. **Setup MCP Server** - Configure Google Docs MCP integration
6. **Exit** - Quit the application

## 📝 Usage Examples

### Basic Form Creation
```python
from enhanced_google_form_creator import GoogleFormCreator

# Initialize creator
creator = GoogleFormCreator()

# Authenticate (service account)
creator.authenticate_service_account("msai-service-key.json")

# Create form
form_data = creator.create_form()
print(f"Form URL: {form_data['responderUri']}")
```

### Form Validation
```python
from form_validator import FormValidator

# Initialize validator
validator = FormValidator()

# Validate response
result = validator.validate_response(response_data)
print(f"Valid: {result.is_valid}")
print(f"Score: {result.score}/100")
```

### Analytics
```python
from form_analytics import FormAnalytics

# Initialize analytics
analytics = FormAnalytics("form_responses.json")

# Get insights
insights = analytics.generate_insights()
for insight in insights:
    print(f"- {insight}")

# Create visualizations
analytics.create_visualizations()
```

## ⚙️ Configuration

### Form Configuration (`form_config.json`)
```json
{
  "title": "MS AI Program Application - AURNOVA University",
  "description": "Thank you for your interest...",
  "collect_emails": true,
  "limit_responses": true,
  "show_progress": true,
  "confirmation_message": "Thank you for your application...",
  "theme_color": "#1976D2",
  "validation_rules": {
    "email": {
      "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
      "message": "Please enter a valid email address"
    },
    "gpa": {
      "min": 0.0,
      "max": 4.0,
      "message": "GPA must be between 0.0 and 4.0"
    }
  }
}
```

### Environment Variables
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
export MCP_LOG_LEVEL="info"
export MCP_PORT="3001"
```

## 🔧 MCP Integration

The MCP (Model Context Protocol) server enables Google Docs integration in Cursor:

### Features
- Create and edit Google Docs
- Read document content
- Update document formatting
- Manage document permissions

### Setup
1. Run the setup script: `./setup_mcp_server.sh`
2. Restart Cursor
3. Test integration by asking Cursor to create a Google Doc

### Usage in Cursor
Once configured, you can use natural language commands:
- "Create a new Google Doc titled 'Project Proposal'"
- "Read the content of document ID: 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
- "Add a new paragraph to the document about project timeline"

## 📊 Analytics Features

### Response Analysis
- **Completion Rates**: Track field completion percentages
- **GPA Distribution**: Analyze academic qualifications
- **Demographics**: Gender, employment status, etc.
- **Essay Analysis**: Word count and content analysis
- **Test Scores**: Standardized test score distributions

### Visualizations
- GPA distribution histograms
- Gender distribution charts
- Employment status pie charts
- Completion rate heatmaps
- Time series analysis

### Insights Generation
- Automatic insight generation based on data patterns
- Recommendations for form improvements
- Applicant quality assessment
- Diversity and inclusion metrics

## 🧪 Testing

### Run Tests
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# Run with coverage
pytest --cov=enhanced_google_form_creator tests/
```

### Sample Data
The system includes comprehensive sample data for testing:
- 2 complete application responses
- Various GPA and test score ranges
- Different demographic profiles
- Complete essay responses

## 📈 Monitoring and Logging

### Log Files
- `google_form_creator.log` - Main application logs
- `mcp-server.log` - MCP server logs (if enabled)

### Log Levels
- `DEBUG` - Detailed debugging information
- `INFO` - General information messages
- `WARNING` - Warning messages
- `ERROR` - Error messages
- `CRITICAL` - Critical error messages

### Monitoring
- Form creation success rates
- Authentication status
- API usage and quotas
- Error tracking and alerting

## 🔒 Security

### Best Practices
- Store credentials securely
- Use environment variables for sensitive data
- Regularly rotate service account keys
- Monitor API usage and quotas
- Implement rate limiting

### Permissions
- Minimum required permissions for service accounts
- Principle of least privilege
- Regular permission audits

## 🚀 Deployment

### Local Development
```bash
# Clone repository
git clone <repository-url>
cd MSAI

# Install dependencies
pip install -r requirements.txt

# Set up credentials
# (Follow credential setup instructions above)

# Run application
python run_enhanced_creator.py
```

### Production Deployment
1. Set up production Google Cloud project
2. Configure service accounts with appropriate permissions
3. Set up monitoring and logging
4. Configure backup and recovery
5. Set up CI/CD pipeline

## 🤝 Contributing

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install

# Run code formatting
black .

# Run linting
flake8 .

# Run type checking
mypy .
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Write comprehensive docstrings
- Include unit tests
- Update documentation

## 📚 Documentation

### Additional Resources
- [Google Forms API Documentation](https://developers.google.com/forms/api)
- [Google Drive API Documentation](https://developers.google.com/drive/api)
- [MCP Protocol Documentation](https://modelcontextprotocol.io/)
- [Cursor IDE Documentation](https://cursor.sh/docs)

### Troubleshooting
- Check logs for error messages
- Verify API credentials and permissions
- Ensure all dependencies are installed
- Check Google Cloud Console for API quotas

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Getting Help
1. Check the troubleshooting section
2. Review the logs for error messages
3. Check Google Cloud Console for API issues
4. Create an issue in the repository

### Common Issues
- **Authentication Errors**: Check credentials file and permissions
- **API Quotas**: Check Google Cloud Console for quota limits
- **MCP Server Issues**: Verify Node.js installation and configuration
- **Form Creation Failures**: Check form structure and validation rules

## 🎯 Roadmap

### Planned Features
- [ ] Multi-language support
- [ ] Advanced form templates
- [ ] Real-time collaboration
- [ ] Mobile app integration
- [ ] Advanced analytics dashboard
- [ ] Automated email notifications
- [ ] Integration with CRM systems

### Version History
- **v1.0.0** - Initial release with basic form creation
- **v1.1.0** - Added validation and analytics
- **v1.2.0** - Added MCP integration
- **v1.3.0** - Enhanced configuration and monitoring

---

**Happy Form Creating! 🎉**

For questions or support, please refer to the documentation or create an issue in the repository.