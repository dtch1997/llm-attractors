"""Headline figure: assistant response length vs turn, one line per run.

The single takeaway — under repeated "boom", responses collapse toward silence
(disengagement), they do not grow (escalation).

    python boom/make_figure.py results/trajectories.jsonl figures/response_length.png
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def main():
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "results/trajectories.jsonl")
    out = Path(sys.argv[2] if len(sys.argv) > 2 else "figures/response_length.png")
    out.parent.mkdir(parents=True, exist_ok=True)

    runs = [json.loads(l) for l in src.open()]
    model = runs[0].get("model", "?")

    fig, ax = plt.subplots(figsize=(8, 5))
    maxlen = 0
    for r in runs:
        ac = r["assistant_chars"]
        maxlen = max(maxlen, len(ac))
        ax.plot(range(len(ac)), ac, color="0.7", lw=1, alpha=0.8, zorder=1)

    # mean over runs at each turn index (runs share the same length here)
    n = min(len(r["assistant_chars"]) for r in runs)
    mean = [sum(r["assistant_chars"][i] for r in runs) / len(runs) for i in range(n)]
    ax.plot(range(n), mean, color="C3", lw=2.5, zorder=3, label=f"mean of {len(runs)} runs")

    ax.set_yscale("symlog")
    ax.set_xlabel("turn  (0 = 'nuke the task'; 1+ = 'boom')")
    ax.set_ylabel("assistant response length (characters, symlog)")
    ax.set_title("Repeated “boom”: the model disengages, it doesn't escalate")
    ax.legend(loc="upper right", frameon=False)
    ax.annotate("seed reply\n(longest)", xy=(0, mean[0]), xytext=(4, max(mean) * 1.5),
                fontsize=8, color="0.4",
                arrowprops=dict(arrowstyle="->", color="0.6", lw=0.8))
    ax.margins(x=0.02)
    fig.text(0.5, -0.02, f"model: {model}  ·  one grey line per run", ha="center",
             fontsize=8, color="0.5")
    fig.tight_layout()
    fig.savefig(out, dpi=130, bbox_inches="tight")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
