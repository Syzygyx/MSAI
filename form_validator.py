#!/usr/bin/env python3
"""
Google Form Validator
Validates form responses and provides detailed feedback
"""

import re
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, date

@dataclass
class ValidationResult:
    """Result of form validation"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    score: float  # 0-100

class FormValidator:
    """Comprehensive form validator for MS AI applications"""
    
    def __init__(self, config_file: str = "form_config.json"):
        self.config = self._load_config(config_file)
        self.validation_rules = self.config.get("validation_rules", {})
        self.essay_requirements = self.config.get("essay_requirements", {})
    
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load validation configuration"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Config file {config_file} not found. Using default validation rules.")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error loading config file: {e}")
            return {}
    
    def validate_response(self, response_data: Dict[str, Any]) -> ValidationResult:
        """Validate a complete form response"""
        errors = []
        warnings = []
        score = 100.0
        
        # Validate required fields
        required_fields = self._get_required_fields()
        for field in required_fields:
            if field not in response_data or not response_data[field]:
                errors.append(f"Required field '{field}' is missing")
                score -= 10
        
        # Validate email format
        if "Email Address" in response_data:
            email_result = self._validate_email(response_data["Email Address"])
            if not email_result["valid"]:
                errors.append(f"Email validation failed: {email_result['message']}")
                score -= 5
        
        # Validate phone number
        if "Phone Number" in response_data:
            phone_result = self._validate_phone(response_data["Phone Number"])
            if not phone_result["valid"]:
                errors.append(f"Phone validation failed: {phone_result['message']}")
                score -= 3
        
        # Validate GPA
        if "GPA" in response_data:
            gpa_result = self._validate_gpa(response_data["GPA"])
            if not gpa_result["valid"]:
                errors.append(f"GPA validation failed: {gpa_result['message']}")
                score -= 5
            elif gpa_result.get("warning"):
                warnings.append(gpa_result["warning"])
                score -= 2
        
        # Validate graduation year
        if "Graduation Year" in response_data:
            year_result = self._validate_graduation_year(response_data["Graduation Year"])
            if not year_result["valid"]:
                errors.append(f"Graduation year validation failed: {year_result['message']}")
                score -= 3
        
        # Validate test scores
        test_scores = ["GRE Verbal Score", "GRE Quantitative Score", "GRE Writing Score", 
                      "TOEFL Total Score", "IELTS Overall Score"]
        for score_field in test_scores:
            if score_field in response_data and response_data[score_field]:
                score_result = self._validate_test_score(score_field, response_data[score_field])
                if not score_result["valid"]:
                    errors.append(f"{score_field} validation failed: {score_result['message']}")
                    score -= 2
        
        # Validate essays
        essay_fields = ["Statement of Purpose (750-1000 words)", "Personal Statement (500-750 words)",
                       "Research Interests and Potential Thesis Topics (300-500 words)",
                       "Career Goals and Professional Development (300-500 words)"]
        
        for essay_field in essay_fields:
            if essay_field in response_data and response_data[essay_field]:
                essay_result = self._validate_essay(essay_field, response_data[essay_field])
                if not essay_result["valid"]:
                    errors.append(f"{essay_field} validation failed: {essay_result['message']}")
                    score -= 8
                elif essay_result.get("warning"):
                    warnings.append(essay_result["warning"])
                    score -= 3
        
        # Validate diversity statement (optional)
        if "Diversity and Inclusion Statement (Optional, 200-400 words)" in response_data:
            diversity_result = self._validate_diversity_statement(response_data["Diversity and Inclusion Statement (Optional, 200-400 words)"])
            if not diversity_result["valid"]:
                warnings.append(f"Diversity statement validation: {diversity_result['message']}")
                score -= 1
        
        # Validate references
        ref_result = self._validate_references(response_data)
        if not ref_result["valid"]:
            errors.append(f"References validation failed: {ref_result['message']}")
            score -= 10
        
        # Check for completeness
        completeness_result = self._check_completeness(response_data)
        if completeness_result["score"] < 80:
            warnings.append(f"Form completeness: {completeness_result['message']}")
            score -= completeness_result["penalty"]
        
        # Ensure score doesn't go below 0
        score = max(0, score)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            score=score
        )
    
    def _get_required_fields(self) -> List[str]:
        """Get list of required fields"""
        return [
            "Full Name", "Email Address", "Phone Number", "Date of Birth", "Gender",
            "Mailing Address", "Undergraduate Degree", "Institution", "GPA", "Graduation Year",
            "Relevant Coursework", "Research Experience and Publications",
            "Prerequisite Coursework Completed", "Programming Languages Proficiency",
            "Technical Skills and Tools", "English Proficiency",
            "Statement of Purpose (750-1000 words)", "Personal Statement (500-750 words)",
            "Research Interests and Potential Thesis Topics (300-500 words)",
            "Career Goals and Professional Development (300-500 words)",
            "Current Employment Status", "Work Experience",
            "Reference 1 - Name", "Reference 1 - Title/Position", "Reference 1 - Institution/Organization",
            "Reference 1 - Email", "Reference 1 - Relationship",
            "Reference 2 - Name", "Reference 2 - Title/Position", "Reference 2 - Institution/Organization",
            "Reference 2 - Email", "Reference 2 - Relationship"
        ]
    
    def _validate_email(self, email: str) -> Dict[str, Any]:
        """Validate email address"""
        if not email:
            return {"valid": False, "message": "Email is required"}
        
        pattern = self.validation_rules.get("email", {}).get("pattern", r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        
        if re.match(pattern, email):
            return {"valid": True}
        else:
            return {"valid": False, "message": self.validation_rules.get("email", {}).get("message", "Invalid email format")}
    
    def _validate_phone(self, phone: str) -> Dict[str, Any]:
        """Validate phone number"""
        if not phone:
            return {"valid": False, "message": "Phone number is required"}
        
        pattern = self.validation_rules.get("phone", {}).get("pattern", r"^[\+]?[1-9][\d]{0,15}$")
        
        if re.match(pattern, phone):
            return {"valid": True}
        else:
            return {"valid": False, "message": self.validation_rules.get("phone", {}).get("message", "Invalid phone number format")}
    
    def _validate_gpa(self, gpa_str: str) -> Dict[str, Any]:
        """Validate GPA"""
        if not gpa_str:
            return {"valid": False, "message": "GPA is required"}
        
        try:
            gpa = float(gpa_str)
            min_gpa = self.validation_rules.get("gpa", {}).get("min", 0.0)
            max_gpa = self.validation_rules.get("gpa", {}).get("max", 4.0)
            
            if gpa < min_gpa or gpa > max_gpa:
                return {"valid": False, "message": self.validation_rules.get("gpa", {}).get("message", "GPA must be between 0.0 and 4.0")}
            
            # Add warning for low GPA
            if gpa < 2.5:
                return {"valid": True, "warning": f"GPA of {gpa} is below typical admission standards"}
            
            return {"valid": True}
            
        except ValueError:
            return {"valid": False, "message": "GPA must be a valid number"}
    
    def _validate_graduation_year(self, year_str: str) -> Dict[str, Any]:
        """Validate graduation year"""
        if not year_str:
            return {"valid": False, "message": "Graduation year is required"}
        
        try:
            year = int(year_str)
            min_year = self.validation_rules.get("graduation_year", {}).get("min", 1950)
            max_year = self.validation_rules.get("graduation_year", {}).get("max", 2030)
            
            if year < min_year or year > max_year:
                return {"valid": False, "message": self.validation_rules.get("graduation_year", {}).get("message", "Invalid graduation year")}
            
            # Add warning for very old graduation year
            current_year = datetime.now().year
            if year < current_year - 10:
                return {"valid": True, "warning": f"Graduation year {year} is quite old. Consider explaining any relevant recent experience."}
            
            return {"valid": True}
            
        except ValueError:
            return {"valid": False, "message": "Graduation year must be a valid number"}
    
    def _validate_test_score(self, field_name: str, score_str: str) -> Dict[str, Any]:
        """Validate standardized test scores"""
        if not score_str:
            return {"valid": True}  # Optional field
        
        try:
            score = float(score_str)
            
            # Get validation rules for this field
            field_rules = None
            if "GRE Verbal" in field_name:
                field_rules = self.validation_rules.get("gre_verbal", {})
            elif "GRE Quantitative" in field_name:
                field_rules = self.validation_rules.get("gre_quantitative", {})
            elif "GRE Writing" in field_name:
                field_rules = self.validation_rules.get("gre_writing", {})
            elif "TOEFL" in field_name:
                field_rules = self.validation_rules.get("toefl", {})
            elif "IELTS" in field_name:
                field_rules = self.validation_rules.get("ielts", {})
            
            if field_rules:
                min_score = field_rules.get("min", 0)
                max_score = field_rules.get("max", 100)
                
                if score < min_score or score > max_score:
                    return {"valid": False, "message": field_rules.get("message", f"Score must be between {min_score} and {max_score}")}
            
            return {"valid": True}
            
        except ValueError:
            return {"valid": False, "message": "Score must be a valid number"}
    
    def _validate_essay(self, field_name: str, essay_text: str) -> Dict[str, Any]:
        """Validate essay length and content"""
        if not essay_text:
            return {"valid": False, "message": f"{field_name} is required"}
        
        word_count = len(essay_text.split())
        
        # Get essay requirements
        essay_key = None
        if "Statement of Purpose" in field_name:
            essay_key = "statement_of_purpose"
        elif "Personal Statement" in field_name:
            essay_key = "personal_statement"
        elif "Research Interests" in field_name:
            essay_key = "research_interests"
        elif "Career Goals" in field_name:
            essay_key = "career_goals"
        
        if essay_key and essay_key in self.essay_requirements:
            requirements = self.essay_requirements[essay_key]
            min_words = requirements.get("min_words", 0)
            max_words = requirements.get("max_words", 1000)
            
            if word_count < min_words:
                return {"valid": False, "message": f"Essay must be at least {min_words} words (current: {word_count})"}
            elif word_count > max_words:
                return {"valid": False, "message": f"Essay must be no more than {max_words} words (current: {word_count})"}
            elif word_count < min_words * 0.8:
                return {"valid": True, "warning": f"Essay is quite short ({word_count} words). Consider adding more detail."}
        
        return {"valid": True}
    
    def _validate_diversity_statement(self, essay_text: str) -> Dict[str, Any]:
        """Validate diversity statement (optional)"""
        if not essay_text:
            return {"valid": True}  # Optional field
        
        word_count = len(essay_text.split())
        requirements = self.essay_requirements.get("diversity_statement", {})
        min_words = requirements.get("min_words", 200)
        max_words = requirements.get("max_words", 400)
        
        if word_count < min_words:
            return {"valid": False, "message": f"Diversity statement should be at least {min_words} words (current: {word_count})"}
        elif word_count > max_words:
            return {"valid": False, "message": f"Diversity statement should be no more than {max_words} words (current: {word_count})"}
        
        return {"valid": True}
    
    def _validate_references(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate reference information"""
        required_ref_fields = [
            "Reference 1 - Name", "Reference 1 - Title/Position", "Reference 1 - Institution/Organization",
            "Reference 1 - Email", "Reference 1 - Relationship",
            "Reference 2 - Name", "Reference 2 - Title/Position", "Reference 2 - Institution/Organization", 
            "Reference 2 - Email", "Reference 2 - Relationship"
        ]
        
        missing_fields = []
        for field in required_ref_fields:
            if field not in response_data or not response_data[field]:
                missing_fields.append(field)
        
        if missing_fields:
            return {"valid": False, "message": f"Missing required reference fields: {', '.join(missing_fields)}"}
        
        # Validate reference emails
        ref1_email = response_data.get("Reference 1 - Email", "")
        ref2_email = response_data.get("Reference 2 - Email", "")
        
        if ref1_email and not self._validate_email(ref1_email)["valid"]:
            return {"valid": False, "message": "Reference 1 email is invalid"}
        
        if ref2_email and not self._validate_email(ref2_email)["valid"]:
            return {"valid": False, "message": "Reference 2 email is invalid"}
        
        return {"valid": True}
    
    def _check_completeness(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check overall form completeness"""
        all_fields = self._get_required_fields()
        optional_fields = [
            "Class Rank", "Academic Honors and Awards", "Reference 3 - Name",
            "Reference 3 - Title/Position", "Reference 3 - Institution/Organization",
            "Reference 3 - Email", "Reference 3 - Phone", "Reference 3 - Relationship",
            "Notable Projects", "Diversity and Inclusion Statement (Optional, 200-400 words)",
            "Honors, Awards, and Recognition", "Extracurricular Activities and Leadership",
            "Additional Information"
        ]
        
        total_fields = len(all_fields) + len(optional_fields)
        completed_fields = 0
        
        for field in all_fields + optional_fields:
            if field in response_data and response_data[field]:
                completed_fields += 1
        
        completeness_percentage = (completed_fields / total_fields) * 100
        
        if completeness_percentage < 50:
            return {"score": completeness_percentage, "message": "Form is very incomplete", "penalty": 20}
        elif completeness_percentage < 80:
            return {"score": completeness_percentage, "message": "Form could be more complete", "penalty": 10}
        else:
            return {"score": completeness_percentage, "message": "Form is well completed", "penalty": 0}

def main():
    """Test the validator with sample data"""
    validator = FormValidator()
    
    # Sample response data
    sample_response = {
        "Full Name": "John Doe",
        "Email Address": "john.doe@example.com",
        "Phone Number": "+1234567890",
        "GPA": "3.5",
        "Graduation Year": "2020",
        "Statement of Purpose (750-1000 words)": "This is a sample statement of purpose. " * 100,  # ~500 words
        "Personal Statement (500-750 words)": "This is a sample personal statement. " * 50,  # ~250 words
        "Reference 1 - Name": "Dr. Smith",
        "Reference 1 - Email": "smith@university.edu"
    }
    
    result = validator.validate_response(sample_response)
    
    print(f"Validation Result:")
    print(f"Valid: {result.is_valid}")
    print(f"Score: {result.score}/100")
    print(f"Errors: {result.errors}")
    print(f"Warnings: {result.warnings}")

if __name__ == "__main__":
    main()