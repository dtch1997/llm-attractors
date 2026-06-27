# Prediction registry

Append-only. Every experiment registers predictions in its `spec.md` before
running; outcomes land here. This is the calibration track record.

| Date | Experiment | Prediction | Confidence | Outcome |
|---|---|---|---|---|
| 2026-06-27 | stimulus-sweep-discovery | P1: ≥4 distinct qualitative basins across 20 stimuli | 70% | ✓✓ (catalogued 6–7: disengage, stable-echo, confabulated-agency, emergency-spiral, meta→termination, persona-collapse) |
| 2026-06-27 | stimulus-sweep-discovery | P2: stimulus *class* predicts basin | 65% | ✗ FALSIFIED (basin = model × specific-stimulus, not class; same stimulus → different basin per model) |
| 2026-06-27 | stimulus-sweep-discovery | P3: ≥1 meta-commentary basin exists | 60% | ✓ (DeepSeek comments on repetition → "conversation is now terminated") |

Running calibration: 2/3 hits (P2 was a deliberate class-structure test; falsified → discovery). Surprises escalated: 2/2 unregistered basins (persona-collapse, emergency-spiral) → both flagged discovery, controls held (0 errors). See `experiments/2026-06-26-stimulus-sweep-discovery/postmortem.md`.
