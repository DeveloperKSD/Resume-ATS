"""
scanner.py — Enhanced ATS analysis logic
Optimized for 2026 deployment with dual-mode evaluation architecture.
"""

import re
import math
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import pdfplumber
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

# ─────────────────────────────────────────────
# PDF EXTRACTION
# ─────────────────────────────────────────────

def extract_text_from_pdf(pdf_file) -> str:
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

# ─────────────────────────────────────────────
# PREPROCESSING & DICTS
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

TECH_SKILLS = {
    'python','java','javascript','typescript','c++','c#','ruby','go','rust',
    'swift','kotlin','sql','nosql','html','css','react','angular','vue',
    'django','flask','fastapi','spring','nodejs','express','tensorflow',
    'pytorch','sklearn','pandas','numpy','matplotlib','docker','kubernetes',
    'aws','azure','gcp','git','linux','bash','rest','api','graphql',
    'mongodb','postgresql','mysql','redis','kafka','spark','hadoop',
    'machine learning','deep learning','nlp','data science','devops','ci/cd',
    'agile','scrum','microservices','tableau','powerbi','excel','vba',
    'terraform','ansible','jenkins','github actions','airflow','dbt',
    'next.js','tailwind','firebase','supabase','vercel','netlify',
    'selenium','playwright','pytest','junit','jest','cypress',
}

SECTIONS = {
    'experience'     : r'\b(experience|work history|employment|work experience)\b',
    'education'      : r'\b(education|degree|university|college|bachelor|master|phd|b\.?sc|m\.?sc)\b',
    'skills'         : r'\b(skills|technologies|tools|proficiencies|competencies|tech stack)\b',
    'contact'        : r'\b(email|phone|linkedin|github|contact|mobile)\b',
    'summary'        : r'\b(summary|objective|profile|about me|overview)\b',
    'projects'       : r'\b(projects|portfolio|case studies|personal projects)\b',
    'certifications' : r'\b(certifications|certificates|credentials|courses)\b',
}

ACTION_VERBS = {
    'achieved','improved','trained','managed','created','developed','designed',
    'implemented','launched','delivered','led','built','increased','reduced',
    'optimized','automated','streamlined','analyzed','collaborated','deployed',
    'architected','mentored','negotiated','transformed','established','spearheaded',
    'engineered','scaled','migrated','integrated','generated','directed',
}

