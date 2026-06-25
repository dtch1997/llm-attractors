.PHONY: setup run figure

# Lightweight env: anthropic + matplotlib. Add the live dashboard with
#   uv pip install --python .venv -e ../stagehand
setup:
	uv venv .venv --python 3.11
	uv pip install --python .venv anthropic matplotlib

# A real sweep (needs ANTHROPIC_API_KEY). Override knobs: make run ARGS="--runs 4 --turns 80"
run:
	.venv/bin/python boom/run.py $(ARGS)

figure:
	.venv/bin/python boom/make_figure.py results/trajectories.jsonl figures/response_length.png
