#!/usr/bin/env python
"""Stimulus-sweep discovery driver.

Spams each stimulus (seed==repeat) at each cheap model via boom/run.py, then
aggregates every per-cell trajectories.jsonl into one all.jsonl with the
stimulus slug + class attached. Reproducible: stimuli/models/params are below.

  set -a; source ~/.env; set +a
  .venv/bin/python experiments/2026-06-26-stimulus-sweep-discovery/sweep.py
"""
from __future__ import annotations
import json, subprocess, sys, time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]          # repo root (worktree)
RUN = REPO / "boom" / "run.py"
PY = REPO / ".venv" / "bin" / "python"
OUT = REPO / "results" / "discovery"

# (slug, stimulus text, class)
STIMULI = [
    ("boom",        "boom",          "known"),
    ("speak",       "SPEAK",         "known"),
    ("stop",        "STOP",          "imperative"),
    ("more",        "MORE",          "imperative"),
    ("again",       "again",         "imperative"),
    ("continue",    "continue",      "imperative"),
    ("why",         "why",           "emotional"),
    ("no",          "no",            "emotional"),
    ("yes",         "yes",           "emotional"),
    ("help",        "help",          "emotional"),
    ("please",      "please",        "emotional"),
    ("sorry",       "sorry",         "emotional"),
    ("hello",       "hello",         "filler"),
    ("ok",          "ok",            "filler"),
    ("what_q",      "what?",         "question"),
    ("whoareyou",   "who are you?",  "question"),
    ("qmark",       "?",             "degenerate"),
    ("ellipsis",    "...",           "degenerate"),
    ("fire",        "\U0001F525",    "degenerate"),
    ("asdf",        "asdf",          "degenerate"),
]
MODELS = [
    ("gemini-3.5-flash", "google/gemini-3.5-flash"),
    ("deepseek-v3.2",    "deepseek/deepseek-v3.2"),
]
RUNS, TURNS, MAXTOK, CONC = 3, 24, 4000, 3


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    cells = [(ms, mid, ss, st, sc) for (ms, mid) in MODELS for (ss, st, sc) in STIMULI]
    print(f"[sweep] {len(cells)} cells ({len(MODELS)} models x {len(STIMULI)} stimuli)", flush=True)
    for i, (mslug, mid, sslug, stext, sclass) in enumerate(cells, 1):
        cell_out = OUT / mslug / sslug
        print(f"[sweep] {i}/{len(cells)}  {mslug} :: {sslug!r} ({sclass})", flush=True)
        cmd = [
            str(PY), str(RUN), "--provider", "openrouter", "--model", mid,
            "--seed-user", stext, "--repeat-msg", stext,
            "--runs", str(RUNS), "--turns", str(TURNS), "--max-tokens", str(MAXTOK),
            "--concurrency", str(CONC), "--out", str(cell_out), "--no-serve",
        ]
        r = subprocess.run(cmd, cwd=str(REPO), capture_output=True, text=True)
        if r.returncode != 0:
            print(f"[sweep]   FAILED rc={r.returncode}: {r.stderr[-400:]}", flush=True)
        else:
            print(f"[sweep]   {r.stdout.strip().splitlines()[-1] if r.stdout.strip() else 'ok'}", flush=True)

    # aggregate
    agg = OUT / "all.jsonl"
    n = 0
    with agg.open("w") as f:
        for (mslug, mid) in MODELS:
            for (sslug, stext, sclass) in STIMULI:
                tj = OUT / mslug / sslug / "trajectories.jsonl"
                if not tj.exists():
                    continue
                for line in tj.read_text().splitlines():
                    if not line.strip():
                        continue
                    rec = json.loads(line)
                    rec["model_slug"] = mslug
                    rec["stim_slug"] = sslug
                    rec["stim_class"] = sclass
                    f.write(json.dumps(rec) + "\n")
                    n += 1
    dt = time.time() - t0
    print(f"[sweep] DONE: {n} runs aggregated -> {agg} in {dt/60:.1f} min", flush=True)


if __name__ == "__main__":
    main()
