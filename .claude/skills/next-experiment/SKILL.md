---
name: next-experiment
description: Run ONE iteration of the autonomous attractor-research loop (flywheel) — pick the next experiment off experiments/queue.md, run it end-to-end, write it up, and file follow-ups. Use when asked to "run the next experiment", or driven via `/loop next-experiment`.
---

# Run the next experiment (flywheel iteration)

One turn of the attractor-research flywheel. Do the whole iteration, then stop.

## 1. Get the iteration

From the repo root (where `flywheel.toml` lives):

```bash
flywheel prompt --mark-running
```

- If it prints **"nothing eligible to pick"**: backlog empty or everything
  blocked by guardrails (budget/tier/strikes). **Stop** and say so — don't
  invent an experiment. (`flywheel status` / `flywheel next` show why.)
- Otherwise it prints the assembled prompt: north stars + prior reports + the
  **one selected idea** + the protocol + the exact bookkeeping commands.

## 2. Do exactly what that prompt says

Per `experiments/LOOP_PROTOCOL.md`:
1. **Worktree** on a dedicated branch (under this repo's `.claude/worktrees/`).
2. **Spec before spend** — `experiments/<date>-<slug>/spec.md` with a registered
   prediction + confidence and **positive & negative controls**.
3. **Run** cheap-first (tiny dry run → scale). `set -a; source ~/.env; set +a`
   for keys; use the worktree `.venv`; cheap models for discovery.
4. **Write up** — `postmortem.md`, prediction-registry + changelog lines.
   **Surprise escalates.** Controls fail → discard.
5. **Wrap up** — commit, PR, reproducibility, persist transcripts to GCS with a
   committed pointer.

## 3. Close the loop (bookkeeping — don't skip)

- `flywheel update <id> --status done --spec … --postmortem … --pr …`
  (or `flywheel update <id> --strikes <n>` if uninformative).
- `flywheel spend <dollars> --idea <id> --note "…"`.
- **File 2–4 concrete follow-ups**: `flywheel add --hypothesis "…"
  --rationale "…" --tier <0|1|2> --cost "$…" --source <id> --priority <n>`.

Keep going end-to-end; this is a delegated, autonomous iteration.
