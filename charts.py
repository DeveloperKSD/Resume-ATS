"""
charts.py — Enhanced chart generation for ATS Resume Scanner
All charts use a cohesive glassmorphism dark palette.
"""

import io
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.patheffects as pe

# ─────────────────────────────────────────────
# PALETTE & THEME
# ─────────────────────────────────────────────

BG        = "#0d0f1a"
PANEL     = "#13162a"
ACCENT    = "#6366f1"
ACCENT2   = "#8b5cf6"
ACCENT3   = "#06b6d4"
GREEN     = "#22c55e"
YELLOW    = "#eab308"
ORANGE    = "#f97316"
RED       = "#ef4444"
TEXT      = "#e2e8f0"
MUTED     = "#475569"
GRID      = "#1e2235"

LABELS  = ['Keyword\nMatch', 'Skills\nMatch', 'Cosine\nSimilarity', 'TF-IDF\nRelevance', 'Section\nPresence']
MAXVALS = [35, 25, 20, 10, 10]
COLORS  = [ACCENT, ACCENT2, ACCENT3, "#a78bfa", "#34d399"]

def _base_fig(w=8, h=4.5):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(PANEL)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID)
    ax.tick_params(colors=TEXT, labelsize=8)
    return fig, ax

def _save(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight",
                facecolor=fig.get_facecolor(), dpi=150)
    plt.close(fig)
    buf.seek(0)
    return buf


# ─────────────────────────────────────────────
# 1. HORIZONTAL BAR CHART (score breakdown)
# ─────────────────────────────────────────────

def bar_chart(score_vector: np.ndarray):
    fig, ax = _base_fig(8, 4)

    ratios = score_vector / np.array(MAXVALS)
    bar_colors = [GREEN if r >= 0.7 else YELLOW if r >= 0.45 else RED for r in ratios]

    y_pos = np.arange(len(LABELS))
    # Background (max) bars
    ax.barh(y_pos, MAXVALS, color=GRID, height=0.55, zorder=1)
    # Score bars
    bars = ax.barh(y_pos, score_vector, color=bar_colors, height=0.55,
                   zorder=2, alpha=0.9)

    # Glow effect via thin bright edge
    for bar, c in zip(bars, bar_colors):
        bar.set_edgecolor(c)
        bar.set_linewidth(0.8)

    # Labels
    for i, (score, mx, ratio) in enumerate(zip(score_vector, MAXVALS, ratios)):
        ax.text(mx + 0.4, i, f"{score:.1f}/{mx}", va='center',
                color=TEXT, fontsize=8.5, fontweight='bold',
                fontfamily='monospace')
        pct_color = GREEN if ratio >= 0.7 else YELLOW if ratio >= 0.45 else RED
        ax.text(score / 2, i, f"{ratio*100:.0f}%", va='center', ha='center',
                color='white', fontsize=8, fontweight='bold', zorder=3)

    ax.set_yticks(y_pos)
    ax.set_yticklabels([l.replace('\n', ' ') for l in LABELS],
                       color=TEXT, fontsize=9)
    ax.set_xlim(0, max(MAXVALS) + 6)
    ax.set_xlabel("Score", color=MUTED, fontsize=8)
    ax.xaxis.label.set_color(MUTED)
    ax.tick_params(axis='x', colors=MUTED)
    ax.grid(axis='x', color=GRID, linewidth=0.5, zorder=0)
    ax.set_title("Score Breakdown", color=TEXT, fontsize=11,
                 fontweight='bold', pad=10)
    fig.tight_layout()
    return _save(fig)


# ─────────────────────────────────────────────
# 2. RADAR CHART
# ─────────────────────────────────────────────

def radar_chart(score_vector: np.ndarray):
    categories = ['Keywords', 'Skills', 'Similarity', 'TF-IDF', 'Sections']
    ratios = (score_vector / np.array(MAXVALS)).tolist()
    N = len(categories)

    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]
    ratios += ratios[:1]

    fig = plt.figure(figsize=(5, 5), facecolor=BG)
    ax  = fig.add_subplot(111, polar=True)
    ax.set_facecolor(PANEL)

    # Grid rings
    for r in [0.25, 0.5, 0.75, 1.0]:
        ax.plot(angles, [r] * (N + 1), color=GRID, linewidth=0.8, linestyle='--')
        ax.text(angles[0], r + 0.04, f"{int(r*100)}%",
                ha='center', va='center', color=MUTED, fontsize=7)

    # Fill + line
    ax.fill(angles, ratios, alpha=0.25, color=ACCENT)
    ax.plot(angles, ratios, color=ACCENT, linewidth=2.5)

    # Dots at each vertex
    for angle, ratio in zip(angles[:-1], ratios[:-1]):
        color = GREEN if ratio >= 0.7 else YELLOW if ratio >= 0.45 else RED
        ax.plot(angle, ratio, 'o', color=color, markersize=7, zorder=5)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, color=TEXT, fontsize=8.5)
    ax.set_yticklabels([])
    ax.set_ylim(0, 1)
    ax.spines['polar'].set_color(GRID)
    ax.tick_params(colors=TEXT)
    ax.set_title("Performance Radar", color=TEXT, fontsize=11,
                 fontweight='bold', pad=18)
    fig.tight_layout()
    return _save(fig)


