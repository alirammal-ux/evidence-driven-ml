'''Diagrams of the README: the project lifecycle (one row) and the improvement loop (a circle).
Run from the repository root:  python docs/make_diagrams.py   (needs matplotlib)'''

from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).parent
INK, MUTED, LINE, GREEN = "#333333", "#6B6B6B", "#BDBDBD", "#1E7A46"
plt.rcParams.update({"font.family": ["Noto Sans", "DejaVu Sans"], "svg.fonttype": "path"})


def box(ax, x, y, w, h, title, detail="", user=False, highlight=False):
    '''A rounded box centred at (x, y): bold title, optional grey detail; user steps filled in green.'''
    face = GREEN if user else "white"
    edge = GREEN if (user or highlight) else LINE
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.06",
                                facecolor=face, edgecolor=edge, linewidth=2.2 if highlight else 1.4))
    colour = "white" if user else INK
    if detail:
        ax.text(x, y + h * 0.15, title, ha="center", va="center", fontsize=12.5, fontweight="bold", color=colour)
        ax.text(x, y - h * 0.2, detail, ha="center", va="center", fontsize=9.5, color="white" if user else MUTED)
    else:
        ax.text(x, y, title, ha="center", va="center", fontsize=12.5, fontweight="bold", color=colour)


def arrow(ax, start, end, rad=0.0):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=13, color=MUTED, linewidth=1.3,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0))


def lifecycle(path):
    steps = [("Understand", "docs + interview"), ("EDA", "insights"), ("Plan", "metrics + rule"),
             ("Baselines", "first model"), ("Improve ↻", "the loop below"), ("Test", "once"),
             ("Deliver", "notebooks, slides")]
    w, h, gap = 1.62, 0.62, 0.3
    fig, ax = plt.subplots(figsize=(13.4, 1.3))
    for k, (title, detail) in enumerate(steps):
        x = k * (w + gap) + w / 2
        box(ax, x, 0, w, h, title, detail, highlight=title.startswith("Improve"))
        if k:
            arrow(ax, (x - w / 2 - gap + 0.04, 0), (x - w / 2 - 0.04, 0))
    ax.set_xlim(-0.05, len(steps) * (w + gap) - gap + 0.05)
    ax.set_ylim(-0.4, 0.4)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(path, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)


def loop(path):
    steps = [("Diagnose", "errors and ceilings", False), ("Propose", "gain, cost, risk", False),
             ("You choose", "", True), ("Fix the rule", "before running", False),
             ("You run it", "local or Kaggle/Colab", True), ("Evaluate", "paired bootstrap", False),
             ("You judge", "", True), ("Record", "DECISIONS.md", False)]
    r, w, h = 2.75, 1.75, 0.66
    angles = np.pi / 2 - np.arange(len(steps)) * 2 * np.pi / len(steps)      # clockwise from the top
    fig, ax = plt.subplots(figsize=(8.4, 7.6))
    points = [(r * np.cos(a), r * np.sin(a)) for a in angles]
    for k in range(len(steps)):                       # arcs between consecutive steps, along the circle
        a0, a1 = angles[k], angles[(k + 1) % len(steps)]
        mid0, mid1 = a0 - 0.27, a1 + 0.27
        arrow(ax, (r * np.cos(mid0), r * np.sin(mid0)), (r * np.cos(mid1), r * np.sin(mid1)), rad=-0.18)
    for (x, y), (title, detail, user) in zip(points, steps):
        box(ax, x, y, w, h, title, detail, user=user)
    ax.text(0, 0.2, "Improvement loop", ha="center", va="center", fontsize=15, fontweight="bold", color=INK)
    ax.text(0, -0.28, "adopted only if it passes\na rule written before the run", ha="center",
            va="center", fontsize=10.5, color=MUTED, linespacing=1.4)
    ax.set_xlim(-r - w / 2 - 0.1, r + w / 2 + 0.1)
    ax.set_ylim(-r - h / 2 - 0.1, r + h / 2 + 0.1)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(path, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    lifecycle(OUT / "lifecycle.svg")
    loop(OUT / "improvement-loop.svg")
    print("written:", OUT / "lifecycle.svg", OUT / "improvement-loop.svg")
