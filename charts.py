"""
charts.py — Matplotlib visualizations for ATS results
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')   # non-interactive backend (works in Streamlit & Docker)
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import io


# ── Shared style ──────────────────────────────────────────────────────────────
BG       = "#0f1117"
CARD     = "#1e2130"
ACCENT   = "#6366f1"       # indigo
GREEN    = "#22c55e"
YELLOW   = "#eab308"
ORANGE   = "#f97316"
RED      = "#ef4444"
TEXT     = "#e2e8f0"
SUBTEXT  = "#94a3b8"

COMPONENTS = ['Keyword\nMatch', 'Skills\nMatch', 'Cosine\nSimilarity', 'TF-IDF\nRelevance', 'Section\nPresence']
MAXES      = np.array([35, 25, 20, 10, 10])


def _score_color(pct: float) -> str:
    if pct >= 80: return GREEN
    if pct >= 60: return YELLOW
    if pct >= 40: return ORANGE
    return RED


def _fig_to_bytes(fig) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor=BG)
    buf.seek(0)
    return buf.read()


# ── Chart 1: Horizontal bar chart ────────────────────────────────────────────

def bar_chart(score_vector: np.ndarray) -> bytes:
    pcts = score_vector / MAXES * 100

    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(CARD)

    y = np.arange(len(COMPONENTS))
    bars = ax.barh(y, pcts, height=0.55, color=[_score_color(p) for p in pcts],
                   zorder=3)

    # background full bars
    ax.barh(y, [100]*len(y), height=0.55, color='#2a2f45', zorder=2)

    for bar, pct, raw in zip(bars, pcts, score_vector):
        ax.text(bar.get_width() + 1.5, bar.get_y() + bar.get_height()/2,
                f'{pct:.0f}%  ({raw:.1f})', va='center', ha='left',
                color=TEXT, fontsize=9, fontweight='bold')

    ax.set_yticks(y)
    ax.set_yticklabels(COMPONENTS, color=TEXT, fontsize=10)
    ax.set_xlim(0, 120)
    ax.set_xlabel('Score %', color=SUBTEXT, fontsize=9)
    ax.set_title('ATS Score Breakdown', color=TEXT, fontsize=13, fontweight='bold', pad=12)
    ax.tick_params(colors=SUBTEXT, labelsize=8)
    ax.spines[:].set_visible(False)
    ax.xaxis.grid(True, color='#2a2f45', linestyle='--', linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)

    plt.tight_layout()
    data = _fig_to_bytes(fig)
    plt.close(fig)
    return data


# ── Chart 2: Radar / spider chart ────────────────────────────────────────────

def radar_chart(score_vector: np.ndarray) -> bytes:
    pcts = (score_vector / MAXES * 100).tolist()
    labels = ['Keyword', 'Skills', 'Cosine', 'TF-IDF', 'Sections']
    N = len(labels)

    angles = [n / N * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    pcts   += pcts[:1]

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    ax.plot(angles, pcts, color=ACCENT, linewidth=2)
    ax.fill(angles, pcts, color=ACCENT, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color=TEXT, fontsize=10)
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20','40','60','80','100'], color=SUBTEXT, fontsize=7)
    ax.grid(color='#2a2f45', linewidth=0.8)
    ax.spines['polar'].set_color('#2a2f45')
    ax.set_title('Component Radar', color=TEXT, fontsize=12, fontweight='bold', pad=18)

    plt.tight_layout()
    data = _fig_to_bytes(fig)
    plt.close(fig)
    return data


# ── Chart 3: Gauge (total score) ─────────────────────────────────────────────

def gauge_chart(total: float) -> bytes:
    fig, ax = plt.subplots(figsize=(5, 3))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 200)
    ax.set_ylim(0, 110)
    ax.axis('off')

    # background arc
    theta = np.linspace(np.pi, 0, 200)
    r = 80
    cx, cy = 100, 10

    # color zones
    zones = [(0,40,RED), (40,60,ORANGE), (60,80,YELLOW), (80,100,GREEN)]
    for lo, hi, color in zones:
        t = np.linspace(np.pi * (1 - lo/100), np.pi * (1 - hi/100), 50)
        x_out = cx + r * np.cos(t)
        y_out = cy + r * np.sin(t)
        x_in  = cx + (r-18) * np.cos(t[::-1])
        y_in  = cy + (r-18) * np.sin(t[::-1])
        ax.fill(np.concatenate([x_out, x_in]),
                np.concatenate([y_out, y_in]),
                color=color, alpha=0.85)

    # needle
    angle  = np.pi * (1 - total/100)
    nx     = cx + 65 * np.cos(angle)
    ny     = cy + 65 * np.sin(angle)
    ax.annotate('', xy=(nx, ny), xytext=(cx, cy),
                arrowprops=dict(arrowstyle='->', color=TEXT, lw=2.5))
    ax.plot(cx, cy, 'o', color=TEXT, markersize=7, zorder=5)

    color = _score_color(total)
    ax.text(cx, cy + 42, f'{total:.1f}', ha='center', va='center',
            fontsize=28, fontweight='bold', color=color)
    ax.text(cx, cy + 22, '/ 100', ha='center', va='center',
            fontsize=13, color=SUBTEXT)
    ax.text(cx, cy - 8, 'ATS SCORE', ha='center', va='center',
        fontsize=10, color=SUBTEXT)

    plt.tight_layout()
    data = _fig_to_bytes(fig)
    plt.close(fig)
    return data