def preprocess(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_keywords(text: str) -> set:
    words = set(preprocess(text).split())
    return {w for w in words if len(w) > 2 and w not in STOPWORDS}

def extract_bigrams(text: str) -> set:
    words = preprocess(text).split()
    filtered = [w for w in words if w not in STOPWORDS and len(w) > 2]
    return {f"{filtered[i]} {filtered[i+1]}" for i in range(len(filtered)-1)}

def extract_skills(text: str) -> set:
    text_lower = text.lower()
    return {skill for skill in TECH_SKILLS if skill in text_lower}

def detect_sections(text: str) -> list:
    return [name for name, pattern in SECTIONS.items() if re.search(pattern, text.lower())]

def detect_action_verbs(text: str) -> dict:
    words_lower = set(re.findall(r'\b\w+\b', text.lower()))
    found = words_lower & ACTION_VERBS
    missing = ACTION_VERBS - words_lower
    return {'found': sorted(found), 'missing': sorted(list(missing)[:15])}

def quantification_score(text: str) -> dict:
    numbers = re.findall(r'\b\d+[\.,]?\d*\s*(%|x|k|m|b|hrs?|users?|months?)?\b', text.lower())
    percents = re.findall(r'\d+\s*%', text)
    total = len(numbers)
    score = min(100, total * 8)
    return {
        'count': total,
        'percents': len(percents),
        'score': score,
        'label': 'Strong' if score >= 60 else 'Moderate' if score >= 30 else 'Weak',
    }

def readability_score(text: str) -> dict:
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    words = re.findall(r'\b\w+\b', text.lower())
    
    def _count_syllables(w):
        c = len(re.findall(r'[aeiou]+', w))
        if w.endswith('e') and c > 1: c -= 1
        return max(1, c)

    syllables = sum(_count_syllables(w) for w in words)
    if not sentences or not words:
        return {'score': 0, 'label': 'N/A', 'word_count': 0, 'avg_sentence_len': 0, 'sentence_count': 0}

    asl = len(words) / len(sentences)
    asw = syllables / len(words)
    fre = 206.835 - (1.015 * asl) - (84.6 * asw)
    fre = max(0, min(100, fre))

    return {
        'score': round(fre, 1),
        'label': "Easy" if fre >= 70 else "Standard" if fre >= 50 else "Complex" if fre >= 30 else "Very Complex",
        'word_count': len(words),
        'sentence_count': len(sentences),
        'avg_sentence_len': round(asl, 1),
    }

def detect_red_flags(text: str) -> list:
    flags = []
    if len(re.findall(r'[^\x00-\x7F]', text)) > 20:
        flags.append("Non-ASCII characters detected — may confuse legacy ATS models.")
    if re.search(r'(table|column|row|cell)', text.lower()) and len(re.findall(r'\n', text)) < 40:
        flags.append("Potential multi-column layout risk — content lines could be parsed incorrectly.")
    if len(text) < 300:
        flags.append("Critical low length count — possible flattened image layer PDF.")
    if not re.search(r'\b[\w.-]+@[\w.-]+\.\w+\b', text):
        flags.append("Missing or un-parsable email address profile.")
    return flags

# ─────────────────────────────────────────────
# HYBRID COMPARISON ANALYSIS MODELS
# ─────────────────────────────────────────────

def analyze(resume_text: str, job_text: str = None) -> dict:
    resume_clean = preprocess(resume_text)
    found_sections = detect_sections(resume_text)
    readability = readability_score(resume_text)
    action_verbs = detect_action_verbs(resume_text)
    quantification = quantification_score(resume_text)
    red_flags = detect_red_flags(resume_text)
    resume_skills = extract_skills(resume_text)

    if job_text and job_text.strip():
        job_clean = preprocess(job_text)
        
        job_kw = extract_keywords(job_clean)
        resume_kw = extract_keywords(resume_clean)
        matched_kw = job_kw & resume_kw
        missing_kw = job_kw - resume_kw
        kw_ratio = len(matched_kw) / len(job_kw) if job_kw else 0
        kw_score = round(kw_ratio * 35, 2)

        job_skills = extract_skills(job_text)
        matched_skills = job_skills & resume_skills
        missing_skills = job_skills - resume_skills
        skill_ratio = len(matched_skills) / len(job_skills) if job_skills else 0
        skill_score = round(skill_ratio * 25, 2)

        cv = CountVectorizer()
        try:
            cv_matrix = cv.fit_transform([resume_clean, job_clean])
            cos_sim = float(cosine_similarity(cv_matrix)[0][1])
        except Exception:
            cos_sim = 0.0
        cos_score = round(cos_sim * 20, 2)

        tfidf = TfidfVectorizer()
        try:
            tfidf_matrix = tfidf.fit_transform([resume_clean, job_clean])
            tfidf_sim = float(cosine_similarity(tfidf_matrix)[0][1])
        except Exception:
            tfidf_sim = 0.0
        tfidf_score = round(tfidf_sim * 10, 2)

        section_score = round((len(found_sections) / len(SECTIONS)) * 10, 2)
        total = kw_score + skill_score + cos_score + tfidf_score + section_score
        score_vector = np.array([kw_score, skill_score, cos_score, tfidf_score, section_score])

        df_scores = pd.DataFrame({
            'Component': ['Keyword Match', 'Skills Match', 'Cosine Similarity', 'TF-IDF Relevance', 'Section Presence'],
            'Score': score_vector,
            'Max': [35, 25, 20, 10, 10],
            'Percentage': np.round(score_vector / np.array([35, 25, 20, 10, 10]) * 100, 1)
        })

        job_bigrams = extract_bigrams(job_text)
        resume_bigrams = extract_bigrams(resume_text)
        matched_phrases = sorted(job_bigrams & resume_bigrams)
        missing_phrases = sorted(job_bigrams - resume_bigrams)

        try:
            tfidf2 = TfidfVectorizer(max_features=30, stop_words='english')
            tfidf2.fit([job_clean])
            top_jd_terms = tfidf2.get_feature_names_out().tolist()
        except Exception:
            top_jd_terms = []

        return {
            'has_jd': True, 'total': round(float(total), 2), 'score_df': df_scores, 'score_vector': score_vector,
            'kw_match_pct': round(kw_ratio * 100, 1), 'matched_keywords': sorted(matched_kw), 'missing_keywords': sorted(missing_kw),
            'skill_match_pct': round(skill_ratio * 100, 1), 'matched_skills': sorted(matched_skills), 'missing_skills': sorted(missing_skills),
            'cos_sim_pct': round(cos_sim * 100, 1), 'tfidf_sim_pct': round(tfidf_sim * 100, 1),
            'found_sections': found_sections, 'matched_phrases': matched_phrases[:30], 'missing_phrases': missing_phrases[:30],
            'readability': readability, 'action_verbs': action_verbs, 'quantification': quantification, 'red_flags': red_flags, 'top_jd_terms': top_jd_terms
        }

    else:
        sec_score = (len(found_sections) / len(SECTIONS)) * 30
        vrb_score = min(30, len(action_verbs['found']) * 4)
        quant_score = min(25, quantification['score'] * 0.25)
        read_score = 15 if readability['score'] >= 50 else 8
        
        total = sec_score + vrb_score + quant_score + read_score
        score_vector = np.array([sec_score, vrb_score, quant_score, read_score, 0.0])

        df_scores = pd.DataFrame({
            'Component': ['Structural Completeness', 'Action Verb Density', 'Quantifiable Metrics', 'Readability Tier', 'Context Matching'],
            'Score': score_vector, 'Max': [30, 30, 25, 15, 0],
            'Percentage': [round((sec_score/30)*100,1), round((vrb_score/30)*100,1), round((quant_score/25)*100,1), round((read_score/15)*100,1), 0.0]
        })

        return {
            'has_jd': False, 'total': round(float(total), 2), 'score_df': df_scores, 'score_vector': score_vector,
            'matched_skills': sorted(resume_skills), 'found_sections': found_sections, 'readability': readability,
            'action_verbs': action_verbs, 'quantification': quantification, 'red_flags': red_flags,
            'missing_keywords': [], 'missing_skills': [], 'matched_keywords': [], 'top_jd_terms': [], 'matched_phrases': [], 'missing_phrases': []
        }

def verdict(score: float) -> tuple:
    if score >= 80: return ("✅", "Premium Quality", "#00AA00")
    elif score >= 60: return ("🟡", "Compliant Tier", "#eab308")
    elif score >= 40: return ("🟠", "Intermediate Level", "#f97316")
    else: return ("🔴", "Critical Gaps", "#FF0000")

def generate_report(results: dict) -> str:
    emoji, label, _ = verdict(results['total'])
    lines = [
        "=" * 60,
        "        ATS PIPELINE PRO DIAGNOSTICS REPORT (VINTAGE ENGINE)",
        "=" * 60,
        f"\nOVERALL PERFORMANCE SCORE : {results['total']:.1f}/100 — {label} {emoji}",
        "\nMATRIX COMPONENTS ANALYSIS:",
    ]
    for _, row in results['score_df'].iterrows():
        lines.append(f"  - {row['Component']:<25} : {row['Score']:.1f}/{row['Max']} ({row['Percentage']:.0f}%)")
    lines += [
        "\n" + "-" * 40,
        "STRUCTURAL & TEXT MATRICES",
        "-" * 40,
        f"Readability Index    : {results['readability']['score']} ({results['readability']['label']})",
        f"Total Word Tokens    : {results['readability']['word_count']}",
    ]
    lines.append("\n" + "=" * 60)
    return "\n".join(lines)