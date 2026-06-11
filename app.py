"""
app.py — 1990s Workstation Edition ATS Core 
"""

import streamlit as st
import pandas as pd
import numpy as np
from scanner import extract_text_from_pdf, analyze, verdict, generate_report
from charts import bar_chart, radar_chart, gauge_chart, keyword_heatmap, score_donut

st.set_page_config(
    page_title="Windows 95 ATS Workspace v1.97",
    page_icon="💾",
    layout="wide"
)

# ─────────────────────────────────────────────
# WINDOWS 95 RADICAL STYLE ENGINE OVERRIDE
# ─────────────────────────────────────────────
st.markdown("""
<style>
@charset "UTF-8";

/* Force system font stacks and backgrounds */
html, body, [class*="css"], [data-testid="stAppViewContainer"] {
    background-color: #C0C0C0 !important;
    color: #000000 !important;
    font-family: "MS Sans Serif", "Segoe UI", Tahoma, sans-serif !important;
    font-size: 13px !important;
}

/* ZERO OUT BORDER RADIUS EVERYWHERE */
* {
    border-radius: 0px !important;
}

/* Vintage 90s diagonal crosshatch texture */
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
    opacity: 0.4;
}

/* Classic Windows 95 Outset Bevel Container Window */
.win95-window {
    background-color: #C0C0C0 !important;
    border: 2px solid !important;
    border-color: #ffffff #808080 #808080 #ffffff !important;
    box-shadow: inset -1px -1px 0px #404040, inset 1px 1px 0px #dfdfdf !important;
    padding: 4px !important;
    margin-bottom: 20px;
}

/* Active Navy Title Bar Gradient */
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
}

/* Sunken Inset Content Area Box */
.win95-inset-canvas {
    background-color: #FFFFFF !important;
    border: 2px solid !important;
    border-color: #808080 #ffffff #ffffff #808080 !important;
    box-shadow: inset 1px 1px 0px #404040, inset -1px -1px 0px #dfdfdf !important;
    padding: 16px !important;
    color: #000000 !important;
}

/* Notepad Panel Yellow Accent */
.win95-notepad {
    background-color: #FFFFCC !important;
    border: 2px solid !important;
    border-color: #808080 #ffffff #ffffff #808080 !important;
    padding: 12px !important;
    color: #000000 !important;
}

/* Hyperlink overrides */
a {
    color: #0000FF !important;
    text-decoration: underline !important;
}
a:hover {
    color: #FF0000 !important;
}

/* 3D Etched Groove Divider Rule */
.win95-hr {
    border: none !important;
    height: 4px !important;
    background: linear-gradient(to bottom, #808080 0%, #808080 50%, #ffffff 50%, #ffffff 100%) !important;
    margin: 20px 0 !important;
}

/* Construction Warnings Stripes Block */
.construction-stripes {
    background: repeating-linear-gradient(45deg, #ffff00, #ffff00 12px, #000000 12px, #000000 24px) !important;
    height: 12px;
    width: 100%;
    margin: 8px 0;
}

/* Rainbow Headings Keyframe Animation */
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

/* Native Streamlit Form & Input Button Adjustments */
.stButton > button {
    background-color: #C0C0C0 !important;
    color: #000000 !important;
    font-weight: bold !important;
    border: 2px solid !important;
    border-color: #ffffff #808080 #808080 #ffffff !important;
    box-shadow: inset -1px -1px 0px #404040, inset 1px 1px 0px #dfdfdf !important;
    border-radius: 0px !important;
    transition: none !important;
}
.stButton > button:active {
    border-color: #808080 #ffffff #ffffff #808080 !important;
    transform: translate(1px, 1px) !important;
}
.stButton > button:focus {
    outline: 2px dotted #000000 !important;
}

/* Hit Counter Panel box style */
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
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 90s MARQUEE BANNER
# ─────────────────────────────────────────────
st.markdown("""
<div style="background-color:#000080; color:#FFFF00; font-family:'Courier New'; padding:3px; font-weight:bold; border-bottom:2px solid #000;">
    <marquee scrollamount="5">💥 SITE ALIVE // SYSTEM ENGINE RUNNING 100% PURE C95 CORE VECTOR ARCHITECTURE // NO LOGIN REQUIRED 💥</marquee>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ENVIRONMENT WORKSPACE CONTROLLER
# ─────────────────────────────────────────────
st.markdown("<br/>", unsafe_allow_html=True)
top_c1, top_c2 = st.columns([3, 1])

with top_c1:
    st.markdown("<h1 class='rainbow-text' style='margin:0; font-size:42px;'>ATS RESUME PIPELINE PRO '97</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-weight:bold;'>Welcome to the primitive automated matrix deployment workspace.</p>", unsafe_allow_html=True)

with top_c2:
    user_role = st.radio(
        "Select Desktop Workspace Shell Mode:",
        ["Job Seeker", "Enterprise Recruiter"],
        horizontal=False
    )

# ─────────────────────────────────────────────
# MAIN PANEL APPLICATIONS WINDOW
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="win95-window">
    <div class="win95-titlebar">
        <span>⚙️ Configuration_Wizard.exe [Mode: {user_role}]</span>
        <span>[?] [X]</span>
    </div>
</div>
""", unsafe_allow_html=True)

panel_c1, panel_c2 = st.columns(2, gap="large")

with panel_c1:
    st.markdown("### 📄 Step 1: Upload Portfolio Data")
    resume_file = st.file_uploader("Drop target binary object here (.pdf)", type=["pdf"], key="res_upload")
    
with panel_c2:
    if user_role == "Enterprise Recruiter":
        st.markdown("### 💼 Step 2: Role Profile Target Context (Compulsory)")
        job_text = st.text_area("Paste job specifications row elements data parameters here:", height=120, key="jd_text_rec")
    else:
        st.markdown("### 💼 Step 2: Role Profile Target Context (Optional)")
        has_jd_toggle = st.checkbox("Toggle target role profiling parameters manual mapping constraints", value=True)
        job_text = ""
        if has_jd_toggle:
            job_text = st.text_area("Paste job specifications row elements data parameters here:", height=90, key="jd_text_app")

# Execute Command Segment
st.markdown("<div class='win95-hr'></div>", unsafe_allow_html=True)
btn_col = st.columns([1, 2, 1])
with btn_col[1]:
    is_recruiter = (user_role == "Enterprise Recruiter")
    action_disabled = not resume_file or (is_recruiter and not job_text.strip())
    analyze_btn = st.button("💾 Run Diagnostics Processing Sequence [CLICK HERE]", disabled=action_disabled)

if not resume_file:
    st.markdown("""
    <div class="win95-window" style="text-align:center; padding:40px 10px;">
        <span style="font-size:30px;">⚠️</span>
        <p style="font-weight:bold; font-family:'Courier New';">SYSTEM IDLE: SYSTEM REQUIREMENT MATRIX PACKET RESUME FILE MISSING.</p>
        <div class="construction-stripes"></div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

if analyze_btn:
    with st.spinner("Executing system pipeline computations..."):
        resume_payload_text = extract_text_from_pdf(resume_file)
        if not resume_payload_text:
            st.error("Fatal system IO failure mapping text segment streams.")
            st.stop()
        compiled_results = analyze(resume_payload_text, job_text if (not is_recruiter or job_text.strip()) else None)
        st.session_state['compiled_results'] = compiled_results
        st.session_state['cached_res_text'] = resume_payload_text

results = st.session_state.get('compiled_results')
resume_text = st.session_state.get('cached_res_text', '')

if not results:
    st.stop()

# ─────────────────────────────────────────────
# SYSTEM RESULTS DESKTOP WINDOWS LAYER
# ─────────────────────────────────────────────
emoji, heading, score_hex = verdict(results['total'])

st.markdown(f"""
<div class="win95-window">
    <div class="win95-titlebar">
        <span>📊 Analysis_Console_Output.log // Target Metric Readouts</span>
        <span>[X]</span>
    </div>
</div>
""", unsafe_allow_html=True)

an_c1, an_c2, an_c3, an_c4 = st.columns([1.2, 1, 1, 1])

with an_c1:
    st.image(gauge_chart(results['total']), use_container_width=True)

with an_c2:
    st.markdown(f"""
    <div class="win95-inset-canvas" style="height:100%; text-align:center;">
        <p style="font-family:'Arial Black'; font-size:14px; margin:0; text-transform:uppercase;">TOTAL CALCULATED OUTPUTFIT</p>
        <h2 style="font-size:42px; font-family:Impact; color:{score_hex}; margin:5px 0;">{results['total']:.0f} / 100</h2>
        <div class="hit-counter">STATUS: {heading} {emoji}</div>
    </div>
    """, unsafe_allow_html=True)

with an_c3:
    rd = results['readability']
    st.markdown(f"""
    <div class="win95-inset-canvas" style="height:100%; font-family:'Courier New';">
        <p style="font-weight:bold; margin:0; background-color:#000080; color:#fff; padding:2px;">[READABILITY ENGINE]</p>
        <p style="margin-top:5px;"><b>Index Score:</b> {rd['score']}</p>
        <p><b>Tier State:</b> {rd['label']}</p>
        <p><b>Word Count:</b> {rd['word_count']} units</p>
    </div>
    """, unsafe_allow_html=True)

with an_c4:
    qf = results['quantification']
    av = results['action_verbs']
    st.markdown(f"""
    <div class="win95-notepad" style="height:100%; font-family:'Courier New';">
        <p style="font-weight:bold; margin:0; border-bottom:1px solid #000;">📝 INDEX DATA MARKERS</p>
        <p style="margin-top:5px;"><b>Quant Score:</b> {qf['label']} ({qf['count']} found)</p>
        <p><b>Action Verbs:</b> {len(av['found'])} tokens loaded</p>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SEPARATED RECRUITER VS APPLICANT DISPLAY VIEWPORT
# ─────────────────────────────────────────────
st.markdown("<br/>", unsafe_allow_html=True)

if user_role == "Enterprise Recruiter":
    st.markdown("### 🛠️ Data Systems Recruiter Matrix Views")
    tab_rec1, tab_rec2, tab_rec3 = st.tabs(["📊 Metric Projections", "🔍 Word Intersect Elements", "🚨 Core System Red Flags"])
    
    with tab_rec1:
        rc1, rc2 = st.columns([1.5, 1])
        with rc1:
            st.image(bar_chart(results['score_vector']), use_container_width=True)
        with rc2:
            st.image(score_donut(results['score_vector']), use_container_width=True)
        st.markdown("<p style='font-family:monospace; font-weight:bold;'>COMPUTED MATRIX DATA PROFILE SUMMARY TABLE:</p>", unsafe_allow_html=True)
        st.dataframe(results['score_df'], hide_index=True, use_container_width=True)
        
    with tab_rec2:
        if results['has_jd'] and results['matched_keywords']:
            st.image(keyword_heatmap(results['matched_keywords'], resume_text, job_text), use_container_width=True)
        mc1, mc2 = st.columns(2)
        with mc1:
            st.markdown("<p style='font-weight:bold; background-color:#808080; color:#fff; padding:2px;'>Overlap Skills Confirmed:</p>", unsafe_allow_html=True)
            st.write(", ".join(results['matched_skills']) if results['matched_skills'] else "No baseline intersects.")
        with mc2:
            st.markdown("<p style='font-weight:bold; background-color:#808080; color:#fff; padding:2px;'>Discovered File Node Headers:</p>", unsafe_allow_html=True)
            st.write(results['found_sections'])

    with tab_rec3:
        if results['red_flags']:
            for flag in results['red_flags']:
                st.markdown(f"<div style='background-color:#FF0000; color:#FFF; padding:8px; font-weight:bold; margin-bottom:4px;'>[SYSTEM RISK FLAG] !! {flag}</div>", unsafe_allow_html=True)
        else:
            st.success("Structure evaluation returned zero anomalous parsing compliance vulnerabilities.")

else:
    st.markdown("### 🛠️ Strategic Candidate Enhancement Panel")
    tab_app1, tab_app2, tab_app3 = st.tabs(["💡 Engineering Improvement Tips", "🔤 Missing Target Key Elements", "💾 Export Text Logs"])
    
    with tab_app1:
        tips = []
        if results['has_jd'] and results['kw_match_pct'] < 55:
            tips.append(f"CRITICAL GAP DETECTED: Missing contextual core alignment tokens: {', '.join(results['missing_keywords'][:5])}")
        if results['missing_skills']:
            tips.append(f"COMPETENCY ERROR: Inject standard framework modules into core blocks: {', '.join(results['missing_skills'][:4])}")
        if len(results['action_verbs']['found']) < 7:
            tips.append("DESCRIPTIVE ERROR: Supplement narrative items using definitive vector verbs (e.g. 'spearheaded', 'automated').")
        
        for tip in tips:
            st.markdown(f"<div style='border:2px solid #000; background-color:#FFFFCC; padding:8px; margin-bottom:4px; font-family:monospace;'>💡 [DIRECTIVE] -> {tip}</div>", unsafe_allow_html=True)
        
        st.image(radar_chart(results['score_vector']), width=400)

    with tab_app2:
        kc1, kc2 = st.columns(2)
        with kc1:
            st.markdown("<p style='color:#FF0000; font-weight:bold;'>❌ MISSING CRITICAL COMPETENCIES:</p>", unsafe_allow_html=True)
            st.write(", ".join(results['missing_skills']) if results['missing_skills'] else "Zero deficit parameters mapped.")
        with kc2:
            st.markdown("<p style='color:#00AA00; font-weight:bold;'>✅ CONFIRMED ASSET SKILLS LOGGED:</p>", unsafe_allow_html=True)
            st.write(", ".join(results['matched_skills']) if results['matched_skills'] else "No baseline elements logged.")

    with tab_app3:
        report_data = generate_report(results)
        st.download_button(
            label="💾 DOWNLOAD DIAGNOSTICS REPORT DOCUMENT (.TXT FILE OBJECT)",
            data=report_data,
            file_name="ats_diagnostic_stream.txt",
            mime="text/plain"
        )