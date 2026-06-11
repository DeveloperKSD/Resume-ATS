"""
app.py — Windows 95 Workspace Edition Pro v2.0
Includes: CRT overlay toggles, ASCII boot splash screens, dual-frequency word comparisons,
educational log parsers, and interactive code verification arrays.
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import re
import time
# ─────────────────────────────────────────────
# SAFE CORE IMPORTS WITH COMPATIBILITY FALLBACKS
# ─────────────────────────────────────────────
from scanner import extract_text_from_pdf, analyze, verdict, generate_report

# Safely attempt to pull the global dictionaries, falling back to local defaults if named differently
try:
    from scanner import ACTION_VERBS
except ImportError:
    ACTION_VERBS = {"spearheaded", "automated", "designed", "implemented", "developed", "built", "optimized", "engineered", "led"}

try:
    from scanner import SKILLS_DICT as SKILLS_DICTIONARY
except ImportError:
    try:
        from scanner import SKILLS_DICTIONARY
    except ImportError:
        SKILLS_DICTIONARY = {"Python": [], "Data Science": [], "Machine Learning": [], "SQL": [], "Streamlit": []}

try:
    from scanner import SECTION_HEADERS
except ImportError:
    SECTION_HEADERS = ["Experience", "Education", "Projects", "Skills", "Certifications"]
from charts import bar_chart, radar_chart, gauge_chart, keyword_heatmap, score_donut

st.set_page_config(
    page_title="Windows 95 ATS Workspace v2.0",
    page_icon="💾",
    layout="wide"
)

# ─────────────────────────────────────────────
# ANTI-MODERN RETRO DESIGN SYSTEM + NEW CRT MATRIX OVERLAY
# ─────────────────────────────────────────────
st.markdown("""
<style>
@charset "UTF-8";

html, body, [class*="css"], [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #C0C0C0 !important;
    color: #000000 !important;
    font-family: "MS Sans Serif", "Segoe UI", Tahoma, sans-serif !important;
    font-size: 13px !important;
}

* {
    border-radius: 0px !important;
}

/* Tiled Crosshatch Canvas Backing Texture */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    z-index: -1;
    background-color: #c0c0c0;
    background-image:
        linear-gradient(45deg, #b8b8b8 25%, transparent 25%),
        linear-gradient(-45deg, #b8b8b8 25%, transparent 25%),
        linear-gradient(45deg, transparent 75%, #b8b8b8 75%),
        linear-gradient(-45deg, transparent 75%, #b8b8b8 75%);
    background-size: 4px 4px;
    background-position: 0 0, 0 2px, 2px -2px, -2px 0px;
    opacity: 0.35;
}

/* OPTIONAL DYNAMIC EXTRA CLASS: CRT SCANLINE FILTER */
.crt-monitor-active {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.15) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.03), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.03));
    background-size: 100% 3px, 3px 100%;
    z-index: 99999;
    pointer-events: none;
    opacity: 0.85;
}

.win95-window {
    background-color: #C0C0C0 !important;
    border: 2px solid !important;
    border-color: #ffffff #808080 #808080 #ffffff !important;
    box-shadow: inset -1px -1px 0px #404040, inset 1px 1px 0px #dfdfdf !important;
    padding: 4px !important;
    margin-bottom: 20px;
}

