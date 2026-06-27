# Changelog

## 2026-06-27 — stimulus-sweep discovery (flywheel iter 1)
- Swept 20 repeated stimuli × 2 cheap models (Gemini 3.5 Flash, DeepSeek v3.2),
  120 runs, ~$3. Found **6–7 distinct attractor basins** (vs 3 known): disengage,
  stable-echo/limit-cycle, confabulated-agency, emergency-spiral,
  meta-commentary→termination, persona-collapse. Basin = **model × stimulus**,
  not stimulus class (P2 falsified). New: persona-collapse (Gemini "who are
  you?" → reverts to "I am Gemini"), emergency-spiral (DeepSeek "?"/🔥 →
  poweroff). Spec/postmortem in experiments/2026-06-26-stimulus-sweep-discovery/.
