import os
import json
import pandas as pd
from pathlib import Path
from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE

def validate_file(file):
    """
    Validate uploaded file format and size.
    """
    if file is None:
        return False, "No file uploaded"
    
    file_ext = Path(file.name).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        return False, f"Invalid file format. Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}"
    
    if file.size > MAX_FILE_SIZE:
        return False, f"File size exceeds {MAX_FILE_SIZE // (1024*1024)}MB limit"
    
    return True, "File is valid"

def export_to_csv(data, filename="ranked_resumes.csv"):
    """
    Export results to CSV file.
    """
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    return filename

def export_to_json(data, filename="ranked_resumes.json"):
    """
    Export results to JSON file.
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    return filename

def calculate_percentage(score, max_score):
    """
    Calculate percentage score.
    """
    if max_score == 0:
        return 0
    return (score / max_score) * 100

def format_skills(skills_list):
    """
    Format skills list for display.
    """
    return ", ".join(sorted(set(skills_list)))

def create_temp_directory():
    """
    Create temporary directory for file processing.
    """
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    return temp_dir

def cleanup_temp_files(temp_dir):
    """
    Clean up temporary files after processing.
    """
    if temp_dir.exists():
        for file in temp_dir.glob("*"):
            try:
                file.unlink()
            except Exception as e:
                print(f"Error deleting {file}: {e}")
        temp_dir.rmdir() 