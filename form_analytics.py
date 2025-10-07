#!/usr/bin/env python3
"""
Google Form Analytics
Analyzes form responses and generates insights
"""

import json
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import numpy as np

class FormAnalytics:
    """Analytics engine for Google Form responses"""
    
    def __init__(self, responses_file: str = "form_responses.json"):
        self.responses_file = responses_file
        self.responses = self._load_responses()
        self.df = self._create_dataframe()
    
    def _load_responses(self) -> List[Dict[str, Any]]:
        """Load form responses from file"""
        try:
            with open(self.responses_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Responses file {self.responses_file} not found. Using empty dataset.")
            return []
        except json.JSONDecodeError as e:
            print(f"Error loading responses: {e}")
            return []
    
    def _create_dataframe(self) -> pd.DataFrame:
        """Create pandas DataFrame from responses"""
        if not self.responses:
            return pd.DataFrame()
        
        # Flatten nested responses
        flattened_responses = []
        for response in self.responses:
            flattened = {}
            for key, value in response.items():
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        flattened[f"{key}_{sub_key}"] = sub_value
                else:
                    flattened[key] = value
            flattened_responses.append(flattened)
        
        return pd.DataFrame(flattened_responses)
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics"""
        if self.df.empty:
            return {"total_responses": 0, "message": "No responses found"}
        
        total_responses = len(self.df)
        
        # Calculate completion rates
        required_fields = [
            "Full Name", "Email Address", "Phone Number", "Date of Birth", "Gender",
            "Mailing Address", "Undergraduate Degree", "Institution", "GPA", "Graduation Year"
        ]
        
        completion_rates = {}
        for field in required_fields:
            if field in self.df.columns:
                completion_rates[field] = (self.df[field].notna().sum() / total_responses) * 100
        
        # Calculate average GPA
        avg_gpa = None
        if "GPA" in self.df.columns:
            gpa_values = pd.to_numeric(self.df["GPA"], errors='coerce')
            avg_gpa = gpa_values.mean()
        
        # Calculate gender distribution
        gender_dist = {}
        if "Gender" in self.df.columns:
            gender_dist = self.df["Gender"].value_counts().to_dict()
        
        # Calculate employment status distribution
        employment_dist = {}
        if "Current Employment Status" in self.df.columns:
            employment_dist = self.df["Current Employment Status"].value_counts().to_dict()
        
        # Calculate English proficiency distribution
        english_prof_dist = {}
        if "English Proficiency" in self.df.columns:
            english_prof_dist = self.df["English Proficiency"].value_counts().to_dict()
        
        return {
            "total_responses": total_responses,
            "completion_rates": completion_rates,
            "average_gpa": avg_gpa,
            "gender_distribution": gender_dist,
            "employment_distribution": employment_dist,
            "english_proficiency_distribution": english_prof_dist,
            "date_range": self._get_date_range()
        }
    
    def _get_date_range(self) -> Dict[str, str]:
        """Get date range of responses"""
        if "Timestamp" in self.df.columns:
            timestamps = pd.to_datetime(self.df["Timestamp"], errors='coerce')
            return {
                "earliest": timestamps.min().strftime("%Y-%m-%d %H:%M:%S") if not timestamps.isna().all() else "N/A",
                "latest": timestamps.max().strftime("%Y-%m-%d %H:%M:%S") if not timestamps.isna().all() else "N/A"
            }
        return {"earliest": "N/A", "latest": "N/A"}
    
    def analyze_essays(self) -> Dict[str, Any]:
        """Analyze essay responses"""
        essay_fields = [
            "Statement of Purpose (750-1000 words)",
            "Personal Statement (500-750 words)",
            "Research Interests and Potential Thesis Topics (300-500 words)",
            "Career Goals and Professional Development (300-500 words)"
        ]
        
        essay_analysis = {}
        
        for field in essay_fields:
            if field in self.df.columns:
                essays = self.df[field].dropna()
                if len(essays) > 0:
                    word_counts = essays.apply(lambda x: len(str(x).split()) if x else 0)
                    
                    essay_analysis[field] = {
                        "count": len(essays),
                        "average_words": word_counts.mean(),
                        "min_words": word_counts.min(),
                        "max_words": word_counts.max(),
                        "median_words": word_counts.median()
                    }
        
        return essay_analysis
    
    def analyze_academic_qualifications(self) -> Dict[str, Any]:
        """Analyze academic qualifications"""
        analysis = {}
        
        # GPA analysis
        if "GPA" in self.df.columns:
            gpa_values = pd.to_numeric(self.df["GPA"], errors='coerce').dropna()
            if len(gpa_values) > 0:
                analysis["gpa"] = {
                    "count": len(gpa_values),
                    "mean": gpa_values.mean(),
                    "median": gpa_values.median(),
                    "std": gpa_values.std(),
                    "min": gpa_values.min(),
                    "max": gpa_values.max(),
                    "distribution": {
                        "3.5+": (gpa_values >= 3.5).sum(),
                        "3.0-3.5": ((gpa_values >= 3.0) & (gpa_values < 3.5)).sum(),
                        "2.5-3.0": ((gpa_values >= 2.5) & (gpa_values < 3.0)).sum(),
                        "<2.5": (gpa_values < 2.5).sum()
                    }
                }
        
        # Graduation year analysis
        if "Graduation Year" in self.df.columns:
            grad_years = pd.to_numeric(self.df["Graduation Year"], errors='coerce').dropna()
            if len(grad_years) > 0:
                current_year = datetime.now().year
                years_since_graduation = current_year - grad_years
                
                analysis["graduation_year"] = {
                    "count": len(grad_years),
                    "mean_year": grad_years.mean(),
                    "years_since_graduation": {
                        "mean": years_since_graduation.mean(),
                        "median": years_since_graduation.median(),
                        "recent_graduates": (years_since_graduation <= 2).sum(),
                        "experienced": (years_since_graduation > 5).sum()
                    }
                }
        
        # Institution analysis
        if "Institution" in self.df.columns:
            institutions = self.df["Institution"].value_counts()
            analysis["institutions"] = {
                "total_unique": len(institutions),
                "top_10": institutions.head(10).to_dict()
            }
        
        return analysis
    
    def analyze_test_scores(self) -> Dict[str, Any]:
        """Analyze standardized test scores"""
        test_fields = {
            "GRE Verbal Score": "gre_verbal",
            "GRE Quantitative Score": "gre_quantitative", 
            "GRE Writing Score": "gre_writing",
            "TOEFL Total Score": "toefl",
            "IELTS Overall Score": "ielts"
        }
        
        analysis = {}
        
        for field, key in test_fields.items():
            if field in self.df.columns:
                scores = pd.to_numeric(self.df[field], errors='coerce').dropna()
                if len(scores) > 0:
                    analysis[key] = {
                        "count": len(scores),
                        "mean": scores.mean(),
                        "median": scores.median(),
                        "std": scores.std(),
                        "min": scores.min(),
                        "max": scores.max()
                    }
        
        return analysis
    
    def analyze_prerequisites(self) -> Dict[str, Any]:
        """Analyze prerequisite coursework completion"""
        if "Prerequisite Coursework Completed" not in self.df.columns:
            return {}
        
        prerequisites = [
            "Calculus (I, II, III)", "Linear Algebra", "Statistics and Probability",
            "Programming (Python, Java, C++)", "Data Structures and Algorithms",
            "Machine Learning or AI", "Database Systems", "Computer Science Fundamentals"
        ]
        
        completion_counts = {}
        for prereq in prerequisites:
            # Check if prerequisite is mentioned in responses
            count = 0
            for response in self.df["Prerequisite Coursework Completed"].dropna():
                if prereq in str(response):
                    count += 1
            completion_counts[prereq] = count
        
        total_responses = len(self.df["Prerequisite Coursework Completed"].dropna())
        
        return {
            "total_responses": total_responses,
            "completion_counts": completion_counts,
            "completion_percentages": {
                prereq: (count / total_responses * 100) if total_responses > 0 else 0
                for prereq, count in completion_counts.items()
            }
        }
    
    def generate_insights(self) -> List[str]:
        """Generate actionable insights from the data"""
        insights = []
        
        stats = self.get_summary_stats()
        
        # Response volume insights
        if stats["total_responses"] > 0:
            insights.append(f"Total applications received: {stats['total_responses']}")
            
            if stats["total_responses"] < 10:
                insights.append("Low application volume - consider increasing marketing efforts")
            elif stats["total_responses"] > 100:
                insights.append("High application volume - ensure adequate review capacity")
        
        # GPA insights
        if stats.get("average_gpa"):
            avg_gpa = stats["average_gpa"]
            insights.append(f"Average GPA: {avg_gpa:.2f}")
            
            if avg_gpa < 3.0:
                insights.append("Average GPA is below typical standards - consider adjusting requirements")
            elif avg_gpa > 3.7:
                insights.append("High average GPA - very competitive applicant pool")
        
        # Completion rate insights
        completion_rates = stats.get("completion_rates", {})
        low_completion_fields = [field for field, rate in completion_rates.items() if rate < 80]
        if low_completion_fields:
            insights.append(f"Low completion rates for: {', '.join(low_completion_fields)}")
        
        # Gender diversity insights
        gender_dist = stats.get("gender_distribution", {})
        if gender_dist:
            total_gender = sum(gender_dist.values())
            female_pct = (gender_dist.get("Female", 0) / total_gender) * 100
            insights.append(f"Female applicants: {female_pct:.1f}%")
            
            if female_pct < 30:
                insights.append("Low female representation - consider diversity initiatives")
        
        return insights
    
    def create_visualizations(self, output_dir: str = "analytics_plots"):
        """Create visualization plots"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        if self.df.empty:
            print("No data to visualize")
            return
        
        # Set style
        plt.style.use('seaborn-v0_8')
        
        # GPA distribution
        if "GPA" in self.df.columns:
            gpa_values = pd.to_numeric(self.df["GPA"], errors='coerce').dropna()
            if len(gpa_values) > 0:
                plt.figure(figsize=(10, 6))
                plt.hist(gpa_values, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
                plt.xlabel('GPA')
                plt.ylabel('Frequency')
                plt.title('GPA Distribution of Applicants')
                plt.axvline(gpa_values.mean(), color='red', linestyle='--', label=f'Mean: {gpa_values.mean():.2f}')
                plt.legend()
                plt.tight_layout()
                plt.savefig(f"{output_dir}/gpa_distribution.png", dpi=300, bbox_inches='tight')
                plt.close()
        
        # Gender distribution
        if "Gender" in self.df.columns:
            gender_counts = self.df["Gender"].value_counts()
            if len(gender_counts) > 0:
                plt.figure(figsize=(8, 6))
                gender_counts.plot(kind='bar', color=['lightblue', 'lightpink', 'lightgreen', 'lightgray'])
                plt.xlabel('Gender')
                plt.ylabel('Count')
                plt.title('Gender Distribution of Applicants')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig(f"{output_dir}/gender_distribution.png", dpi=300, bbox_inches='tight')
                plt.close()
        
        # Employment status distribution
        if "Current Employment Status" in self.df.columns:
            emp_counts = self.df["Current Employment Status"].value_counts()
            if len(emp_counts) > 0:
                plt.figure(figsize=(10, 6))
                emp_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
                plt.title('Current Employment Status of Applicants')
                plt.ylabel('')
                plt.tight_layout()
                plt.savefig(f"{output_dir}/employment_status.png", dpi=300, bbox_inches='tight')
                plt.close()
        
        print(f"Visualizations saved to {output_dir}/")

def main():
    """Test the analytics with sample data"""
    # Create sample data
    sample_responses = [
        {
            "Timestamp": "2024-01-15 10:30:00",
            "Full Name": "John Doe",
            "Email Address": "john.doe@example.com",
            "Gender": "Male",
            "GPA": "3.5",
            "Current Employment Status": "Student",
            "English Proficiency": "Native Speaker"
        },
        {
            "Timestamp": "2024-01-16 14:20:00", 
            "Full Name": "Jane Smith",
            "Email Address": "jane.smith@example.com",
            "Gender": "Female",
            "GPA": "3.8",
            "Current Employment Status": "Full-time employed",
            "English Proficiency": "Native Speaker"
        }
    ]
    
    # Save sample data
    with open("form_responses.json", "w") as f:
        json.dump(sample_responses, f, indent=2)
    
    # Run analytics
    analytics = FormAnalytics()
    
    print("Summary Statistics:")
    print(json.dumps(analytics.get_summary_stats(), indent=2))
    
    print("\nInsights:")
    for insight in analytics.generate_insights():
        print(f"- {insight}")

if __name__ == "__main__":
    main()