import re
import PyPDF2
import docx
import pytesseract
from pdf2image import convert_from_path
import together
from pathlib import Path
import spacy
import json
from config import (
    TOGETHER_API_KEY,
    RESUME_EXTRACTION_PROMPT,
    NAME_PATTERN,
    EXPERIENCE_PATTERN,
    EDUCATION_LEVELS,
    TESSERACT_CMD
)

# Initialize Together AI client
together.api_key = TOGETHER_API_KEY

# Load spaCy model
nlp = spacy.load("en_core_web_lg")

def extract_text_from_pdf(file_path):
    """
    Extract text from PDF files with OCR fallback.
    """
    try:
        # Try normal PDF extraction first
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
        
        # If no text was extracted, use OCR
        if not text.strip():
            images = convert_from_path(file_path)
            text = ""
            for image in images:
                text += pytesseract.image_to_string(image) + "\n"
        
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def extract_text_from_docx(file_path):
    """
    Extract text from DOCX files.
    """
    try:
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from DOCX: {str(e)}")

def extract_using_ai(text):
    """
    Extract information using Together AI API.
    """
    try:
        response = together.Complete.create(
            prompt=f"{RESUME_EXTRACTION_PROMPT}\n\nResume Text:\n{text}",
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            max_tokens=1000,
            temperature=0.3
        )
        
        # Extract the JSON response from the completion
        result = response['output']['choices'][0]['text']
        # Find the JSON object in the response
        json_str = re.search(r'\{.*\}', result, re.DOTALL)
        if json_str:
            return json.loads(json_str.group())
        return None
    except Exception as e:
        return None

def extract_using_patterns(text):
    """
    Fallback extraction using regex patterns.
    """
    # Extract name
    name_match = re.search(NAME_PATTERN, text, re.MULTILINE)
    name = name_match.group(1) if name_match else ""

    # Extract experience years
    exp_match = re.search(EXPERIENCE_PATTERN, text)
    years_experience = int(exp_match.group(1)) if exp_match else 0

    # Extract education level
    education_level = "unknown"
    for level in EDUCATION_LEVELS.keys():
        if re.search(rf'\b{level}\b', text.lower()):
            education_level = level
            break

    # Extract skills using spaCy
    doc = nlp(text)
    skills = []
    for ent in doc.ents:
        if ent.label_ in ["PRODUCT", "ORG", "GPE"]:
            skills.append(ent.text)

    return {
        "name": name,
        "skills": skills,
        "education_level": education_level,
        "years_experience": years_experience
    }

def process_resume(file_path):
    """
    Process a single resume file.
    """
    # Extract text based on file type
    file_ext = Path(file_path).suffix.lower()
    if file_ext == '.pdf':
        text = extract_text_from_pdf(file_path)
    elif file_ext == '.docx':
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_ext}")

    # Try AI extraction first
    result = extract_using_ai(text)
    
    # Fallback to pattern matching if AI extraction fails
    if not result:
        result = extract_using_patterns(text)
    
    return result 