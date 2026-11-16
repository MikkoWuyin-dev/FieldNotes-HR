#!/usr/bin/env python3
"""Read-only, offline-by-default diagnosis. Never installs or repairs tools."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from urllib.request import build_opener, HTTPRedirectHandler, ProxyHandler
from pathlib import Path

from environment import ROOT, command, inspect_environment, lock_digest, browser_problem


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, message, headers, newurl):
        return None  # A local identity probe must never follow an external redirect.


urlopen = build_opener(ProxyHandler({}), NoRedirect()).open


def protected(root=ROOT):
    failures = []
    inventory = root / 'tools/skill-hashes.sha256'
    expected = {}
    for line in inventory.read_text().splitlines():
        if line and not line.startswith('#'):
            digest, path = line.split('  ', 1)
            expected[path] = digest
    folder = root / '.agents/skills/resource-learning-library'
    actual = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts
              and p.suffix != '.pyc'}
    if actual != expected:
        failures.append('skill inventory differs (missing, changed or unexpected file)')
    pals = root / 'learning-library/src/pals'
    config = json.loads((pals / 'pals.json').read_text())
    if hashlib.sha256((pals / 'piixpal-payload.html').read_bytes()).hexdigest() != config['payload_sha256']:
        failures.append('Pals engine payload differs')
    # Read the approved pin from source without importing/executing the builder.
    builder = (root / 'learning-library/tools/build_tracker.py').read_text()
    pin = re.search(r'FAVICON_SHA256 = "([0-9a-f]{64})"', builder)
    tag = (root / 'learning-library/src/favicon-link.html').read_text().strip()
    if not pin or hashlib.sha256(tag.encode()).hexdigest() != pin[1]:
        failures.append('favicon source differs')
    return failures


def preview(port, root=ROOT):
    with urlopen(f'http://127.0.0.1:{port}/', timeout=3) as response:
        body = response.read(2_000_000)
        header = response.headers.get('X-FieldNotes-Artifact-SHA256')
    digest = hashlib.sha256(body).hexdigest()
    local = hashlib.sha256((root / 'learning-library/out/roadmap-app.html').read_bytes()).hexdigest()
    if digest != local or header != digest:
        raise ValueError('preview does not identify/serve the current local tracker; restart make preview')
    return f'local preview matches tracker SHA-256 {digest}; not a source-drift proof'


def diagnose(root=ROOT, port=None):
    rows = []
    def add(name, state, detail): rows.append((name, state, detail))
    def probe(name, fn):
        try: fn()
        except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
            add(name, 'FAILED', f'{exc}; inspect this item, no repair attempted')
    def git():
        branch = command(['git', 'branch', '--show-current'], cwd=root)
        if branch.returncode: raise ValueError('not a readable Git checkout')
        add('branch', 'PASSED' if branch.stdout.strip() else 'WARNING',
            branch.stdout.strip() or 'detached HEAD; follow session branch instructions')
        status = command(['git', 'status', '--short'], cwd=root)
        if status.returncode: raise ValueError('git status failed')
        # Filenames only, never read credentials or change contents.
        add('working tree', 'WARNING' if status.stdout else 'PASSED',
            status.stdout.strip() or 'clean')
        shallow = command(['git', 'rev-parse', '--is-shallow-repository'], cwd=root)
        if shallow.returncode: raise ValueError('cannot inspect history')
        add('history', 'WARNING' if shallow.stdout.strip() == 'true' else 'PASSED',
            'shallow: fetch full history before historical claims' if shallow.stdout.strip() == 'true' else 'full checkout')
    probe('git', git)
    add('system Python', 'PASSED' if sys.version_info >= (3, 11) else 'FAILED',
        sys.version.split()[0] + '; Python >=3.11 required; CI baseline 3.11')
    def node():
        problem = browser_problem(root)
        add('Node/npm', 'FAILED' if problem else 'PASSED',
            problem or 'supported Node/npm/make found; CI Node is 22.22.3')
    probe('Node/npm', node)
    for tool in ('make', 'git'):
        add(tool, 'PASSED' if shutil.which(tool) else 'FAILED', shutil.which(tool) or f'install {tool}')
    def env():
        issues = inspect_environment(root)
        add('Python environment', 'FAILED' if issues else 'PASSED',
            '; '.join(issues) if issues else 'pinned versions, imports and pip check agree')
        add('lock identity', 'PASSED', lock_digest(root))
    probe('Python environment', env)
    def hashes():
        issues = protected(root)
        add('protected files', 'FAILED' if issues else 'PASSED',
            '; '.join(issues) if issues else 'skill inventory, Pals payload and favicon pins agree')
    probe('protected files', hashes)
    out = root / 'learning-library/out'
    names = ['Recruiter-TA-Library.' + ext for ext in ('md','pdf','docx','html')] + ['roadmap-app.html']
    missing = [name for name in names if not (out / name).is_file()]
    add('outputs', 'FAILED' if missing else 'PASSED',
        'missing: ' + ', '.join(missing) + '; run make build' if missing else
        'all five exist; freshness NOT proved (run make verify)')
    if port is None:
        add('preview', 'NOT RUN', 'no requests made; opt in with --preview-port PORT to identify a running local server')
    else:
        probe('preview', lambda: add('preview', 'PASSED', preview(port, root)))
    add('external network/permissions', 'NOT RUN', 'offline by default; no provider/MCP/GitHub access or permission claims')
    for name, state, detail in rows:
        print(f'[{state}] {name}: {detail}')
    print('Doctor only: no installation, repair, source regeneration or product-test claim.')
    return int(any(state == 'FAILED' for _, state, _ in rows))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview-port', type=int, help='opt-in HTTP read on local loopback only')
    args = parser.parse_args()
    if args.preview_port is not None and not 1 <= args.preview_port <= 65535:
        parser.error('port must be 1..65535')
    return diagnose(port=args.preview_port)


if __name__ == '__main__':
    raise SystemExit(main())