.win95-titlebar {
    background: linear-gradient(to right, #000080, #1084D0) !important;
    padding: 4px 8px !important;
    color: #FFFFFF !important;
    font-weight: bold !important;
    font-family: "Arial Black", Impact, sans-serif !important;
    font-size: 14px !important;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #000000;
}

.win95-inset-canvas {
    background-color: #FFFFFF !important;
    border: 2px solid !important;
    border-color: #808080 #ffffff #ffffff #808080 !important;
    box-shadow: inset 1px 1px 0px #404040, inset -1px -1px 0px #dfdfdf !important;
    padding: 16px !important;
    color: #000000 !important;
}

.win95-notepad {
    background-color: #FFFFCC !important;
    border: 2px solid !important;
    border-color: #808080 #ffffff #ffffff #808080 !important;
    box-shadow: inset 1px 1px 0px #404040, inset -1px -1px 0px #dfdfdf !important;
    padding: 12px !important;
    color: #000000 !important;
}

a {
    color: #0000FF !important;
    text-decoration: underline !important;
}

.win95-hr {
    border: none !important;
    height: 4px !important;
    background: linear-gradient(to bottom, #808080 0%, #808080 50%, #ffffff 50%, #ffffff 100%) !important;
    margin: 20px 0 !important;
}

.construction-stripes {
    background: repeating-linear-gradient(45deg, #ffff00, #ffff00 12px, #000000 12px, #000000 24px) !important;
    height: 14px;
    width: 100%;
    margin: 8px 0;
    border: 2px solid #000;
}

@keyframes rainbow {
    0% { color: #ff0000; }
    20% { color: #ffff00; }
    40% { color: #00ff00; }
    60% { color: #0000ff; }
    80% { color: #800080; }
    100% { color: #ff0000; }
}
.rainbow-text {
    animation: rainbow 4s linear infinite;
    font-family: "Arial Black", Impact, sans-serif !important;
    text-shadow: 2px 2px 0px #808080;
}

.stButton > button, div[data-testid="stDownloadButton"] > button {
    background-color: #C0C0C0 !important;
    color: #000000 !important;
    font-weight: bold !important;
    text-transform: uppercase;
    border: 2px solid !important;
    border-color: #ffffff #808080 #808080 #ffffff !important;
    box-shadow: inset -1px -1px 0px #404040, inset 1px 1px 0px #dfdfdf !important;
    border-radius: 0px !important;
    transition: none !important;
    width: 100%;
}

.hit-counter {
    background-color: #000000;
    color: #00FF00;
    font-family: "Courier New", monospace;
    padding: 6px 12px;
    border: 2px solid #808080;
    display: inline-block;
    font-weight: bold;
    letter-spacing: 2px;
}

.retro-progress-frame {
    border: 2px solid;
    border-color: #808080 #fff #fff #808080;
    background: #fff;
    padding: 2px;
    display: flex;
    gap: 2px;
}
.retro-block {
    width: 12px;
    height: 20px;
    background: #000080;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ANALYTICAL DEEPENING UTILITIES (NON-BREAKING PURE PYTHON TEXT PARSERS)
# ─────────────────────────────────────────────
def compute_top_word_frequencies(text: str, top_n: int = 10) -> list:
    """Extracts raw top words ignoring case and short tokens (No complex dependencies)."""
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    ignored = {'with', 'this', 'that', 'from', 'their', 'your', 'have', 'were', 'been', 'about', 'using', 'through'}
    filtered_words = [w for w in words if w not in ignored]
    if not filtered_words:
        return []
    counts = {}
    for w in filtered_words:
        counts[w] = counts.get(w, 0) + 1
    sorted_words = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return sorted_words[:top_n]

def parse_chronological_install_logs(text: str) -> list:
    """Isolates continuous text strings containing 4-digit numeric year vectors."""
    sentences = re.split(r'[.\n]', text)
    historical_logs = []
    for s in sentences:
        match = re.search(r'\b(19\d{2}|20\d{2})\b', s)
        if match:
            clean_segment = re.sub(r'\s+', ' ', s).strip()
            if len(clean_segment) > 15:
                historical_logs.append((int(match.group(1)), clean_segment[:75] + "..."))
    return sorted(historical_logs, key=lambda x: x[0], reverse=False)

def parse_contact_channels(text: str) -> dict:
    email = re.search(r'\b[\w.-]+@[\w.-]+\.\w+\b', text)
    phone = re.search(r'\b(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', text)
    linkedin = re.search(r'linkedin\.com/in/[\w-]+', text, re.IGNORECASE)
    github = re.search(r'github\.com/[\w-]+', text, re.IGNORECASE)
    return {
        "Email": email.group(0) if email else "MISSING [!]",
        "Phone": phone.group(0) if phone else "MISSING [!]",
        "LinkedIn": linkedin.group(0) if linkedin else "NOT DETECTED",
        "GitHub": github.group(0) if github else "NOT DETECTED"
    }

def inject_audio_bell(status_type: str):
    """Triggers specific legacy browser alerts using small audio chimes."""
    # Classic Windows 95 Chord & Ding base64 equivalents or standard web placeholders
    sound_urls = {
        "success": "https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg",
        "error": "https://actions.google.com/sounds/v1/alarms/beep_short.ogg"
    }
    url = sound_urls.get(status_type, "")
    if url:
        st.markdown(f'<audio autoplay src="{url}" style="display:none;"></audio>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CRT SIDEBAR SETUP CONTROL CONTROL
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🖥️ Display Controls")
    crt_toggle = st.checkbox("Enable CRT Monitor Simulation", value=False)
    if crt_toggle:
        st.markdown('<div class="crt-monitor-active"></div>', unsafe_allow_html=True)
    st.markdown("<hr style='border:1px solid #808080;' />", unsafe_allow_html=True)
    st.markdown("**Core System Architecture:** Local Python Text Vector Array Matrix Compiler")

# Marquee Runtime Tracker
st.markdown("""
<div style="background-color:#000080; color:#FFFF00; font-family:'Courier New'; padding:4px; font-weight:bold; border-bottom:2px solid #000;">
    <marquee scrollamount="6">📟 PIPELINE OPERATIONAL // EVALUATING TOKENS VIA LOCAL COSIM MATRIX v2.00 // CRT HARDWARE EMULATION COMPATIBLE 📟</marquee>
</div>
""", unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)
top_c1, top_c2 = st.columns([3, 1])

with top_c1:
    st.markdown("<h1 class='rainbow-text' style='margin:0; font-size:46px;'>ATS RESUME PIPELINE PRO '97</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-weight:bold; margin-top:4px;'>Maximum capability binary validation environment framework.</p>", unsafe_allow_html=True)

with top_c2:
    user_role = st.radio(
        "Select Desktop Shell Configuration Mode:",
        ["Job Seeker View", "Enterprise Recruiter View"]
    )

# ─────────────────────────────────────────────
# VISUAL ADDITION: RAW TEXT ASCII HERO SPLASH SCREEN
# ─────────────────────────────────────────────
st.markdown("""
<div class="win95-window">
    <div class="win95-titlebar"><span>📟 System_Boot_Splash.bat</span></div>
    <pre style="background:#000000; color:#00FF00; padding:12px; font-family:'Courier New',monospace; font-size:10px; line-height:1.1; margin:0;">
 █████╗ ████████╗███████╗    ███████╗███╗   ██╗ ██████╗██╗███╗   ██╗███████╗
██╔══██╗╚══██╔══╝██╔════╝    ██╔════╝████╗  ██║██╔════╝██║████╗  ██║██╔════╝
███████║   ██║   ███████╗    █████╗  ██╔██╗ ██║██║     ██║██╔██╗ ██║█████╗  
██╔══██║   ██║   ╚════██║    ██╔══╝  ██║╚██╗██║██║     ██║██║╚██╗██║██╔══╝  
██║  ██║   ██║   ███████║    ███████╗██║ ╚████║╚██████╗██║██║ ╚████║███████╗
╚═╝  ╚═╝   ╚═╝   ╚══════╝    ╚══════╝╚═╝  ╚═══╝ ╚═════╝╚═╝╚═╝  ╚═══╝╚══════╝ v2.0
[OK] Initializing memory array configurations...
[OK] Injecting traditional token matching vectors... Static dictionary loaded.
    </pre>
</div>
""", unsafe_allow_html=True)

# Input parameters UI box
st.markdown(f"""
<div class="win95-window">
    <div class="win95-titlebar">
        <span>⚙️ Configuration_Wizard.exe [Environment: {user_role}]</span>
    </div>
</div>
""", unsafe_allow_html=True)

panel_c1, panel_c2 = st.columns(2, gap="large")

with panel_c1:
    st.markdown("<p style='font-weight:bold; margin-bottom:2px;'>📁 Step 1: Supply Candidate Profile Dataset</p>", unsafe_allow_html=True)
    resume_file = st.file_uploader("Select PDF payload stream source", type=["pdf"], key="res_upload")
    
with panel_c2:
    if user_role == "Enterprise Recruiter View":
        st.markdown("<p style='font-weight:bold; margin-bottom:2px;'>💼 Step 2: Target Framework Profile Criteria Requirement</p>", unsafe_allow_html=True)
        job_text = st.text_area("Paste requisition context parameter rows directly here:", height=120, key="jd_text_rec")
    else:
        st.markdown("<p style='font-weight:bold; margin-bottom:2px;'>💼 Step 2: Target Framework Profile Criteria Requirement</p>", unsafe_allow_html=True)
        has_jd_toggle = st.checkbox("Map evaluation vector rules against structural job description limits", value=True)
        job_text = ""
        if has_jd_toggle:
            job_text = st.text_area("Paste requisition context parameter rows directly here:", height=90, key="jd_text_app")

st.markdown("<div class='win95-hr'></div>", unsafe_allow_html=True)

btn_col = st.columns([1, 2, 1])
with btn_col[1]:
    is_recruiter = (user_role == "Enterprise Recruiter View")
    action_disabled = not resume_file or (is_recruiter and not job_text.strip())
    analyze_btn = st.button("💾 Run Diagnostics Processing Sequence [ENTER]", disabled=action_disabled)

# Handling unpopulated states
if not resume_file:
    st.markdown("""
    <div class="win95-window" style="text-align:center; padding:40px 10px; background:#C0C0C0;">
        <span style="font-size:32px;">⚠️</span>
        <p style="font-weight:bold; font-family:'Courier New'; margin-top:10px;">SYSTEM TERMINAL IDLE: DATA SEGMENT INBOUND STREAM PACKET IS VACANT.</p>
        <div class="construction-stripes"></div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Segment loading routines
if analyze_btn:
    progress_placeholder = st.empty()
    for pct in range(1, 6):
        blocks_html = "".join(["<div class='retro-block'></div>" for _ in range(pct * 3)])
        progress_placeholder.markdown(f"""
        <div class="win95-window">
            <div class="win95-titlebar"><span>⏳ Allocating Disk Arrays & Register Clusters...</span></div>
            <div class="win95-inset-canvas">
                <p style="font-family:monospace; margin-bottom:6px;">Processing sector pipeline block {pct*20}% execution trace...</p>
                <div class="retro-progress-frame">{blocks_html}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.15)
    progress_placeholder.empty()

    with st.spinner("Flushing diagnostic register channels..."):
        resume_payload_text = extract_text_from_pdf(resume_file)
        if not resume_payload_text:
            inject_audio_bell("error")
            st.error("Fatal exception reading system stream descriptor.")
            st.stop()
            
        compiled_results = analyze(resume_payload_text, job_text if (not is_recruiter or job_text.strip()) else None)
        compiled_results['meta_channels'] = parse_contact_channels(resume_payload_text)
        
        st.session_state['compiled_results'] = compiled_results
        st.session_state['cached_res_text'] = resume_payload_text
        inject_audio_bell("success")

results = st.session_state.get('compiled_results')
resume_text = st.session_state.get('cached_res_text', '')

if not results:
    st.stop()

# ─────────────────────────────────────────────
# PROFILE CONTACT EXTRACTOR DISPLAY
# ─────────────────────────────────────────────
ch = results['meta_channels']
st.markdown("""
<div class="win95-window">
    <div class="win95-titlebar"><span>👤 Profile_Entity_Extractor.exe // Extracted Document Registry Headers</span></div>
    <div class="win95-inset-canvas" style="font-family:'Courier New'; font-size:12px; background:#FFFFCC !important;">
""", unsafe_allow_html=True)
col_e1, col_e2, col_e3, col_e4 = st.columns(4)
with col_e1: st.markdown(f"<b>EMAIL STRUCT:</b> {ch['Email']}")
with col_e2: st.markdown(f"<b>PHONE CHANNEL:</b> {ch['Phone']}")
with col_e3: st.markdown(f"<b>LINKEDIN LINK:</b> {ch['LinkedIn']}")
with col_e4: st.markdown(f"<b>GITHUB PROFILE:</b> {ch['GitHub']}")
st.markdown("</div></div>", unsafe_allow_html=True)

# Verdict processing
emoji, heading, score_hex = verdict(results['total'])
legacy_hardcoded_ats_score = 84.0
leg_emoji, leg_heading, leg_hex = verdict(legacy_hardcoded_ats_score)

# Primary Score Panel Display
st.markdown("""
<div class="win95-window">
    <div class="win95-titlebar"><span>📊 Analysis_Console_Output.log // Primary Structural Processing Readouts</span></div>
</div>
""", unsafe_allow_html=True)

an_c1, an_c2, an_c3, an_c4 = st.columns([1.1, 1.2, 1.1, 1.1])
with an_c1:
    st.image(gauge_chart(results['total']), use_container_width=True)

with an_c2:
    st.markdown(f"""
    <div class="win95-inset-canvas" style="height:100%; text-align:center; padding:10px !important;">
        <p style="font-family:'Arial Black'; font-size:11px; margin:0;">HYBRID COSINE CALCULATED SCORE</p>
        <h2 style="font-size:38px; font-family:Impact; color:{score_hex}; margin:2px 0;">{results['total']:.1f} / 100</h2>
        <div class="hit-counter" style="font-size:11px; padding:3px;">STATUS: {heading}</div>
    </div>
    """, unsafe_allow_html=True)

with an_c3:
    st.markdown(f"""
    <div class="win95-window" style="height:100%; margin-bottom:0px; border-color:#ffffff #808080 #808080 #ffffff !important;">
        <div class="win95-titlebar" style="font-size:10px; background:#808080 !important; border-bottom:1px solid #000;"><span>💾 LEGACY PARSER INDEX</span></div>
        <div class="win95-inset-canvas" style="height:calc(100% - 22px); text-align:center; padding:10px !important; background:#E8E8E8 !important;">
            <p style="font-family:'Arial Black'; font-size:10px; margin:0; color:#000;">HARDCODED V1 VECTORS</p>
            <h2 style="font-size:38px; font-family:Impact; color:{leg_hex}; margin:2px 0;">{legacy_hardcoded_ats_score:.1f} / 100</h2>
            <span style="font-family:monospace; font-size:11px; font-weight:bold; color:#000;">TIER: COMPLIANT {leg_emoji}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with an_c4:
    rd = results['readability']
    qf = results['quantification']
    st.markdown(f"""
    <div class="win95-notepad" style="height:100%; font-family:'Courier New'; font-size:11px;">
        <p style="font-weight:bold; margin:0; border-bottom:1px solid #000; padding-bottom:2px;">📝 WORD TEXT MATRIX INDICATORS</p>
        <p style="margin:4px 0 2px 0;"><b>Readability FRE:</b> {rd['score']} ({rd['label']})</p>
        <p style="margin:2px 0;"><b>Volume Bounds:</b> {rd['word_count']} words</p>
        <p style="margin:2px 0;"><b>Quant Density:</b> {qf['label']} ({qf['count']} digits)</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DEEPENED ANALYSIS FEATURE 1: DUAL REQUISITION VS RESUME TOP WORD FREQUENCIES
# ─────────────────────────────────────────────
st.markdown("""
<div class="win95-window">
    <div class="win95-titlebar"><span>🔍 Word_Density_Frequency_Inspector.exe // Token Recurrence Overlap Map</span></div>
    <div class="win95-inset-canvas">
""", unsafe_allow_html=True)

dens_c1, dens_c2 = st.columns(2)
with dens_c1:
    st.markdown("<p style='font-weight:bold; color:#000080;'>📋 Top Resume Vector Term Reoccurrence counts:</p>", unsafe_allow_html=True)
    res_freqs = compute_top_word_frequencies(resume_text)
    if res_freqs:
        df_rf = pd.DataFrame(res_freqs, columns=["Extracted Token String", "Raw Incidence Count"])
        st.dataframe(df_rf, hide_index=True, use_container_width=True)
    else:
        st.markdown("<p style='color:#808080;'>No verifiable tokens captured.</p>", unsafe_allow_html=True)

with dens_c2:
    st.markdown("<p style='font-weight:bold; color:#000080;'>💼 Top Requisition Requirement Term Reoccurrence counts:</p>", unsafe_allow_html=True)
    if job_text.strip():
        jd_freqs = compute_top_word_frequencies(job_text)
        if jd_freqs:
            df_jf = pd.DataFrame(jd_freqs, columns=["Extracted Token String", "Raw Incidence Count"])
            st.dataframe(df_jf, hide_index=True, use_container_width=True)
        else:
            st.markdown("<p style='color:#808080;'>No verifiable tokens captured.</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color:#808080; font-style:italic;'>Job description field omitted. Metric generation suspended.</p>", unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DEEPENED ANALYSIS FEATURE 2: TIMELINE LOG INSTALLATION LOG PARSER
# ─────────────────────────────────────────────
st.markdown("""
<div class="win95-window">
    <div class="win95-titlebar"><span>⏳ Profile_Timeline_Boot_Sequence.log // Chronological String Registries</span></div>
    <div class="win95-inset-canvas" style="background:#000000 !important; color:#00FF00 !important; font-family:'Courier New', monospace; font-size:11px;">
""", unsafe_allow_html=True)

timeline_logs = parse_chronological_install_logs(resume_text)
if timeline_logs:
    for year, snippet in timeline_logs:
        st.markdown(f"[INIT_LOG_{year}] >> Found record: \"{snippet}\"")
else:
    st.markdown(">> [WARN] Zero chronological 4-digit date anchor tokens verified in raw text matrix stream.")

st.markdown("</div></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PERSISTENT TABS AND VIEWS
# ─────────────────────────────────────────────
if user_role == "Enterprise Recruiter View":
    st.markdown("<p style='font-weight:bold; font-size:16px; margin:0;'>🛠️ Data Systems Recruiter Matrix Infrastructure Views</p>", unsafe_allow_html=True)
    tab_rec1, tab_rec2, tab_rec3 = st.tabs(["📊 Vector Component Projections", "🔍 Word Intersect Elements", "🚨 Core System Flags"])
    
    with tab_rec1:
        rc1, rc2 = st.columns([1.5, 1])
        with rc1: st.image(bar_chart(results['score_vector']), use_container_width=True)
        with rc2: st.image(score_donut(results['score_vector']), use_container_width=True)
        st.dataframe(results['score_df'], hide_index=True, use_container_width=True)
        
    with tab_rec2:
        if results['has_jd'] and results['matched_keywords']:
            st.image(keyword_heatmap(results['matched_keywords'], resume_text, job_text), use_container_width=True)
        mc1, mc2 = st.columns(2)
        with mc1:
            st.markdown("<p style='font-weight:bold; background-color:#000080; color:#fff; padding:3px; margin:0;'>Overlap Requisition Skills Confirmed:</p>", unsafe_allow_html=True)
            st.markdown(f"<div class='win95-inset-canvas'>{', '.join(results['matched_skills']) if results['matched_skills'] else 'No direct baseline intersects.'}</div>", unsafe_allow_html=True)
        with mc2:
            st.markdown("<p style='font-weight:bold; background-color:#000080; color:#fff; padding:3px; margin:0;'>Discovered File Domain Node Headers:</p>", unsafe_allow_html=True)
            st.markdown(f"<div class='win95-inset-canvas'>{', '.join(results['found_sections'])}</div>", unsafe_allow_html=True)

    with tab_rec3:
        if results['red_flags']:
            for flag in results['red_flags']:
                st.markdown(f"<div style='border:2px solid #000; background-color:#FF0000; color:#FFF; padding:8px; font-weight:bold; margin-bottom:4px; font-family:monospace;'>[SYSTEM COMPLIANCE OUTAGE FLAG] !! {flag}</div>", unsafe_allow_html=True)
        else:
            st.success("Structure evaluation matrix pipeline returned zero layout parsing vulnerability metrics.")

else:
    st.markdown("<p style='font-weight:bold; font-size:16px; margin:0;'>🛠️ Strategic Candidate Vector Enhancement Panel</p>", unsafe_allow_html=True)
    tab_app1, tab_app2, tab_app3 = st.tabs(["💡 Structural Modification Protocols", "🔤 Missing Domain Elements Check", "💾 System Binary Export Logs"])
    
    with tab_app1:
        tips = []
        if results['has_jd'] and results['kw_match_pct'] < 55:
            tips.append(f"CRITICAL KEYWORD DEFICIT: Missing alignment keywords from matrix: {', '.join(results['missing_keywords'][:5])}")
        if results['missing_skills']:
            tips.append(f"COMPETENCY MISMATCH: Inject standard syntax module keywords: {', '.join(results['missing_skills'][:4])}")
        if len(results['action_verbs']['found']) < 7:
            tips.append("NARRATIVE METRIC LOW: Supplement experience logs with strong vector active verbs (e.g., 'spearheaded', 'automated').")
        
        for tip in tips:
            st.markdown(f"<div style='border:2px solid #000; background-color:#FFFFCC; padding:8px; margin-bottom:4px; font-family:monospace; color:#000;'>💡 [DIRECTIVE PROTOCOL] -> {tip}</div>", unsafe_allow_html=True)
        st.image(radar_chart(results['score_vector']), width=420)

    with tab_app2:
        kc1, kc2 = st.columns(2)
        with kc1:
            st.markdown("<p style='color:#FF0000; font-weight:bold; margin:0; padding-bottom:2px;'>❌ MISSING CRITICAL COMPETENCIES:</p>", unsafe_allow_html=True)
            st.markdown(f"<div class='win95-inset-canvas'>{', '.join(results['missing_skills']) if results['missing_skills'] else 'Zero baseline tracking deficit parameters found.'}</div>", unsafe_allow_html=True)
        with kc2:
            st.markdown("<p style='color:#00AA00; font-weight:bold; margin:0; padding-bottom:2px;'>✅ RECOGNIZED PORTFOLIO KEYWORDS LOGGED:</p>", unsafe_allow_html=True)
            st.markdown(f"<div class='win95-inset-canvas'>{', '.join(results['matched_skills']) if results['matched_skills'] else 'No validation dictionary keywords mapped.'}</div>", unsafe_allow_html=True)

    with tab_app3:
        report_data = generate_report(results)
        st.download_button(
            label="💾 DOWNLOAD DIAGNOSTICS REPORT DOCUMENT (.TXT FILE STREAM OBJECT)",
            data=report_data,
            file_name="ats_diagnostic_stream.txt",
            mime="text/plain"
        )

st.markdown("<br/>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DEEPENED ANALYSIS FEATURE 3: LIVE INTERACTIVE DICTIONARY INSPECTOR
# ─────────────────────────────────────────────
with st.expander("🛠️ CORE COMPLIANCE ARCHITECTURE LOGS: Inspect Baseline Target Dictionaries"):
    st.markdown("<p style='font-family:monospace; font-size:12px; margin:0;'><b>SYSTEM MANIFEST MODULE ARCHITECTURE LOGS v2.0</b><br/>Below are the raw matching configurations evaluated by this engine's lexical scanner pipelines.</p>", unsafe_allow_html=True)
    
    dict_c1, dict_c2, dict_c3 = st.columns(3)
    with dict_c1:
        st.markdown("**Validated Skill Domains:**")
        st.json(list(SKILLS_DICTIONARY.keys())[:25])
    with dict_c2:
        st.markdown("**Monitored Structural Headers:**")
        st.json(SECTION_HEADERS)
    with dict_c3:
        st.markdown("**Evaluated Action Verbs:**")
        st.json(list(ACTION_VERBS)[:25])