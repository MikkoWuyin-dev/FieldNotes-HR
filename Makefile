# FieldNotes-HR — reproducible environment and verification.
# All targets are safe to run from the repository root.
# See docs/SETUP.md for the full narrative.

SHELL := /bin/bash
.DEFAULT_GOAL := help

VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/python -m pip
SKILL := .agents/skills/resource-learning-library
LIB := learning-library
SRC := $(LIB)/src
OUT := $(LIB)/out

TITLE := From zero to first recruiter role
SUBTITLE := A roadmap-ordered learning library for an absolute beginner
HERO_META := Lagos, Nigeria - verified 26 October 2026 - about 94 hours over 20 weeks
NAME := Recruiter-TA-Library

.PHONY: help bootstrap build check check-drift check-visual links pin-skill clean ci

help: ## Show available targets
	@grep -hE '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

# --- environment -----------------------------------------------------------
$(PY):
	python3 -m venv $(VENV)
	$(PIP) install --quiet --upgrade pip
	$(PIP) install --quiet -r requirements.lock

bootstrap: $(PY) ## Create .venv and install the pinned dependency tree
	@$(PY) --version

# --- build -----------------------------------------------------------------
build: $(PY) ## Regenerate all 5 outputs from src/ (PDF/DOCX embed a new timestamp)
	$(PY) $(SKILL)/scripts/docx_render.py $(SRC)/recruiter-talent-acquisition-library.md \
		-o $(OUT) --name $(NAME) \
		--title "$(TITLE)" --subtitle "$(SUBTITLE)" --hero-meta "$(HERO_META)" \
		--format pdf docx md html
	$(PY) $(LIB)/tools/build_tracker.py
	@echo "Built. Run 'make check' and 'make check-drift' before committing."

# --- verification ----------------------------------------------------------
check: $(PY) ## Run every fast check (unit, validators, contract, sources, docs)
	$(PY) tools/check.py all

check-drift: $(PY) ## Prove all 5 committed outputs still reproduce from src/
	$(PY) tools/check.py drift

check-visual: ## Run the 13-viewport browser checks (needs npm; installs locally)
	cd tools/visual && npm ci --silent
	node tools/visual/visual_check.mjs

ci: check check-drift ## Everything CI runs (no browser required)

links: ## Sweep all cited URLs (needs general outbound network; best in CI)
	@bash $(LIB)/check-links.sh | tee link-status.tsv

pin-skill: ## Re-record the vendored skill's SHA-256 inventory (intentional upgrades only)
	$(PY) tools/check.py pin-hashes

clean: ## Remove untracked build/runtime artefacts (keeps .venv)
	rm -rf .pytest_cache .mypy_cache .smoke-out link-status.tsv tools/visual/.cache
	find . -path ./.git -prune -o -path ./$(VENV) -prune -o \
		-name '__pycache__' -type d -print0 | xargs -0 -r rm -rf
