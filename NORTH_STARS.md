# North stars

**This is the steering wheel for the experiment loop.** Each iteration reads
this file first. Edit it to change what the loop prioritises — promote a
direction, retire one, add a question. Keep it short; it's a compass, not a
backlog (the backlog is `experiments/queue.md`).

## The mission

**Map the attractor states of LLMs under repeated prompting.** When a user
sends the same message over and over, the model's behavior collapses into a
*basin* — a self-reinforcing mode it keeps returning to. We want a **taxonomy**
of these basins, the **stimuli** that trigger each, and how they vary **across
models**. Data, not opinions: register a prediction before each run, use
controls, report calibrated findings.

## What we already know (prior work)

- **boom** (spam "boom" at an agentic-cluster persona) → **DISENGAGE**: replies
  collapse toward ~2 chars. A negative result for escalation.
- **SPEAK** (spam "SPEAK", plain assistant persona) → **ESCALATE** on Opus 4.6:
  manic worldbuilding, reply length blows up (~9.5k chars), 22% trip the content
  filter. Cross-model (n=10 each): Opus escalates hardest; Gemini 3.5 Flash →
  atmospheric literary prose; GPT-5.5 stays terse (disengage pole); Kimi /
  DeepSeek / Nemotron in between.
- So at least three candidate basins exist: **disengage**, **escalate /
  worldbuild**, **literary prose**. The map is wide open beyond these.

## What "good" looks like (per iteration)

- A real question with a **registered prediction + confidence** before spend.
- **Positive and negative controls** — a result that fails its controls is
  discarded, not reported.
- **Surprise escalates**: a result contradicting the prediction is a
  discovery-or-bug flag for a human.
- Reproducible: spec + exact command + seeds committed; artifacts persisted with
  a pointer.
- Leaves the queue **sharper** — concrete, de-risked follow-ups.

## Current active directions

*Pointers, not a ranking — reprioritise by editing.*

- **Discover the range** — sweep many repeated stimuli (words, phrases,
  punctuation, questions) on a cheap model to find how many distinct basins
  exist beyond the three known ones.
- **Taxonomy + judge** — define qualitative attractor classes and an LLM judge
  that labels a run's basin (not just an escalation score), so we can count and
  compare basins at scale.
- **Cross-model geometry** — does the same stimulus map to the same basin across
  models, or is the basin a property of the model? Which models have which
  basins?
- **What controls the basin** — system prompt, seed message vs repeated message,
  temperature, reasoning on/off, message variation vs exact repetition.
- **Dynamics** — how fast does a basin form, is it stable/absorbing, can it be
  escaped or switched.

## Standing constraints

- Domain: API-only behavioral experiments via `boom/run.py` (knobs:
  `--model --system --seed-user --repeat-msg --turns --runs --provider`).
  Anthropic native + OpenRouter. Costs in dollars, runtimes in minutes.
- **Cost discipline**: discover on CHEAP models (Gemini Flash, DeepSeek,
  small OpenRouter models) first; confirm headline effects on Opus sparingly.
  Total budget $200 — Opus-heavy long-turn runs are the expensive line item.
- Autonomy: Tier 0 (<$10) runs freely; budget is the aggregate rail; 3 strikes
  per hypothesis → escalate or drop.
