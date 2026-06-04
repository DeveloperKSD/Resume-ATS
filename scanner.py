"""
scanner.py — Core ATS analysis logic
Uses: pdfplumber, sklearn, numpy, pandas
"""

import re
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import pdfplumber
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ─────────────────────────────────────────────
# PDF EXTRACTION
# ─────────────────────────────────────────────

def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from a PDF file object (path or file-like object)."""
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


# ─────────────────────────────────────────────
# PREPROCESSING
# ─────────────────────────────────────────────

STOPWORDS = {
    'a','an','the','and','or','but','in','on','at','to','for','of','with',
    'by','from','is','are','was','were','be','been','being','have','has',
    'had','do','does','did','will','would','could','should','may','might',
    'shall','can','need','our','we','you','your','their','this','that',
    'these','those','it','its','as','if','not','no','so','up','out','into',
    'than','then','also','both','each','more','such','well','us','per',
    'via','i','my','me','about','all','other','any','they','he','she',
    'who','which','what','when','how','us','am','very','just','use','using'
}

def preprocess(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_keywords(text: str) -> set:
    words = set(preprocess(text).split())
    return {w for w in words if len(w) > 2 and w not in STOPWORDS}


# ─────────────────────────────────────────────
# TECH SKILLS LIBRARY
# ─────────────────────────────────────────────

TECH_SKILLS = {
    'python','java','javascript','typescript','c++','c#','ruby','go','rust',
    'swift','kotlin','sql','nosql','html','css','react','angular','vue',
    'django','flask','fastapi','spring','nodejs','express','tensorflow',
    'pytorch','sklearn','pandas','numpy','matplotlib','docker','kubernetes',
    'aws','azure','gcp','git','linux','bash','rest','api','graphql',
    'mongodb','postgresql','mysql','redis','kafka','spark','hadoop',
    'machine learning','deep learning','nlp','data science','devops','ci/cd',
    'agile','scrum','microservices','tableau','powerbi','excel','vba',
}

def extract_skills(text: str) -> set:
    text_lower = text.lower()
    found = set()
    for skill in TECH_SKILLS:
        if skill in text_lower:
            found.add(skill)
    return found


# ─────────────────────────────────────────────
# SECTION DETECTION
# ─────────────────────────────────────────────

SECTIONS = {
    'experience'  : r'\b(experience|work history|employment|work experience)\b',
    'education'   : r'\b(education|degree|university|college|bachelor|master|phd|b\.?sc|m\.?sc)\b',
    'skills'      : r'\b(skills|technologies|tools|proficiencies|competencies|tech stack)\b',
    'contact'     : r'\b(email|phone|linkedin|github|contact|mobile)\b',
    'summary'     : r'\b(summary|objective|profile|about me|overview)\b',
    'projects'    : r'\b(projects|portfolio|case studies|personal projects)\b',
    'certifications': r'\b(certifications|certificates|credentials|courses)\b',
}

def detect_sections(text: str) -> list:
    found = []
    for name, pattern in SECTIONS.items():
        if re.search(pattern, text.lower()):
            found.append(name)
    return found


# ─────────────────────────────────────────────
# MAIN ATS ANALYSIS
# ─────────────────────────────────────────────

def analyze(resume_text: str, job_text: str) -> dict:
    """
    Full ATS analysis. Returns a dict with all scores and metadata.

    Score breakdown (total = 100):
      - Keyword Match    : 35 pts
      - Skills Match     : 25 pts
      - Cosine Similarity: 20 pts
      - TF-IDF Relevance : 10 pts
      - Section Presence : 10 pts
    """
    resume_clean = preprocess(resume_text)
    job_clean    = preprocess(job_text)

    # ── 1. Keyword Match (35 pts) ──────────────
    job_kw      = extract_keywords(job_clean)
    resume_kw   = extract_keywords(resume_clean)
    matched_kw  = job_kw & resume_kw
    missing_kw  = job_kw - resume_kw
    kw_ratio    = len(matched_kw) / len(job_kw) if job_kw else 0
    kw_score    = round(kw_ratio * 35, 2)

    # ── 2. Skills Match (25 pts) ───────────────
    job_skills     = extract_skills(job_text)
    resume_skills  = extract_skills(resume_text)
    matched_skills = job_skills & resume_skills
    missing_skills = job_skills - resume_skills
    skill_ratio    = len(matched_skills) / len(job_skills) if job_skills else 0
    skill_score    = round(skill_ratio * 25, 2)

    # ── 3. Cosine Similarity (20 pts) ─────────
    cv          = CountVectorizer()
    cv_matrix   = cv.fit_transform([resume_clean, job_clean])
    cos_sim     = cosine_similarity(cv_matrix)[0][1]
    cos_score   = round(cos_sim * 20, 2)

    # ── 4. TF-IDF Relevance (10 pts) ──────────
    tfidf        = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform([resume_clean, job_clean])
    tfidf_sim    = cosine_similarity(tfidf_matrix)[0][1]
    tfidf_score  = round(tfidf_sim * 10, 2)

    # ── 5. Section Presence (10 pts) ──────────
    found_sections = detect_sections(resume_text)
    section_score  = round((len(found_sections) / len(SECTIONS)) * 10, 2)

    # ── Total ──────────────────────────────────
    total = kw_score + skill_score + cos_score + tfidf_score + section_score

    # ── Score vector as numpy array (for charting) ──
    score_vector = np.array([kw_score, skill_score, cos_score, tfidf_score, section_score])

    # ── Results DataFrame ──────────────────────
    df = pd.DataFrame({
        'Component'  : ['Keyword Match', 'Skills Match', 'Cosine Similarity', 'TF-IDF Relevance', 'Section Presence'],
        'Score'      : score_vector,
        'Max'        : [35, 25, 20, 10, 10],
        'Percentage' : np.round(score_vector / np.array([35, 25, 20, 10, 10]) * 100, 1)
    })

    return {
        'total'             : round(float(total), 2),
        'score_df'          : df,
        'score_vector'      : score_vector,

        'kw_score'          : kw_score,
        'kw_match_pct'      : round(kw_ratio * 100, 1),
        'matched_keywords'  : sorted(matched_kw),
        'missing_keywords'  : sorted(missing_kw),

        'skill_score'       : skill_score,
        'skill_match_pct'   : round(skill_ratio * 100, 1),
        'matched_skills'    : sorted(matched_skills),
        'missing_skills'    : sorted(missing_skills),

        'cos_score'         : cos_score,
        'cos_sim_pct'       : round(float(cos_sim) * 100, 1),

        'tfidf_score'       : tfidf_score,
        'tfidf_sim_pct'     : round(float(tfidf_sim) * 100, 1),

        'section_score'     : section_score,
        'found_sections'    : found_sections,
    }


def verdict(score: float) -> tuple:
    """Return (emoji, label, color) based on total score."""
    if score >= 80:
        return ("✅", "Excellent Match",  "#22c55e")
    elif score >= 60:
        return ("🟡", "Good Match",       "#eab308")
    elif score >= 40:
        return ("🟠", "Moderate Match",   "#f97316")
    else:
        return ("🔴", "Poor Match",       "#ef4444")