# ─────────────────────────────────────────────
# 3. GAUGE CHART
# ─────────────────────────────────────────────

def gauge_chart(score: float):
    fig, ax = plt.subplots(figsize=(5, 3.2), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    score = max(0, min(100, score))

    # Color zones: red → orange → yellow → green
    zones = [(25, RED), (15, ORANGE), (20, YELLOW), (40, GREEN)]
    theta_start = np.pi
    for span_pct, color in zones:
        span = np.deg2rad(span_pct * 1.8)
        theta = np.linspace(theta_start, theta_start - span, 100)
        ax.fill_between(theta, 0.65, 0.85, color=color, alpha=0.85, zorder=2)
        theta_start -= span

    # Needle
    needle_angle = np.pi - np.deg2rad(score * 1.8)
    ax.annotate('', xy=(needle_angle, 0.6), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color=TEXT,
                                lw=2.5, mutation_scale=15))

    # Center dot
    ax.plot(0, 0, 'o', color=TEXT, markersize=5, zorder=10)

    # Score text
    ax.text(0, -0.15, f"{score:.0f}", ha='center', va='center',
            fontsize=28, fontweight='bold', color=TEXT,
            transform=ax.transData)
    ax.text(0, -0.38, "/ 100", ha='center', va='center',
            fontsize=11, color=MUTED, transform=ax.transData)

    ax.set_ylim(-0.5, 1)
    ax.set_xlim(-np.pi / 2, np.pi / 2)
    ax.set_theta_zero_location('W')
    ax.set_theta_direction(-1)
    ax.axis('off')
    fig.tight_layout(pad=0)
    return _save(fig)


# ─────────────────────────────────────────────
# 4. KEYWORD FREQUENCY HEATMAP (NEW)
# ─────────────────────────────────────────────

def keyword_heatmap(matched_kw: list, resume_text: str, job_text: str, top_n=20):
    """Bar chart showing keyword frequency in resume vs JD."""
    if not matched_kw:
        return None

    # Count frequencies
    words = matched_kw[:top_n]
    resume_lower = resume_text.lower()
    jd_lower     = job_text.lower()

    resume_counts = [resume_lower.split().count(w) for w in words]
    jd_counts     = [jd_lower.split().count(w) for w in words]

    fig, ax = _base_fig(9, max(3.5, len(words) * 0.45))
    y = np.arange(len(words))
    h = 0.38

    ax.barh(y + h/2, jd_counts,    h, color=ACCENT,  alpha=0.85, label='Job Description', zorder=2)
    ax.barh(y - h/2, resume_counts, h, color=ACCENT3, alpha=0.85, label='Your Resume',      zorder=2)

    ax.set_yticks(y)
    ax.set_yticklabels(words, color=TEXT, fontsize=8, fontfamily='monospace')
    ax.set_xlabel("Occurrences", color=MUTED, fontsize=8)
    ax.grid(axis='x', color=GRID, linewidth=0.5, zorder=0)
    ax.set_title("Matched Keyword Frequency: Resume vs JD", color=TEXT,
                 fontsize=11, fontweight='bold', pad=10)

    legend = ax.legend(facecolor=PANEL, edgecolor=GRID, labelcolor=TEXT, fontsize=8)
    fig.tight_layout()
    return _save(fig)


# ─────────────────────────────────────────────
# 5. SCORE DONUT (NEW — compact summary)
# ─────────────────────────────────────────────

def score_donut(score_vector: np.ndarray):
    """Donut chart showing proportional contribution of each component."""
    fig, ax = plt.subplots(figsize=(5, 4.5))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    labels_short = ['Keywords', 'Skills', 'Similarity', 'TF-IDF', 'Sections']
    wedge_colors = COLORS

    wedges, texts, autotexts = ax.pie(
        score_vector,
        labels=None,
        colors=wedge_colors,
        autopct=lambda p: f'{p:.0f}%' if p > 5 else '',
        startangle=90,
        wedgeprops=dict(width=0.55, edgecolor=BG, linewidth=2),
        pctdistance=0.75,
    )

    for t in autotexts:
        t.set_color('white')
        t.set_fontsize(8)
        t.set_fontweight('bold')

    # Center total
    total = score_vector.sum()
    ax.text(0, 0.08, f"{total:.0f}", ha='center', va='center',
            fontsize=26, fontweight='bold', color=TEXT)
    ax.text(0, -0.18, "Total Score", ha='center', va='center',
            fontsize=9, color=MUTED)

    # Legend
    patches = [mpatches.Patch(color=c, label=f"{l} ({s:.1f})")
               for c, l, s in zip(wedge_colors, labels_short, score_vector)]
    ax.legend(handles=patches, loc='lower center', bbox_to_anchor=(0.5, -0.18),
              ncol=3, facecolor=PANEL, edgecolor=GRID, labelcolor=TEXT, fontsize=7.5)

    ax.set_title("Score Composition", color=TEXT, fontsize=11,
                 fontweight='bold', pad=10)
    fig.tight_layout()
    return _save(fig)
