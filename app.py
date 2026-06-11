"""
app.py — ATS Resume Scanner  |  Enhanced Edition
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
from scanner import (
    extract_text_from_pdf, analyze, verdict, generate_report
)
from charts import bar_chart, radar_chart, gauge_chart, keyword_heatmap, score_donut


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
# DESIGN SYSTEM
# ─────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: #070b14;
    color: #cbd5e1;
}

.block-container { padding: 1.5rem 2.5rem; max-width: 1280px; }

/* ── Animated gradient hero background ── */
.hero-bg {
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, #6366f120 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 100%, #8b5cf615 0%, transparent 60%),
        #070b14;
    z-index: -1; pointer-events: none;
}

/* ── Glass card ── */
.glass {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
}

.glass-bright {
    background: rgba(99,102,241,0.06);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 16px;
}

/* ── Score pill ── */
.score-pill {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 100px;
    padding: 6px 18px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.9rem; font-weight: 700;
    color: #a5b4fc;
}

/* ── Stat cards ── */
.stat-row { display: flex; gap: 12px; margin: 1rem 0; flex-wrap: wrap; }

.stat-card {
    flex: 1; min-width: 130px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 14px 16px;
    text-align: center;
}
.stat-card .stat-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.7rem; font-weight: 700; line-height: 1;
    margin-bottom: 4px;
}
.stat-card .stat-lbl {
    font-size: 0.72rem; color: #64748b; letter-spacing: 0.06em;
    text-transform: uppercase; font-weight: 600;
}

/* ── Section eyebrow ── */
.eyebrow {
    font-size: 0.68rem; font-weight: 700;
    letter-spacing: 0.14em; text-transform: uppercase;
    color: #6366f1; margin-bottom: 0.5rem;
}

/* ── Tags ── */
.tag-wrap { display: flex; flex-wrap: wrap; gap: 6px; margin: 6px 0; }
.tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem; font-weight: 500;
    padding: 3px 10px; border-radius: 6px;
    border: 1px solid rgba(255,255,255,0.1);
    color: #94a3b8; background: rgba(255,255,255,0.03);
    white-space: nowrap;
}
.tag-green { color: #4ade80; background: rgba(74,222,128,0.08); border-color: rgba(74,222,128,0.25); }
.tag-red   { color: #f87171; background: rgba(248,113,113,0.08); border-color: rgba(248,113,113,0.25); }
.tag-blue  { color: #60a5fa; background: rgba(96,165,250,0.08); border-color: rgba(96,165,250,0.25); }
.tag-purple{ color: #c084fc; background: rgba(192,132,252,0.08); border-color: rgba(192,132,252,0.25); }

/* ── Progress bar ── */
.progress-wrap { margin: 4px 0 10px 0; }
.progress-bar-bg {
    background: rgba(255,255,255,0.06); border-radius: 100px;
    height: 6px; overflow: hidden;
}
.progress-bar-fill {
    height: 6px; border-radius: 100px;
    transition: width 0.8s ease;
}

/* ── Flag / tip items ── */
.flag-item {
    display: flex; align-items: flex-start; gap: 10px;
    padding: 10px 14px; margin-bottom: 8px;
    background: rgba(239,68,68,0.06);
    border: 1px solid rgba(239,68,68,0.2);
    border-radius: 10px; font-size: 0.85rem;
    color: #fca5a5;
}
.tip-item {
    display: flex; align-items: flex-start; gap: 10px;
    padding: 10px 14px; margin-bottom: 8px;
    background: rgba(99,102,241,0.06);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 10px; font-size: 0.85rem;
    color: #c7d2fe;
}
.ok-item {
    display: flex; align-items: flex-start; gap: 10px;
    padding: 10px 14px; margin-bottom: 8px;
    background: rgba(74,222,128,0.06);
    border: 1px solid rgba(74,222,128,0.2);
    border-radius: 10px; font-size: 0.85rem;
    color: #86efac;
}

/* ── Divider ── */
.div { border-bottom: 1px solid rgba(255,255,255,0.07); margin: 1.5rem 0; }

/* ── Upload zone ── */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1.5px dashed rgba(99,102,241,0.3) !important;
    border-radius: 12px !important;
    transition: border-color 0.2s;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(99,102,241,0.6) !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: white; border: none; border-radius: 10px;
    padding: 0.65rem 2.5rem;
    font-family: 'Inter', sans-serif;
    font-weight: 700; font-size: 0.95rem;
    letter-spacing: 0.03em; width: 100%;
    transition: all 0.2s; box-shadow: 0 0 20px rgba(99,102,241,0.3);
}
.stButton > button:hover {
    box-shadow: 0 0 35px rgba(99,102,241,0.5);
    transform: translateY(-1px);
}
.stButton > button:disabled { opacity: 0.4; box-shadow: none; transform: none; }

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] { gap: 4px; border-bottom: 1px solid rgba(255,255,255,0.07); }
[data-testid="stTabs"] [role="tab"] {
    font-family: 'Inter', sans-serif; font-weight: 600;
    font-size: 0.82rem; letter-spacing: 0.04em;
    color: #64748b; padding: 8px 18px; border-radius: 8px 8px 0 0;
    border: none; background: transparent;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #a5b4fc; border-bottom: 2px solid #6366f1;
    background: rgba(99,102,241,0.06);
}

/* ── DataFrame ── */
[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.02) !important;
    border-radius: 10px; border: 1px solid rgba(255,255,255,0.06);
}

/* ── Spinner ── */
[data-testid="stSpinner"] p { color: #6366f1 !important; font-size: 0.9rem; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.35); border-radius: 10px; }

/* ── Metric overrides ── */
[data-testid="metric-container"] { background: transparent !important; }
</style>

<div class="hero-bg"></div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────

st.markdown("""
<div style='padding: 2.5rem 0 1.2rem 0;'>
  <div style='display:flex; align-items:center; gap:14px; margin-bottom:8px;'>
    <span style='font-size:2rem;'>📄</span>
    <h1 style='font-size:2.2rem; font-weight:800; letter-spacing:-0.03em; margin:0;
               background: linear-gradient(135deg, #e2e8f0 30%, #6366f1);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
      ATS Resume Scanner
    </h1>
  </div>
  <p style='color:#475569; font-size:0.95rem; margin:0; max-width:600px;'>
    Deep-scan your resume against any job description — keyword gaps, skill alignment,
    readability, action verbs, ATS red flags, and more.
  </p>
</div>
<div class='div'></div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# UPLOAD PANEL
# ─────────────────────────────────────────────

uc1, uc2, uc3 = st.columns([1.1, 1.1, 0.8], gap="large")

with uc1:
    st.markdown('<p class="eyebrow">📋 Your Resume</p>', unsafe_allow_html=True)
    resume_file = st.file_uploader("Resume PDF", type=["pdf"], key="resume",
                                   label_visibility="collapsed")
    if resume_file:
        st.markdown(f'<p style="color:#4ade80;font-size:0.78rem;margin-top:4px;">✓ {resume_file.name}</p>',
                    unsafe_allow_html=True)

with uc2:
    st.markdown('<p class="eyebrow">💼 Job Description</p>', unsafe_allow_html=True)
    job_file = st.file_uploader("Job Description PDF", type=["pdf"], key="job",
                                label_visibility="collapsed")
    if job_file:
        st.markdown(f'<p style="color:#4ade80;font-size:0.78rem;margin-top:4px;">✓ {job_file.name}</p>',
                    unsafe_allow_html=True)

with uc3:
    st.markdown('<p class="eyebrow" style="visibility:hidden;">action</p>', unsafe_allow_html=True)
    analyze_btn = st.button("🔍 Analyze Resume",
                            disabled=not (resume_file and job_file))

st.markdown("<div class='div'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# EMPTY STATE
# ─────────────────────────────────────────────

if not (resume_file and job_file):
    st.markdown("""
    <div style='text-align:center; padding:4rem 0; color:#1e293b;'>
      <div style='font-size:4rem; margin-bottom:1rem; filter: grayscale(0.3);'>☝️</div>
      <p style='font-size:1rem; color:#334155;'>
        Upload both PDFs above, then click <strong style="color:#6366f1;">Analyze Resume</strong>.
      </p>
      <div style='display:flex; justify-content:center; gap:2rem; margin-top:2rem;
                  flex-wrap:wrap; color:#1e293b; font-size:0.8rem;'>
        <span>📊 Keyword & Phrase Matching</span>
        <span>🛠 Tech Skill Gap Analysis</span>
        <span>🧠 Readability Score</span>
        <span>⚡ Action Verb Detection</span>
        <span>🚩 ATS Red Flag Scanner</span>
        <span>📥 Downloadable Report</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ─────────────────────────────────────────────
# ANALYSIS
# ─────────────────────────────────────────────

if analyze_btn and resume_file and job_file:
    with st.spinner("Deep-scanning your resume..."):
        resume_text = extract_text_from_pdf(resume_file)
        job_text    = extract_text_from_pdf(job_file)

        if not resume_text:
            st.error("⚠️ Could not extract text from Resume PDF. Ensure it's not a scanned image.")
            st.stop()
        if not job_text:
            st.error("⚠️ Could not extract text from Job Description PDF.")
            st.stop()

        results = analyze(resume_text, job_text)
        st.session_state['results']     = results
        st.session_state['resume_text'] = resume_text
        st.session_state['job_text']    = job_text

# Use cached results between reruns
results     = st.session_state.get('results')
resume_text = st.session_state.get('resume_text', '')
job_text    = st.session_state.get('job_text', '')

if not results:
    st.stop()


# ─────────────────────────────────────────────
# HERO SCORE ROW
# ─────────────────────────────────────────────

emoji, label, score_color = verdict(results['total'])

h1, h2, h3, h4 = st.columns([1.1, 1, 1, 1], gap="medium")

with h1:
    st.image(gauge_chart(results['total']), use_column_width=True)

with h2:
    st.markdown(f"""
    <div class="glass" style="padding:1.5rem; height:100%; box-sizing:border-box;">
      <div class="eyebrow">Verdict</div>
      <div style="font-size:2.8rem; margin:4px 0;">{emoji}</div>
      <div style="font-family:'JetBrains Mono',monospace; font-size:2.6rem;
                  font-weight:800; color:{score_color}; line-height:1;">
        {results['total']:.0f}
        <span style="font-size:1rem; color:#475569; font-weight:400;">/100</span>
      </div>
      <div style="font-weight:700; color:{score_color}; margin-top:6px;">{label}</div>
    </div>
    """, unsafe_allow_html=True)

with h3:
    rd = results['readability']
    st.markdown(f"""
    <div class="glass" style="padding:1.5rem; height:100%;">
      <div class="eyebrow">Readability</div>
      <div style="font-family:'JetBrains Mono',monospace; font-size:2.2rem;
                  font-weight:700; color:#60a5fa; line-height:1;">{rd['score']}</div>
      <div style="font-size:0.78rem; color:#60a5fa; margin:4px 0 8px 0;">{rd['label']}</div>
      <div style="font-size:0.75rem; color:#475569;">
        {rd['word_count']} words · {rd['sentence_count']} sentences<br/>
        Avg {rd['avg_sentence_len']} words/sentence
      </div>
    </div>
    """, unsafe_allow_html=True)

with h4:
    qf = results['quantification']
    av = results['action_verbs']
    st.markdown(f"""
    <div class="glass" style="padding:1.5rem; height:100%;">
      <div class="eyebrow">Impact Signals</div>
      <div style="display:flex; flex-direction:column; gap:8px; margin-top:6px;">
        <div>
          <div style="font-size:0.72rem; color:#64748b; text-transform:uppercase; letter-spacing:.06em;">Quantification</div>
          <div style="font-family:'JetBrains Mono',monospace; font-weight:700; font-size:1.2rem;
                      color:{'#4ade80' if qf['score']>=60 else '#facc15' if qf['score']>=30 else '#f87171'};">
            {qf['label']}
          </div>
          <div style="font-size:0.72rem; color:#475569;">{qf['count']} numbers · {qf['percents']} percentages</div>
        </div>
        <div>
          <div style="font-size:0.72rem; color:#64748b; text-transform:uppercase; letter-spacing:.06em;">Action Verbs</div>
          <div style="font-family:'JetBrains Mono',monospace; font-weight:700; font-size:1.2rem; color:#c084fc;">
            {len(av['found'])}
          </div>
          <div style="font-size:0.72rem; color:#475569;">verbs detected</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='div'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STAT STRIP
# ─────────────────────────────────────────────

def _pct_color(pct):
    if pct >= 70: return "#4ade80"
    if pct >= 45: return "#facc15"
    return "#f87171"

stats = [
    ("Keyword Hit",   f"{results['kw_match_pct']}%",    _pct_color(results['kw_match_pct'])),
    ("Skill Match",   f"{results['skill_match_pct']}%", _pct_color(results['skill_match_pct'])),
    ("Cosine Sim",    f"{results['cos_sim_pct']}%",     _pct_color(results['cos_sim_pct'])),
    ("TF-IDF Sim",    f"{results['tfidf_sim_pct']}%",   _pct_color(results['tfidf_sim_pct'])),
    ("Sections",      f"{len(results['found_sections'])}/{len(['experience','education','skills','contact','summary','projects','certifications'])}", "#a5b4fc"),
    ("Phrases Hit",   str(len(results['matched_phrases'])),  "#60a5fa"),
    ("Red Flags",     str(len(results['red_flags'])),        "#f87171" if results['red_flags'] else "#4ade80"),
]

cols = st.columns(len(stats), gap="small")
for col, (lbl, val, color) in zip(cols, stats):
    col.markdown(f"""
    <div class="stat-card">
      <div class="stat-val" style="color:{color};">{val}</div>
      <div class="stat-lbl">{lbl}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='div'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊  Charts & Scores",
    "🔤  Keywords & Skills",
    "💡  Phrases & Tips",
    "⚡  Resume Quality",
    "📥  Export",
])


# ────────── TAB 1: Charts ──────────────────────
with tab1:
    c1, c2 = st.columns([1.6, 1], gap="large")
    with c1:
        st.markdown('<p class="eyebrow">Score Breakdown</p>', unsafe_allow_html=True)
        st.image(bar_chart(results['score_vector']), use_column_width=True)

    with c2:
        st.markdown('<p class="eyebrow">Score Composition</p>', unsafe_allow_html=True)
        st.image(score_donut(results['score_vector']), use_column_width=True)

    st.markdown("<div class='div'></div>", unsafe_allow_html=True)

    c3, c4 = st.columns([1, 1.2], gap="large")
    with c3:
        st.markdown('<p class="eyebrow">Radar</p>', unsafe_allow_html=True)
        st.image(radar_chart(results['score_vector']), use_column_width=True)

    with c4:
        st.markdown('<p class="eyebrow">Detailed Score Table</p>', unsafe_allow_html=True)
        df = results['score_df'].copy()
        df['Score'] = df['Score'].map(lambda x: f"{x:.1f}")
        df['Max']   = df['Max'].map(str)
        df['%']     = df['Percentage'].map(lambda x: f"{x:.0f}%")
        st.dataframe(df[['Component', 'Score', 'Max', '%']],
                     hide_index=True, use_container_width=True)

        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown('<p class="eyebrow">Resume Sections</p>', unsafe_allow_html=True)
        all_sections = ['experience','education','skills','contact','summary','projects','certifications']
        tags_html = '<div class="tag-wrap">'
        for s in all_sections:
            if s in results['found_sections']:
                tags_html += f'<span class="tag tag-green">✓ {s}</span>'
            else:
                tags_html += f'<span class="tag tag-red">✗ {s}</span>'
        tags_html += '</div>'
        st.markdown(tags_html, unsafe_allow_html=True)


# ────────── TAB 2: Keywords & Skills ──────────
with tab2:
    k1, k2 = st.columns(2, gap="large")

    with k1:
        st.markdown('<p class="eyebrow">🟢 Matched Keywords</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:#64748b; font-size:0.8rem;">{len(results["matched_keywords"])} matched</p>',
                    unsafe_allow_html=True)
        if results['matched_keywords']:
            tags = '<div class="tag-wrap">' + \
                   "".join(f'<span class="tag tag-green">{k}</span>'
                           for k in results['matched_keywords'][:50]) + '</div>'
            st.markdown(tags, unsafe_allow_html=True)
        else:
            st.markdown("_None found._")

        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown('<p class="eyebrow">🔴 Missing Keywords</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:#64748b; font-size:0.8rem;">{len(results["missing_keywords"])} missing</p>',
                    unsafe_allow_html=True)
        if results['missing_keywords']:
            tags = '<div class="tag-wrap">' + \
                   "".join(f'<span class="tag tag-red">{k}</span>'
                           for k in results['missing_keywords'][:50]) + '</div>'
            st.markdown(tags, unsafe_allow_html=True)
        else:
            st.markdown("_None missing — great!_")

    with k2:
        st.markdown('<p class="eyebrow">🟢 Matched Skills</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:#64748b; font-size:0.8rem;">{len(results["matched_skills"])} matched</p>',
                    unsafe_allow_html=True)
        if results['matched_skills']:
            tags = '<div class="tag-wrap">' + \
                   "".join(f'<span class="tag tag-blue">{s}</span>'
                           for s in results['matched_skills']) + '</div>'
            st.markdown(tags, unsafe_allow_html=True)
        else:
            st.markdown("_No matching tech skills._")

        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown('<p class="eyebrow">🔴 Missing Skills</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:#64748b; font-size:0.8rem;">{len(results["missing_skills"])} missing</p>',
                    unsafe_allow_html=True)
        if results['missing_skills']:
            tags = '<div class="tag-wrap">' + \
                   "".join(f'<span class="tag tag-red">{s}</span>'
                           for s in results['missing_skills']) + '</div>'
            st.markdown(tags, unsafe_allow_html=True)
        else:
            st.markdown("_No skill gaps detected._")

    st.markdown("<div class='div'></div>", unsafe_allow_html=True)

    # Keyword frequency heatmap
    if results['matched_keywords']:
        st.markdown('<p class="eyebrow">Keyword Frequency: Resume vs JD</p>', unsafe_allow_html=True)
        hm = keyword_heatmap(results['matched_keywords'], resume_text, job_text, top_n=20)
        if hm:
            st.image(hm, use_column_width=True)

    # Keyword frequency table
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown('<p class="eyebrow">Top JD Terms (TF-IDF)</p>', unsafe_allow_html=True)
    if results['top_jd_terms']:
        tags = '<div class="tag-wrap">' + \
               "".join(f'<span class="tag tag-purple">{t}</span>'
                       for t in results['top_jd_terms']) + '</div>'
        st.markdown(tags, unsafe_allow_html=True)


# ────────── TAB 3: Phrases & Tips ─────────────
with tab3:
    p1, p2 = st.columns(2, gap="large")

    with p1:
        st.markdown('<p class="eyebrow">✅ Matched Phrases</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:#64748b; font-size:0.8rem;">{len(results["matched_phrases"])} 2-word phrases in common</p>',
                    unsafe_allow_html=True)
        if results['matched_phrases']:
            tags = '<div class="tag-wrap">' + \
                   "".join(f'<span class="tag tag-green">{p}</span>'
                           for p in results['matched_phrases'][:40]) + '</div>'
            st.markdown(tags, unsafe_allow_html=True)
        else:
            st.markdown("_No matching phrases._")

    with p2:
        st.markdown('<p class="eyebrow">❌ Missing Phrases (from JD)</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:#64748b; font-size:0.8rem;">Top JD phrases not in your resume</p>',
                    unsafe_allow_html=True)
        if results['missing_phrases']:
            tags = '<div class="tag-wrap">' + \
                   "".join(f'<span class="tag tag-red">{p}</span>'
                           for p in results['missing_phrases'][:40]) + '</div>'
            st.markdown(tags, unsafe_allow_html=True)
        else:
            st.markdown("_No phrase gaps._")

    st.markdown("<div class='div'></div>", unsafe_allow_html=True)
    st.markdown('<p class="eyebrow">💡 Personalized Improvement Tips</p>', unsafe_allow_html=True)

    tips = []

    if results['kw_match_pct'] < 60:
        top_missing = ', '.join(results['missing_keywords'][:8])
        tips.append(("🔑", f"Add these high-priority keywords naturally: {top_missing}"))
    if results['missing_skills']:
        top_skills = ', '.join(results['missing_skills'][:6])
        tips.append(("🛠", f"Skills to add if applicable: {top_skills}"))
    if 'summary' not in results['found_sections']:
        tips.append(("📝", "Add a professional summary/objective at the top of your resume."))
    if 'projects' not in results['found_sections']:
        tips.append(("🗂", "Add a Projects section — critical for tech roles."))
    if results['cos_sim_pct'] < 50:
        tips.append(("🔄", "Mirror the JD's phrasing more closely where authentic to your experience."))
    if results['quantification']['score'] < 30:
        tips.append(("📈", "Add more numbers — 'improved performance by 40%', 'managed 5 engineers', etc."))
    if len(results['action_verbs']['found']) < 5:
        top_av = ', '.join(results['action_verbs']['missing'][:8])
        tips.append(("⚡", f"Strengthen with action verbs: {top_av}"))
    if results['missing_phrases']:
        top_ph = results['missing_phrases'][0] if results['missing_phrases'] else ''
        tips.append(("💬", f"Try naturally incorporating JD phrases like '{top_ph}' into bullet points."))

    if not tips:
        st.markdown("""
        <div class="ok-item">✅ Your resume is well-optimized for this job description. Great work!</div>
        """, unsafe_allow_html=True)
    else:
        for icon, tip in tips:
            st.markdown(f'<div class="tip-item"><span style="font-size:1rem;">{icon}</span><span>{tip}</span></div>',
                        unsafe_allow_html=True)


# ────────── TAB 4: Resume Quality ─────────────
with tab4:
    q1, q2 = st.columns(2, gap="large")

    with q1:
        st.markdown('<p class="eyebrow">⚡ Action Verbs Used</p>', unsafe_allow_html=True)
        av = results['action_verbs']
        if av['found']:
            tags = '<div class="tag-wrap">' + \
                   "".join(f'<span class="tag tag-green">{v}</span>' for v in av['found']) + \
                   '</div>'
            st.markdown(tags, unsafe_allow_html=True)
        else:
            st.markdown("_None detected._")

        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown('<p class="eyebrow">📈 Suggested Action Verbs to Add</p>', unsafe_allow_html=True)
        tags = '<div class="tag-wrap">' + \
               "".join(f'<span class="tag tag-red">{v}</span>' for v in av['missing'][:15]) + \
               '</div>'
        st.markdown(tags, unsafe_allow_html=True)

    with q2:
        st.markdown('<p class="eyebrow">🚩 ATS Red Flags</p>', unsafe_allow_html=True)
        if results['red_flags']:
            for flag in results['red_flags']:
                st.markdown(f'<div class="flag-item"><span>⚠</span><span>{flag}</span></div>',
                            unsafe_allow_html=True)
        else:
            st.markdown('<div class="ok-item"><span>✅</span><span>No ATS red flags detected.</span></div>',
                        unsafe_allow_html=True)

        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown('<p class="eyebrow">📊 Quantification Analysis</p>', unsafe_allow_html=True)
        qf = results['quantification']
        qf_color = "#4ade80" if qf['score'] >= 60 else "#facc15" if qf['score'] >= 30 else "#f87171"
        st.markdown(f"""
        <div class="glass" style="padding:14px 18px;">
          <div style="font-family:'JetBrains Mono',monospace; font-size:1.5rem;
                      font-weight:700; color:{qf_color};">{qf['label']}</div>
          <div style="font-size:0.78rem; color:#64748b; margin-top:4px;">
            {qf['count']} numeric values · {qf['percents']} percentages found
          </div>
          <div class="progress-wrap" style="margin-top:10px;">
            <div style="font-size:0.68rem; color:#475569; margin-bottom:4px;">Impact Score: {qf['score']}/100</div>
            <div class="progress-bar-bg">
              <div class="progress-bar-fill"
                   style="width:{qf['score']}%; background:{qf_color};"></div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)


# ────────── TAB 5: Export ─────────────────────
with tab5:
    st.markdown('<p class="eyebrow">📥 Download Your Report</p>', unsafe_allow_html=True)
    st.markdown("""
    <p style='color:#475569; font-size:0.88rem; margin-bottom:1rem;'>
      Download a plain-text report with your full ATS scan results —
      perfect for tracking applications or sharing with a career coach.
    </p>
    """, unsafe_allow_html=True)

    report_text = generate_report(results)
    st.download_button(
        label="📄 Download ATS Report (.txt)",
        data=report_text,
        file_name="ats_scan_report.txt",
        mime="text/plain",
    )

    st.markdown("<div class='div'></div>", unsafe_allow_html=True)

    # Side-by-side text comparison
    st.markdown('<p class="eyebrow">🔍 Side-by-Side Text View</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#475569; font-size:0.8rem; margin-bottom:8px;">First 1500 characters of each document</p>',
                unsafe_allow_html=True)
    t1, t2 = st.columns(2, gap="large")
    with t1:
        st.markdown('<p class="eyebrow" style="color:#4ade80;">Your Resume</p>', unsafe_allow_html=True)
        st.text_area("", value=resume_text[:1500], height=300,
                     key="rtxt", label_visibility="collapsed", disabled=True)
    with t2:
        st.markdown('<p class="eyebrow" style="color:#60a5fa;">Job Description</p>', unsafe_allow_html=True)
        st.text_area("", value=job_text[:1500], height=300,
                     key="jtxt", label_visibility="collapsed", disabled=True)

st.markdown("<br/><br/>", unsafe_allow_html=True)
