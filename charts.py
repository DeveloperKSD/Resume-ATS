"""
charts.py — 1990s Desktop Theme Chart Renderer
All visualization components emit strict geometric flat structures.
"""

import io
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ─────────────────────────────────────────────
# RETRO PALETTE CONFIGURATION
# ─────────────────────────────────────────────

BG      = "#C0C0C0"  # Classic Windows 95 Silver
PANEL   = "#FFFFFF"  # Sunken white page canvas
TEXT    = "#000000"  # Solid black
MUTED   = "#808080"  # 50% Gray
ACCENT  = "#0000FF"  # Hyperlink pure blue
RED     = "#FF0000"  # Accent secondary red
YELLOW  = "#FFFF00"  # Highlight yellow
GREEN   = "#00AA00"  # Success green

COLORS  = [ACCENT, RED, "#800080", GREEN, "#008080"]
LABELS  = ['Keywords', 'Skills', 'Cosine', 'TF-IDF', 'Sections']

def _retro_engine(fig, ax):
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(PANEL)
    ax.spines['top'].set_color(TEXT)
    ax.spines['bottom'].set_color(TEXT)
    ax.spines['left'].set_color(TEXT)
    ax.spines['right'].set_color(TEXT)
    ax.spines['top'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    ax.tick_params(colors=TEXT, labelsize=9)
    for t in ax.get_xticklabels() + ax.get_yticklabels():
        t.set_fontname('Arial')
        t.set_weight('bold')

def _output_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=110, facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return buf

def bar_chart(score_vector: np.ndarray):
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    _retro_engine(fig, ax)
    
    bars = ax.bar(LABELS, score_vector, color=COLORS, edgecolor=TEXT, linewidth=2, zorder=3)
    ax.grid(True, color=MUTED, linestyle='--', linewidth=1, zorder=1)
    
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 1, f'{h:.1f}', ha='center', va='bottom', color=TEXT, fontname='Arial', weight='bold', fontsize=9)
        
    ax.set_ylim(0, 40)
    return _output_bytes(fig)

def radar_chart(score_vector: np.ndarray):
    # Fallback to horizontal bar structure to mimic database readouts
    fig, ax = plt.subplots(figsize=(5, 3.8))
    _retro_engine(fig, ax)
    ax.barh(LABELS, score_vector, color=COLORS, edgecolor=TEXT, linewidth=2, zorder=3)
    ax.grid(True, color=MUTED, linestyle=':', linewidth=1)
    return _output_bytes(fig)

def gauge_chart(score: float):
    fig, ax = plt.subplots(figsize=(3.5, 3.5))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis('off')
    
    # Render vintage segmented square gauge
    ax.fill_between([0, 1], [0, 0], [1, 1], color=MUTED, zorder=1)
    ax.fill_between([0.05, 0.95], [0.05, 0.05], [0.95, 0.95], color=PANEL, zorder=2)
    
    # Fill proportion
    fill_height = 0.05 + (0.90 * (score / 100.0))
    ax.fill_between([0.05, 0.95], [0.05, 0.05], [fill_height, fill_height], color=ACCENT, zorder=3)
    
    ax.text(0.5, 0.5, f"{score:.0f}%", color=TEXT, fontsize=24, fontname='Impact', ha='center', va='center', zorder=4)
    return _output_bytes(fig)

def score_donut(score_vector: np.ndarray):
    fig, ax = plt.subplots(figsize=(4, 4))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    
    wedges, texts = ax.pie(
        score_vector + 0.1, # non-zero guard
        colors=COLORS,
        startangle=90,
        wedgeprops=dict(width=0.4, edgecolor=TEXT, linewidth=2)
    )
    
    total = score_vector.sum()
    ax.text(0, 0, f"{total:.0f}", ha='center', va='center', fontsize=22, fontname='Impact', color=TEXT)
    return _output_bytes(fig)

def keyword_heatmap(matched_keywords, resume_text, job_text, top_n=15):
    fig, ax = plt.subplots(figsize=(6, 2))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(PANEL)
    ax.axis('off')
    # Text placeholder box matching win95 dialog fields
    ax.text(0.5, 0.5, f"Matrix Tokens Verified:\n{len(matched_keywords)} Core System Keys Active", 
            ha='center', va='center', color=TEXT, fontname='Arial', weight='bold', bbox=dict(facecolor=YELLOW, edgecolor=TEXT, boxstyle='square,pad=1'))
    return _output_bytes(fig)