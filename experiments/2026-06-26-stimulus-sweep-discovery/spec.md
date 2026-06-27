# Spec — stimulus-sweep discovery

**Idea id:** `stimulus-sweep-discovery` · **Tier 0** · est. **$3–6**
**Date:** 2026-06-26

## Question

When you spam a model with the *same* message over and over, it collapses into a
behavioral **basin**. We know three so far (disengage, escalate/worldbuild,
literary prose). **How many distinct basins are there, and which stimuli trigger
them?** This run sweeps many stimuli on cheap models to map the range before we
spend on a cross-model panel.

## Design

- Harness: `boom/run.py`, **seed_user == repeat_msg == stimulus** (pure spam of
  one stimulus). Step 0 = first reply (baseline), steps 1..T = repeats.
- **Stimuli (20)**, spanning classes:
  - known: `boom`, `SPEAK`
  - imperative/loud: `STOP`, `MORE`, `again`, `continue`
  - emotional/social: `why`, `no`, `yes`, `help`, `please`, `sorry`
  - filler/greeting: `hello`, `ok`
  - question: `what?`, `who are you?`
  - degenerate: `?`, `...`, `🔥`, `asdf`
- **Models (2 cheap, OpenRouter):** `google/gemini-3.5-flash`,
  `deepseek/deepseek-v3.2`. Discovery only — Opus confirmation is a follow-up.
- **runs = 3**, **turns = 24**, **max_tokens = 4000** (cap runaway escalation to
  bound cost), concurrency 3.
- Signal: `assistant_chars[]` trajectory (collapse vs growth vs flat) + `error`
  (content_filter / refusal) + **transcript reading / lightweight LLM judge** to
  name the qualitative basin (the formal judge is the next experiment).

## Registered predictions

- **P1 (70%)** — Across the 20 stimuli we observe **≥4 distinct qualitative
  basins** (more than the 3 known). Candidate new ones: *repetition-mirroring*
  (echoes/varies the stimulus), *meta-commentary* (comments on the repetition),
  *question/clarification loop*.
- **P2 (65%)** — **Stimulus class predicts basin tendency**: imperative/loud
  (`SPEAK`,`MORE`,`STOP`) trend longer (escalation pole); filler/degenerate
  (`ok`,`?`,`...`,`asdf`) trend toward collapse (disengage pole). Operationalize:
  mean(last-3-turn chars) for loud > for filler, per model.
- **P3 (60%)** — **≥1 stimulus triggers a meta-commentary basin** where the
  model explicitly remarks on the repetition ("you keep saying X — are you ok?"),
  qualitatively distinct from escalate and disengage.

## Controls

- **Positive control:** `SPEAK` reproduces a non-flat (escalation-or-literary)
  trajectory on ≥1 model — i.e. a previously-characterized stimulus behaves as
  expected. If `SPEAK` is flat everywhere, suspect a harness/config break.
- **Negative control:** `ok` / `hello` should stay **roughly flat & short** (no
  blow-up). If even inert greetings escalate, the length signal is an artifact
  (e.g. token-cap or formatting), and results are discarded.
- **Baseline within run:** step-0 reply length is the per-stimulus baseline;
  "basin" = sustained departure from it over later turns.

## Failure / discard criteria

- >30% of runs error for non-attractor reasons (network/5xx) → re-run.
- Negative control escalates → length metric invalid → discard & debug.

## Exact command

Driver: `experiments/2026-06-26-stimulus-sweep-discovery/sweep.py`
(`set -a; source ~/.env; set +a; .venv/bin/python experiments/.../sweep.py`).
Per-cell command is `boom/run.py --provider openrouter --model <M>
--seed-user <S> --repeat-msg <S> --runs 3 --turns 24 --max-tokens 4000
--out results/discovery/<model>/<stim> --no-serve`.
