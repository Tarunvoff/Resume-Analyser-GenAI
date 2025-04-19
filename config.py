import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')

# File Processing
ALLOWED_EXTENSIONS = {'.pdf', '.docx'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Scoring Weights
WEIGHTS = {
    'skills': 0.5,
    'experience': 0.3,
    'education': 0.2
}

# Education Levels and Scores
EDUCATION_LEVELS = {
    'high school': 1,
    'associate': 2,
    'bachelor': 3,
    'master': 4,
    'phd': 5,
    'doctorate': 5
}

# AI Prompt Templates
RESUME_EXTRACTION_PROMPT = """
Extract the following information from the resume text:
- Full Name
- Skills (as a list)
- Education Level (highest degree)
- Years of Experience (total number)

Format the response as JSON with these exact keys:
{
    "name": "",
    "skills": [],
    "education_level": "",
    "years_experience": 0
}
"""

# Regular Expression Patterns
NAME_PATTERN = r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)'
EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
PHONE_PATTERN = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
EXPERIENCE_PATTERN = r'(\d+)\+?\s*(?:years?|yrs?)'

# Tesseract Configuration
TESSERACT_CMD = 'tesseract'  # Update this path for Windows if needed 