"""
scanner.py — Enhanced ATS analysis logic
New: bigram/phrase matching, readability score, keyword density,
     action verb detection, quantification score, ATS red flags.
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

def extract_bigrams(text: str) -> set:
    """Extract meaningful 2-word phrases from text."""
    words = preprocess(text).split()
    filtered = [w for w in words if w not in STOPWORDS and len(w) > 2]
    return {f"{filtered[i]} {filtered[i+1]}" for i in range(len(filtered)-1)}

def keyword_frequency(text: str, keywords: set) -> dict:
    """Count how many times each keyword appears in text."""
    text_lower = text.lower()
    return {kw: text_lower.split().count(kw) for kw in keywords}


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
    'terraform','ansible','jenkins','github actions','airflow','dbt',
    'next.js','tailwind','firebase','supabase','vercel','netlify',
    'selenium','playwright','pytest','junit','jest','cypress',
}

def extract_skills(text: str) -> set:
    text_lower = text.lower()
    return {skill for skill in TECH_SKILLS if skill in text_lower}


# ─────────────────────────────────────────────
# SECTION DETECTION
# ─────────────────────────────────────────────

SECTIONS = {
    'experience'     : r'\b(experience|work history|employment|work experience)\b',
    'education'      : r'\b(education|degree|university|college|bachelor|master|phd|b\.?sc|m\.?sc)\b',
    'skills'         : r'\b(skills|technologies|tools|proficiencies|competencies|tech stack)\b',
    'contact'        : r'\b(email|phone|linkedin|github|contact|mobile)\b',
    'summary'        : r'\b(summary|objective|profile|about me|overview)\b',
    'projects'       : r'\b(projects|portfolio|case studies|personal projects)\b',
    'certifications' : r'\b(certifications|certificates|credentials|courses)\b',
}

def detect_sections(text: str) -> list:
    return [name for name, pattern in SECTIONS.items()
            if re.search(pattern, text.lower())]


# ─────────────────────────────────────────────
# READABILITY (Flesch-Kincaid approximation)
# ─────────────────────────────────────────────

def readability_score(text: str) -> dict:
    """
    Returns Flesch Reading Ease score and grade label.
    Higher = easier to read. ATS-friendly zone: 60-80.
    """
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    words     = re.findall(r'\b\w+\b', text.lower())
    syllables = sum(_count_syllables(w) for w in words)

    if not sentences or not words:
        return {'score': 0, 'label': 'N/A', 'word_count': 0, 'avg_sentence_len': 0}

    asl  = len(words) / len(sentences)          # avg sentence length
    asw  = syllables / len(words)               # avg syllables per word
    fre  = 206.835 - (1.015 * asl) - (84.6 * asw)
    fre  = max(0, min(100, fre))

    if   fre >= 70: label = "Easy"
    elif fre >= 50: label = "Standard"
    elif fre >= 30: label = "Complex"
    else:           label = "Very Complex"

    return {
        'score'            : round(fre, 1),
        'label'            : label,
        'word_count'       : len(words),
        'sentence_count'   : len(sentences),
        'avg_sentence_len' : round(asl, 1),
    }

def _count_syllables(word: str) -> int:
    word = word.lower()
    count = len(re.findall(r'[aeiou]+', word))
    if word.endswith('e') and count > 1:
        count -= 1
    return max(1, count)


# ─────────────────────────────────────────────
# ACTION VERBS
# ─────────────────────────────────────────────

ACTION_VERBS = {
    'achieved','improved','trained','managed','created','developed','designed',
    'implemented','launched','delivered','led','built','increased','reduced',
    'optimized','automated','streamlined','analyzed','collaborated','deployed',
    'architected','mentored','negotiated','transformed','established','spearheaded',
    'engineered','scaled','migrated','integrated','generated','directed',
}

def detect_action_verbs(text: str) -> dict:
    words_lower = set(re.findall(r'\b\w+\b', text.lower()))
    found   = words_lower & ACTION_VERBS
    missing = ACTION_VERBS - words_lower
    return {'found': sorted(found), 'missing': sorted(list(missing)[:15])}


# ─────────────────────────────────────────────
# QUANTIFICATION DETECTION
# ─────────────────────────────────────────────

def quantification_score(text: str) -> dict:
    """Detect numbers/percentages — quantified bullets score better."""
    numbers  = re.findall(r'\b\d+[\.,]?\d*\s*(%|x|k|m|b|hrs?|users?|months?)?\b', text.lower())
    percents = re.findall(r'\d+\s*%', text)
    total    = len(numbers)
    score    = min(100, total * 8)          # rough: 12+ numbers ≈ 100%
    return {
        'count'    : total,
        'percents' : len(percents),
        'score'    : score,
        'label'    : 'Strong' if score >= 60 else 'Moderate' if score >= 30 else 'Weak',
    }


# ─────────────────────────────────────────────
# ATS RED FLAGS
# ─────────────────────────────────────────────

def detect_red_flags(text: str) -> list:
    flags = []
    if len(re.findall(r'[^\x00-\x7F]', text)) > 20:
        flags.append("Non-ASCII characters detected — may confuse ATS parsers.")
    if re.search(r'(table|column|row|cell)', text.lower()):
        flags.append("Possible table layout — ATS often mis-parses multi-column resumes.")
    if len(text) < 300:
        flags.append("Resume text is very short — possible parsing failure or image-based PDF.")
    if not re.search(r'\b[\w.-]+@[\w.-]+\.\w+\b', text):
        flags.append("No email address detected in parsed text.")
    if re.search(r'(header|footer)', text.lower()):
        flags.append("Header/footer text detected — ATS may ignore contact info in headers.")
    if len(re.findall(r'\b(i am|i have|i built|i created)\b', text.lower())) > 5:
        flags.append("Excessive first-person pronouns — prefer third-person implied style.")
    return flags


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

    total        = kw_score + skill_score + cos_score + tfidf_score + section_score
    score_vector = np.array([kw_score, skill_score, cos_score, tfidf_score, section_score])

    # ── Score DataFrame ────────────────────────
    df = pd.DataFrame({
        'Component'  : ['Keyword Match', 'Skills Match', 'Cosine Similarity', 'TF-IDF Relevance', 'Section Presence'],
        'Score'      : score_vector,
        'Max'        : [35, 25, 20, 10, 10],
        'Percentage' : np.round(score_vector / np.array([35, 25, 20, 10, 10]) * 100, 1)
    })

    # ── Bigram / Phrase Analysis ───────────────
    job_bigrams    = extract_bigrams(job_text)
    resume_bigrams = extract_bigrams(resume_text)
    matched_phrases = sorted(job_bigrams & resume_bigrams)
    missing_phrases = sorted(job_bigrams - resume_bigrams)

    # ── Keyword Frequency (for heatmap) ───────
    kw_freq_resume = keyword_frequency(resume_text, matched_kw)
    kw_freq_jd     = keyword_frequency(job_text, matched_kw)

    # ── Bonus analytics ───────────────────────
    readability     = readability_score(resume_text)
    action_verbs    = detect_action_verbs(resume_text)
    quantification  = quantification_score(resume_text)
    red_flags       = detect_red_flags(resume_text)

    # ── Top TF-IDF terms from JD ───────────────
    try:
        tfidf2     = TfidfVectorizer(max_features=30, stop_words='english')
        tfidf2.fit([job_clean])
        top_jd_terms = tfidf2.get_feature_names_out().tolist()
    except Exception:
        top_jd_terms = []

    return {
        # Core scores
        'total'             : round(float(total), 2),
        'score_df'          : df,
        'score_vector'      : score_vector,

        # Keyword
        'kw_score'          : kw_score,
        'kw_match_pct'      : round(kw_ratio * 100, 1),
        'matched_keywords'  : sorted(matched_kw),
        'missing_keywords'  : sorted(missing_kw),
        'kw_freq_resume'    : kw_freq_resume,
        'kw_freq_jd'        : kw_freq_jd,

        # Skills
        'skill_score'       : skill_score,
        'skill_match_pct'   : round(skill_ratio * 100, 1),
        'matched_skills'    : sorted(matched_skills),
        'missing_skills'    : sorted(missing_skills),

        # Similarity
        'cos_score'         : cos_score,
        'cos_sim_pct'       : round(float(cos_sim) * 100, 1),
        'tfidf_score'       : tfidf_score,
        'tfidf_sim_pct'     : round(float(tfidf_sim) * 100, 1),

        # Sections
        'section_score'     : section_score,
        'found_sections'    : found_sections,

        # Phrases
        'matched_phrases'   : matched_phrases[:30],
        'missing_phrases'   : missing_phrases[:30],

        # Bonus
        'readability'       : readability,
        'action_verbs'      : action_verbs,
        'quantification'    : quantification,
        'red_flags'         : red_flags,
        'top_jd_terms'      : top_jd_terms,
    }


def verdict(score: float) -> tuple:
    if   score >= 80: return ("✅", "Excellent Match",  "#22c55e")
    elif score >= 60: return ("🟡", "Good Match",       "#eab308")
    elif score >= 40: return ("🟠", "Moderate Match",   "#f97316")
    else:             return ("🔴", "Poor Match",       "#ef4444")


# ─────────────────────────────────────────────
# REPORT GENERATION
# ─────────────────────────────────────────────

def generate_report(results: dict) -> str:
    """Generate a plain-text improvement report for download."""
    emoji, label, _ = verdict(results['total'])
    lines = [
        "=" * 60,
        "  ATS RESUME SCAN REPORT",
        "=" * 60,
        f"\nOVERALL SCORE : {results['total']:.1f}/100 — {label}",
        f"\nSCORE BREAKDOWN:",
    ]
    for _, row in results['score_df'].iterrows():
        lines.append(f"  {row['Component']:<22} {row['Score']:.1f}/{row['Max']}  ({row['Percentage']:.0f}%)")

    lines += [
        f"\nREADABILITY   : {results['readability']['score']} ({results['readability']['label']})",
        f"WORD COUNT    : {results['readability']['word_count']}",
        f"QUANTIFICATION: {results['quantification']['label']} ({results['quantification']['count']} numbers found)",
        "",
        "MATCHED SKILLS :",
        "  " + ", ".join(results['matched_skills']) if results['matched_skills'] else "  None",
        "",
        "MISSING SKILLS :",
        "  " + ", ".join(results['missing_skills']) if results['missing_skills'] else "  None",
        "",
        "ACTION VERBS USED :",
        "  " + ", ".join(results['action_verbs']['found']) if results['action_verbs']['found'] else "  None",
        "",
        "ATS RED FLAGS :",
    ]
    for flag in results['red_flags']:
        lines.append(f"  ⚠ {flag}")
    if not results['red_flags']:
        lines.append("  None detected.")

    lines += [
        "",
        "TOP JD TERMS NOT IN RESUME :",
        "  " + ", ".join(results['missing_keywords'][:20]),
        "",
        "=" * 60,
        "Generated by ATS Resume Scanner",
        "=" * 60,
    ]
    return "\n".join(lines)
