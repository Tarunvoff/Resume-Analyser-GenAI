# Resume Analysis and Ranking System

A Streamlit-based application for analyzing and ranking resumes based on skills, experience, and education criteria.

## Features
- Upload multiple resumes (PDF and DOCX formats)
- Extract information using AI and pattern matching
- Rank candidates based on customizable criteria
- Export results to CSV/JSON
- Detailed resume analysis view

## Setup Instructions

1. Install Python 3.8 or higher
2. Install Tesseract OCR:
   - Windows: Download installer from https://github.com/UB-Mannheim/tesseract/wiki
   - Linux: `sudo apt-get install tesseract-ocr`
   - Mac: `brew install tesseract`

3. Install dependencies:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_lg
```

4. Set up environment variables:
Create a `.env` file with:
```
TOGETHER_API_KEY=your_api_key_here
```

5. Run the application:
```bash
streamlit run app.py
```

## Usage
1. Launch the application
2. Upload resumes (PDF/DOCX)
3. Set criteria for skills, experience, and education
4. View ranked results
5. Export results as needed

## File Structure
- `app.py`: Main Streamlit application
- `resume_processor.py`: Resume text extraction and processing
- `resume_analyzer.py`: Analysis and scoring logic
- `utils.py`: Utility functions
- `config.py`: Configuration settings 