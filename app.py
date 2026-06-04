"""
app.py — Streamlit UI for ATS Resume Scanner
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
from scanner import extract_text_from_pdf, analyze, verdict
from charts  import bar_chart, radar_chart, gauge_chart


# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="ATS Resume Scanner",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0f1117;
    color: #e2e8f0;
}

.block-container { padding: 2rem 3rem; max-width: 1200px; }

h1, h2, h3 { font-family: 'Syne', sans-serif; }

.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 2rem;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.05em;
    width: 100%;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.85; }

.metric-card {
    background: #1e2130;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    border: 1px solid #2a2f45;
    margin-bottom: 1rem;
}

.score-badge {
    font-family: 'DM Mono', monospace;
    font-size: 3rem;
    font-weight: 700;
    line-height: 1;
}

.tag {
    display: inline-block;
    background: #1e2130;
    border: 1px solid #2a2f45;
    border-radius: 6px;
    padding: 3px 10px;
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    margin: 3px 3px 3px 0;
    color: #94a3b8;
}

.tag-green  { border-color: #22c55e44; color: #22c55e; background: #22c55e11; }
.tag-red    { border-color: #ef444444; color: #ef4444; background: #ef444411; }

.section-header {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: #6366f1;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}

hr { border-color: #2a2f45; margin: 1.5rem 0; }

.stFileUploader { background: #1e2130 !important; border-radius: 10px; }

[data-testid="stDataFrame"] { background: #1e2130 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────

st.markdown("""
<div style='text-align:center; padding: 2rem 0 1rem 0;'>
  <h1 style='font-size:2.8rem; font-weight:800; letter-spacing:-0.02em; margin:0;'>
    📄 ATS Resume Scanner
  </h1>
  <p style='color:#94a3b8; font-size:1.05rem; margin-top:0.5rem;'>
    Upload your resume and a job description PDF to get a detailed ATS compatibility score.
  </p>
</div>
<hr/>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FILE UPLOAD
# ─────────────────────────────────────────────

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<p class="section-header">📋 Your Resume</p>', unsafe_allow_html=True)
    resume_file = st.file_uploader("Upload Resume PDF", type=["pdf"], key="resume",
                                   label_visibility="collapsed")

with col2:
    st.markdown('<p class="section-header">💼 Job Description</p>', unsafe_allow_html=True)
    job_file = st.file_uploader("Upload Job Description PDF", type=["pdf"], key="job",
                                label_visibility="collapsed")

st.markdown("<br/>", unsafe_allow_html=True)
analyze_btn = st.button("🔍 Analyze Resume", disabled=not (resume_file and job_file))

