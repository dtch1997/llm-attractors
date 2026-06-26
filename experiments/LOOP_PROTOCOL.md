# Experiment-loop protocol (llm-attractors)

This is the `protocol` block flywheel injects into each iteration's prompt.
These are API-only behavioral experiments — no GPU/Tinker. Cheap and fast.

1. **WORKTREE FIRST.** This repo is a standalone repo nested under
   `jarvis/repos/llm-attractors`. Work happens on a dedicated branch in a
   worktree under this repo's own `.claude/worktrees/<branch>`. (The current
   loop already runs inside `.claude/worktrees/flywheel-research`; small
   experiments may proceed on that branch — open a sub-branch only if isolation
   is needed.)

2. **SPEC BEFORE SPEND — non-negotiable.** Make the experiment a directory
   `experiments/<date>-<slug>/` with a `spec.md`: hypothesis, a *registered
   prediction with a confidence*, the design, **positive AND negative
   controls**, and a cost estimate / tier. An experiment that fails its
   controls is discarded before anyone sees the result.

3. **RUN IT.** Cheap-first: a tiny dry run (1–2 runs, few turns) to validate
   the command and that the basin is visible, then scale N/turns only if green.
   Drive the harness via `boom/run.py` (use the worktree `.venv`). Keys come
   from `~/.env` (`set -a; source ~/.env; set +a`): `ANTHROPIC_API_KEY` for
   native models, `OPENROUTER_API_KEY` for `provider=openrouter`. Prefer cheap
   models for discovery; spend Opus turns only to confirm a headline.

4. **WRITE UP.** Write `postmortem.md`: results vs the registered prediction;
   append outcomes to `experiments/prediction-registry.md` and a line to
   `changelog.md`. **Surprise always escalates** — a result that contradicts
   the registered prediction is a discovery-or-bug flag for a human.

5. **WRAP UP (reproducibility + persistence).** Commit on the worktree branch
   and open a PR; ensure the spec + exact command + seeds/config are committed
   so a fresh run regenerates the result. Persist large raw artifacts (full
   transcripts) to
   `gs://alignment-team-general-storage/daniel/jarvis/experiments/llm-attractors-<slug>/`
   and commit a pointer + the lean `lengths.jsonl`/scores, not the bytes.

6. **BRAINSTORM NEXT.** Propose 2–4 concrete, de-risked follow-ups — each a real
   next experiment (a new stimulus class, a control, a cross-model step, a
   dynamics probe), not a vague remix. File them onto the backlog with
   `flywheel add`. This keeps the flywheel turning.

Binding rules: Tier 0 (<$10) runs freely; $200 aggregate budget; 3 strikes per
hypothesis → escalate or drop; controls always.
