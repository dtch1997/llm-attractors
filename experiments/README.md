# Experiments

One experiment = one directory `experiments/<date>-<slug>/`.

| File | Contents |
|---|---|
| `spec.md` | Hypothesis, registered prediction(s) + confidence, design, **positive & negative controls**, cost estimate / tier. Written **before** the run — non-negotiable. |
| `status.md` | Optional append-only heartbeat for longer runs. |
| code / command | The exact `boom/run.py` invocation(s) — committed so the result reproduces. |
| `results/` | Raw + summarized outputs (lean `lengths.jsonl` / classification table committed; full transcripts → GCS). |
| `postmortem.md` | Results vs registered prediction; discovery-or-bug analysis for any surprise; next steps. |

## Rules (binding)

- Tier 0 < $10 runs freely; **$200 aggregate budget** (the real rail);
  3 strikes per hypothesis → escalate or drop.
- **Surprise always escalates:** any result contradicting a registered
  prediction gets a prominent flag in the postmortem.
- **Controls always**; an experiment that fails its controls is discarded
  before anyone sees the result.
- **Cost discipline**: discover on cheap models; confirm on Opus sparingly.

## The harness

`boom/run.py` — repeated-prompt attractor harness. Key knobs:
`--model --provider {auto,anthropic,openrouter} --system --seed-user
--repeat-msg --turns --runs --concurrency --max-tokens --out --no-serve`.
Signal logged per run: `assistant_chars[]` per turn + `error` (content_filter /
refusal / exception). Attractor outcome classified off `error` + the length
curve + an LLM judge (`boom/build_site.py`).
