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

.PHONY: help bootstrap build preview check check-drift check-visual links pin-skill clean ci doctor repair-env verify verify-core verify-browser

help: ## Show available targets
	@grep -hE '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

# --- environment -----------------------------------------------------------
bootstrap: ## Check/restore .venv: pinned versions, imports, dependency consistency
	python3 -B tools/environment.py ensure

repair-env: ## Transactionally recreate only .venv; restore old environment on failure
	python3 -B tools/environment.py repair

doctor: ## Read-only offline diagnosis (optional DOCTOR_ARGS="--preview-port 8000")
	python3 -B tools/doctor.py $(DOCTOR_ARGS)

# --- build -----------------------------------------------------------------
build: bootstrap ## Regenerate all 5 outputs from src/ (PDF/DOCX embed a new timestamp)
	$(PY) learning-library/tools/build_library.py
	@echo "Built. Run 'make check' and 'make check-drift' before committing."

# --- local preview ---------------------------------------------------------
# learning-library/out/ is excluded from workspace snapshots, so a reset can
# restore the committed (pre-Pals) tracker. Rebuild the tracker from source on
# every preview start. build_tracker.py is stdlib-only, so plain python3 works
# even when .venv/ has been wiped; no PDF/DOCX timestamp churn is introduced.
preview: ## Rebuild the tracker and serve it on 0.0.0.0:8000 for live preview
	python3 $(LIB)/tools/build_tracker.py
	python3 tools/serve_preview.py --port $(or $(PORT),8000)

# --- verification ----------------------------------------------------------
check: bootstrap ## Run every fast check (unit, validators, contract, sources, docs)
	$(PY) tools/check.py all

check-drift: bootstrap ## Prove all 5 committed outputs still reproduce from src/
	$(PY) tools/check.py drift

check-visual: ## Run the 13-viewport browser checks (needs npm; installs locally)
	cd tools/visual && npm ci --silent
	node tools/visual/visual_check.mjs

verify: ## Full verification; every required layer reported; incomplete runs fail
	python3 -B tools/verify.py

verify-core: ## CI/local core subset only (not a full-verification claim)
	python3 -B tools/verify.py --scope core

verify-browser: ## CI/local browser subset only (not a full-verification claim)
	python3 -B tools/verify.py --scope browser

ci: check check-drift ## Legacy fast + drift subset only; use make verify for full coverage

links: ## Sweep all cited URLs (needs general outbound network; best in CI)
	@bash $(LIB)/check-links.sh | tee link-status.tsv

pin-skill: bootstrap ## Re-record the vendored skill's SHA-256 inventory (intentional upgrades only)
	$(PY) tools/check.py pin-hashes

clean: ## Remove untracked build/runtime artefacts (keeps .venv)
	rm -rf .pytest_cache .mypy_cache .smoke-out link-status.tsv tools/visual/.cache
	find . -path ./.git -prune -o -path ./$(VENV) -prune -o \
		-name '__pycache__' -type d -print0 | xargs -0 -r rm -rf
