import streamlit as st
import pandas as pd
from pathlib import Path
import tempfile
import time
from resume_processor import process_resume
from resume_analyzer import ResumeAnalyzer
from utils import (
    validate_file,
    export_to_csv,
    export_to_json,
    create_temp_directory,
    cleanup_temp_files
)
from config import EDUCATION_LEVELS

def init_session_state():
    """Initialize session state variables."""
    if 'processed_resumes' not in st.session_state:
        st.session_state.processed_resumes = []
    if 'ranked_resumes' not in st.session_state:
        st.session_state.ranked_resumes = []
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = ResumeAnalyzer()

def main():
    st.set_page_config(
        page_title="Resume Analysis & Ranking System",
        page_icon="📄",
        layout="wide"
    )
    
    init_session_state()
    
    st.title("Resume Analysis & Ranking System")
    
    # Create sidebar for inputs
    with st.sidebar:
        st.header("Search Criteria")
        
        # Skills input
        skills_input = st.text_area(
            "Required Skills (one per line)",
            help="Enter each required skill on a new line"
        )
        required_skills = [skill.strip() for skill in skills_input.split("\n") if skill.strip()]
        
        # Experience input
        required_years = st.number_input(
            "Minimum Years of Experience",
            min_value=0,
            value=0
        )
        
        # Education input
        required_education = st.selectbox(
            "Minimum Education Level",
            options=list(EDUCATION_LEVELS.keys()),
            format_func=lambda x: x.title()
        )
        
        # Clear button
        if st.button("Clear All"):
            st.session_state.processed_resumes = []
            st.session_state.ranked_resumes = []
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Upload Resumes")
        uploaded_files = st.file_uploader(
            "Upload PDF/DOCX resumes",
            type=['pdf', 'docx'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            temp_dir = create_temp_directory()
            
            try:
                for i, file in enumerate(uploaded_files):
                    status_text.text(f"Processing {file.name}...")
                    
                    # Validate file
                    is_valid, message = validate_file(file)
                    if not is_valid:
                        st.error(f"Error with {file.name}: {message}")
                        continue
                    
                    # Save file temporarily
                    temp_file = temp_dir / file.name
                    with open(temp_file, 'wb') as f:
                        f.write(file.getvalue())
                    
                    # Process resume
                    try:
                        result = process_resume(temp_file)
                        st.session_state.processed_resumes.append(result)
                    except Exception as e:
                        st.error(f"Error processing {file.name}: {str(e)}")
                    
                    progress_bar.progress((i + 1) / len(uploaded_files))
                
                # Analyze and rank resumes
                if st.session_state.processed_resumes:
                    criteria = {
                        'required_skills': required_skills,
                        'required_years': required_years,
                        'required_education': required_education
                    }
                    
                    st.session_state.ranked_resumes = st.session_state.analyzer.rank_resumes(
                        st.session_state.processed_resumes,
                        criteria
                    )
                    
                    status_text.text("Processing complete!")
                
            finally:
                cleanup_temp_files(temp_dir)
    
    with col2:
        st.header("Export Results")
        if st.session_state.ranked_resumes:
            if st.button("Export to CSV"):
                filename = export_to_csv(st.session_state.ranked_resumes)
                st.success(f"Results exported to {filename}")
            
            if st.button("Export to JSON"):
                filename = export_to_json(st.session_state.ranked_resumes)
                st.success(f"Results exported to {filename}")
    
    # Display results
    if st.session_state.ranked_resumes:
        st.header("Ranked Results")
        
        # Convert to DataFrame for display
        df = pd.DataFrame(st.session_state.ranked_resumes)
        
        # Reorder columns for better display
        columns = ['rank', 'name', 'total_score', 'skills_score', 
                  'experience_score', 'education_score', 'years_experience',
                  'education_level']
        
        st.dataframe(
            df[columns].style.format({
                'total_score': '{:.1f}%',
                'skills_score': '{:.1f}%',
                'experience_score': '{:.1f}%',
                'education_score': '{:.1f}%'
            }),
            height=400
        )
        
        # Detailed view
        st.header("Detailed Analysis")
        for resume in st.session_state.ranked_resumes:
            with st.expander(f"#{resume['rank']} - {resume['name']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Scores")
                    st.write(f"Total Score: {resume['total_score']:.1f}%")
                    st.write(f"Skills Score: {resume['skills_score']:.1f}%")
                    st.write(f"Experience Score: {resume['experience_score']:.1f}%")
                    st.write(f"Education Score: {resume['education_score']:.1f}%")
                
                with col2:
                    st.subheader("Details")
                    st.write(f"Years of Experience: {resume['years_experience']}")
                    st.write(f"Education Level: {resume['education_level'].title()}")
                    st.write("Matched Skills:", ", ".join(resume['skills_matched']))
                    st.write("All Skills:", ", ".join(resume['all_skills']))

if __name__ == "__main__":
    main() 