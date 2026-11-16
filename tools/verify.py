#!/usr/bin/env python3
"""One explicit full check, with shared core/browser scopes for CI.

Never rebuilds delivered outputs in place. Missing or failed required layers
cannot produce a successful full-verification exit code.
"""
from __future__ import annotations
import argparse
import os
from pathlib import Path
import subprocess
import sys
from environment import browser_problem

ROOT = Path(__file__).resolve().parents[1]


def plan(root=ROOT):
    py = root / '.venv/bin/python'
    return [
        ('environment', [sys.executable, '-B', 'tools/environment.py', 'ensure'], None),
        ('repository tests', [str(py), '-B', '-m', 'unittest', 'discover', '-s', 'tools', '-p', 'test_*.py', '-v'], 'environment'),
        ('fast checks', [str(py), '-B', 'tools/check.py', 'all'], 'environment'),
        ('output drift', [str(py), '-B', 'tools/check.py', 'drift'], 'environment'),
        ('browser checks', ['make', 'check-visual'], None),
    ]


def execute(argv, root):
    proc = subprocess.run(argv, cwd=root, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,
                          env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    print(proc.stdout, end='', flush=True)
    return proc.returncode, proc.stdout


def run(scope='all', *, root=ROOT, runner=execute, browser_ready=None):
    results = {}
    for name, argv, prerequisite in plan(root):
        selected = scope == 'all' or (name == 'browser checks') == (scope == 'browser')
        if not selected:
            results[name] = ('NOT RUN', 'outside requested partial scope')
            continue
        if prerequisite and results[prerequisite][0] == 'FAILED':
            results[name] = ('NOT RUN', 'environment failed')
            continue
        print(f'\n=== {name} ===', flush=True)
        try:
            problem = ''
            if name == 'browser checks':
                problem = browser_problem(root) if browser_ready is None else (
                    '' if browser_ready else 'node/npm/make unavailable; install supported tools')
            if problem:
                results[name] = ('NOT RUN', problem + '; rerun make verify')
                continue
            code, text = runner(argv, root)
            results[name] = ('FAILED' if code else 'WARNING' if '[WARN]' in text else 'PASSED',
                             f'exit {code}')
        except (OSError, subprocess.SubprocessError) as exc:
            results[name] = ('FAILED', str(exc))
        except KeyboardInterrupt:
            results[name] = ('FAILED', 'interrupted')
            for other, _, _ in plan(root):
                results.setdefault(other, ('NOT RUN', 'interrupted'))
            break
    print('\nVerification summary (scope: ' + scope + ')')
    for name, (state, detail) in results.items():
        print(f'[{state}] {name}: {detail}')
    required = [value for name, value in results.items()
                if scope == 'all' or (name == 'browser checks') == (scope == 'browser')]
    failed = any(state in ('FAILED', 'NOT RUN') for state, _ in required)
    if scope != 'all':
        print('PARTIAL SCOPE: this is not a full-verification claim.')
    print('RESULT: ' + ('INCOMPLETE/FAILED' if failed else
                       'COMPLETED WITH WARNINGS' if any(s == 'WARNING' for s, _ in required)
                       else 'PASSED') + (' (all required layers)' if scope == 'all' else ' (selected layers only)'))
    return int(failed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scope', choices=['all', 'core', 'browser'], default='all')
    return run(parser.parse_args().scope)


if __name__ == '__main__':
    raise SystemExit(main())
