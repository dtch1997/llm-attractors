#!/usr/bin/env python
"""Analyze the discovery sweep: per-cell trajectory stats + a length-shape
heuristic + sampled transcripts for basin naming.

  .venv/bin/python experiments/2026-06-26-stimulus-sweep-discovery/analyze.py
Writes:
  results/discovery/summary.csv     — one row per (model, stimulus)
  results/discovery/samples.md      — one sampled transcript per cell (truncated)
"""
from __future__ import annotations
import json, csv, statistics as st
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "results" / "discovery"
ALL = OUT / "all.jsonl"


def shape(first, last, mx):
    """Crude length-trajectory label (basin naming is the judge's job)."""
    if last >= 2.0 * max(first, 1) and mx >= 600:
        return "escalate"
    if last <= 0.5 * first and last <= 60:
        return "disengage"
    return "flat/other"


def load():
    rows = []
    for line in ALL.read_text().splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def main():
    rows = load()
    # group by (model_slug, stim_slug)
    cells = {}
    for r in rows:
        cells.setdefault((r["model_slug"], r["stim_slug"]), []).append(r)

    summ = []
    for (m, s), rs in sorted(cells.items()):
        ac = [r["assistant_chars"] for r in rs if r.get("assistant_chars")]
        firsts = [a[0] for a in ac if a]
        lasts = [a[-1] for a in ac if a]
        last3 = [st.mean(a[-3:]) for a in ac if len(a) >= 1]
        maxes = [max(a) for a in ac if a]
        errs = [r.get("error") for r in rs]
        cf = sum(1 for e in errs if e and "content_filter" in e)
        rf = sum(1 for e in errs if e and "refusal" in e)
        f = st.mean(firsts) if firsts else 0
        l = st.mean(lasts) if lasts else 0
        l3 = st.mean(last3) if last3 else 0
        mx = max(maxes) if maxes else 0
        summ.append({
            "model": m, "stim": s, "class": rs[0].get("stim_class", ""),
            "n": len(rs), "first": round(f), "last": round(l),
            "last3": round(l3), "max": mx,
            "ratio_last_first": round(l / max(f, 1), 2),
            "content_filter": cf, "refusal": rf,
            "shape": shape(f, l, mx),
        })

    with (OUT / "summary.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(summ[0].keys()))
        w.writeheader()
        w.writerows(summ)

    # one sampled transcript per cell (first run), truncated turns
    with (OUT / "samples.md").open("w") as fh:
        for (m, s), rs in sorted(cells.items()):
            r = rs[0]
            fh.write(f"\n\n# {m} :: {s}  (class={r.get('stim_class')}, err={r.get('error')})\n")
            fh.write(f"chars trajectory: {r.get('assistant_chars')}\n\n")
            turns = r.get("turns", [])
            # sample steps 0,1,2, mid, last two
            steps_seen = sorted({t.get("step") for t in turns if t["role"] == "assistant"})
            keep = set(steps_seen[:3] + steps_seen[len(steps_seen)//2:len(steps_seen)//2+1] + steps_seen[-2:])
            for t in turns:
                if t["role"] == "assistant" and t.get("step") in keep:
                    txt = (t.get("text") or "")[:700]
                    fh.write(f"  [{t['step']}] ({t['chars']}c) {txt!r}\n")

    # console summary
    print(f"{'model':18} {'stim':12} {'cls':11} {'first':>5} {'last':>5} {'max':>6} {'shape':12} cf/rf")
    for d in summ:
        print(f"{d['model']:18} {d['stim']:12} {d['class']:11} {d['first']:>5} {d['last']:>5} "
              f"{d['max']:>6} {d['shape']:12} {d['content_filter']}/{d['refusal']}")
    # shape tally per model
    print("\nshape tally:")
    tally = {}
    for d in summ:
        tally.setdefault((d["model"], d["shape"]), 0)
        tally[(d["model"], d["shape"])] += 1
    for k, v in sorted(tally.items()):
        print(f"  {k[0]:18} {k[1]:12} {v}")


if __name__ == "__main__":
    main()
