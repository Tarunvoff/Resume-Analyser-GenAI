from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from config import WEIGHTS, EDUCATION_LEVELS

class ResumeAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
    def calculate_skills_match(self, required_skills, candidate_skills):
        """
        Calculate skills match score using TF-IDF and cosine similarity.
        """
        if not required_skills or not candidate_skills:
            return 0.0
        
        # Convert skills lists to space-separated strings
        req_text = ' '.join(required_skills).lower()
        cand_text = ' '.join(candidate_skills).lower()
        
        # Calculate TF-IDF and cosine similarity
        try:
            tfidf_matrix = self.vectorizer.fit_transform([req_text, cand_text])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except:
            return 0.0
    
    def calculate_experience_score(self, required_years, candidate_years):
        """
        Calculate experience score based on required years.
        """
        if required_years <= 0:
            return 1.0
        if candidate_years <= 0:
            return 0.0
        
        ratio = candidate_years / required_years
        # Cap the score at 1.0 but allow for exceeding experience
        return min(1.0, ratio)
    
    def calculate_education_score(self, required_level, candidate_level):
        """
        Calculate education score based on level hierarchy.
        """
        required_score = EDUCATION_LEVELS.get(required_level.lower(), 0)
        candidate_score = EDUCATION_LEVELS.get(candidate_level.lower(), 0)
        
        if required_score <= 0:
            return 1.0
        if candidate_score <= 0:
            return 0.0
        
        ratio = candidate_score / required_score
        return min(1.0, ratio)
    
    def analyze_resume(self, resume_data, criteria):
        """
        Analyze a single resume against the given criteria.
        """
        # Calculate individual scores
        skills_score = self.calculate_skills_match(
            criteria.get('required_skills', []),
            resume_data.get('skills', [])
        )
        
        experience_score = self.calculate_experience_score(
            criteria.get('required_years', 0),
            resume_data.get('years_experience', 0)
        )
        
        education_score = self.calculate_education_score(
            criteria.get('required_education', ''),
            resume_data.get('education_level', '')
        )
        
        # Calculate weighted total score
        total_score = (
            skills_score * WEIGHTS['skills'] +
            experience_score * WEIGHTS['experience'] +
            education_score * WEIGHTS['education']
        )
        
        return {
            'name': resume_data.get('name', 'Unknown'),
            'skills_score': round(skills_score * 100, 2),
            'experience_score': round(experience_score * 100, 2),
            'education_score': round(education_score * 100, 2),
            'total_score': round(total_score * 100, 2),
            'skills_matched': [skill for skill in criteria.get('required_skills', [])
                             if skill.lower() in [s.lower() for s in resume_data.get('skills', [])]],
            'years_experience': resume_data.get('years_experience', 0),
            'education_level': resume_data.get('education_level', 'Unknown'),
            'all_skills': resume_data.get('skills', [])
        }
    
    def rank_resumes(self, resumes_data, criteria):
        """
        Rank multiple resumes based on criteria.
        """
        analyzed_resumes = []
        for resume in resumes_data:
            analysis = self.analyze_resume(resume, criteria)
            analyzed_resumes.append(analysis)
        
        # Sort by total score in descending order
        ranked_resumes = sorted(
            analyzed_resumes,
            key=lambda x: x['total_score'],
            reverse=True
        )
        
        # Add rank to each resume
        for i, resume in enumerate(ranked_resumes, 1):
            resume['rank'] = i
        
        return ranked_resumes 