st.markdown("<hr/>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ANALYSIS
# ─────────────────────────────────────────────

if analyze_btn and resume_file and job_file:
    with st.spinner("Extracting text and running analysis..."):
        resume_text = extract_text_from_pdf(resume_file)
        job_text    = extract_text_from_pdf(job_file)

        if not resume_text:
            st.error("⚠️ Could not extract text from Resume PDF. Make sure it's not a scanned image.")
            st.stop()
        if not job_text:
            st.error("⚠️ Could not extract text from Job Description PDF.")
            st.stop()

        results = analyze(resume_text, job_text)

    emoji, label, color = verdict(results['total'])

    # ── TOP ROW: Gauge + Verdict + Radar ──────
    r1c1, r1c2, r1c3 = st.columns([1.2, 1.5, 1.2], gap="large")

    with r1c1:
        st.markdown('<p class="section-header">Overall Score</p>', unsafe_allow_html=True)
        st.image(gauge_chart(results['total']), use_column_width=True)

    with r1c2:
        st.markdown('<p class="section-header">Verdict</p>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-card" style="text-align:center; padding:2rem;">
            <div style="font-size:3rem;">{emoji}</div>
            <div class="score-badge" style="color:{color}; margin:0.5rem 0;">
                {results['total']:.1f}<span style="font-size:1.2rem; color:#94a3b8;">/100</span>
            </div>
            <div style="font-size:1.2rem; font-weight:700; color:{color};">{label}</div>
            <hr style="margin:1rem 0;"/>
            <div style="display:flex; justify-content:space-around; color:#94a3b8; font-size:0.85rem;">
                <div>
                    <div style="font-size:1.4rem; font-weight:700; color:#e2e8f0;">
                        {results['kw_match_pct']}%
                    </div>Keyword Hit
                </div>
                <div>
                    <div style="font-size:1.4rem; font-weight:700; color:#e2e8f0;">
                        {results['skill_match_pct']}%
                    </div>Skills Hit
                </div>
                <div>
                    <div style="font-size:1.4rem; font-weight:700; color:#e2e8f0;">
                        {results['cos_sim_pct']}%
                    </div>Similarity
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with r1c3:
        st.markdown('<p class="section-header">Radar</p>', unsafe_allow_html=True)
        st.image(radar_chart(results['score_vector']), use_column_width=True)

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── BAR CHART + SCORE TABLE ────────────────
    r2c1, r2c2 = st.columns([1.6, 1], gap="large")

    with r2c1:
        st.markdown('<p class="section-header">Score Breakdown Chart</p>', unsafe_allow_html=True)
        st.image(bar_chart(results['score_vector']), use_column_width=True)

    with r2c2:
        st.markdown('<p class="section-header">Score Table</p>', unsafe_allow_html=True)
        df = results['score_df'].copy()
        df['Score'] = df['Score'].map(lambda x: f"{x:.1f}")
        df['Max']   = df['Max'].map(str)
        df['%']     = df['Percentage'].map(lambda x: f"{x:.0f}%")
        st.dataframe(df[['Component','Score','Max','%']],
                     hide_index=True, use_container_width=True)

        st.markdown("<br/>", unsafe_allow_html=True)

        # Sections found
        st.markdown('<p class="section-header">Resume Sections Detected</p>', unsafe_allow_html=True)
        all_sections = ['experience','education','skills','contact','summary','projects','certifications']
        tags_html = ""
        for s in all_sections:
            cls = "tag-green" if s in results['found_sections'] else "tag-red"
            icon = "✓" if s in results['found_sections'] else "✗"
            tags_html += f'<span class="tag {cls}">{icon} {s}</span>'
        st.markdown(tags_html, unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── KEYWORDS & SKILLS ─────────────────────
    r3c1, r3c2 = st.columns(2, gap="large")

    with r3c1:
        st.markdown('<p class="section-header">🟢 Matched Keywords</p>', unsafe_allow_html=True)
        if results['matched_keywords']:
            html = "".join(f'<span class="tag tag-green">{k}</span>'
                           for k in results['matched_keywords'][:40])
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.markdown("_None found._")

        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown('<p class="section-header">🔴 Missing Keywords</p>', unsafe_allow_html=True)
        if results['missing_keywords']:
            html = "".join(f'<span class="tag tag-red">{k}</span>'
                           for k in results['missing_keywords'][:40])
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.markdown("_None missing — great!_")

    with r3c2:
        st.markdown('<p class="section-header">🟢 Matched Skills</p>', unsafe_allow_html=True)
        if results['matched_skills']:
            html = "".join(f'<span class="tag tag-green">{s}</span>'
                           for s in results['matched_skills'])
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.markdown("_No matching tech skills found._")

        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown('<p class="section-header">🔴 Missing Skills</p>', unsafe_allow_html=True)
        if results['missing_skills']:
            html = "".join(f'<span class="tag tag-red">{s}</span>'
                           for s in results['missing_skills'])
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.markdown("_No skill gaps detected._")

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── TIPS ──────────────────────────────────
    st.markdown('<p class="section-header">💡 Improvement Tips</p>', unsafe_allow_html=True)
    tips = []

    if results['kw_match_pct'] < 60:
        tips.append(f"Add these missing keywords naturally into your resume: **{', '.join(results['missing_keywords'][:8])}**")
    if results['missing_skills']:
        tips.append(f"Consider adding these skills if you have them: **{', '.join(results['missing_skills'][:6])}**")
    if 'summary' not in results['found_sections']:
        tips.append("Add a **professional summary** section at the top of your resume.")
    if 'projects' not in results['found_sections']:
        tips.append("Add a **Projects** section to demonstrate hands-on experience.")
    if results['cos_sim_pct'] < 50:
        tips.append("Your resume language is quite different from the JD — try mirroring the JD's phrasing where authentic.")
    if not tips:
        tips.append("Your resume is well-optimized for this job description. Great work!")

    for tip in tips:
        st.markdown(f"- {tip}")

    st.markdown("<br/><br/>", unsafe_allow_html=True)

elif not (resume_file and job_file):
    st.markdown("""
    <div style='text-align:center; padding:3rem; color:#94a3b8;'>
        <div style='font-size:3rem;'>☝️</div>
        <p style='font-size:1rem;'>Upload both PDFs above and click <strong>Analyze Resume</strong>.</p>
    </div>
    """, unsafe_allow_html=True)
