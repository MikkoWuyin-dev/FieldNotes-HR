#!/usr/bin/env python3
"""Stdlib-only environment inspection and explicitly requested maintenance.

Inspection never installs, writes stamps, creates a venv or calls the network.
Maintenance is confined to the literal repository .venv directory. A repair
keeps the old venv until its replacement passes inspection, restoring on error.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
IMPORTS = ('docx', 'reportlab', 'pypdf', 'PIL', 'lxml.etree')
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PIP_DISABLE_PIP_VERSION_CHECK='1',
           GIT_OPTIONAL_LOCKS='0', NPM_CONFIG_UPDATE_NOTIFIER='false')


def command(argv, *, cwd=ROOT, timeout=60):
    return subprocess.run([str(a) for a in argv], cwd=cwd, env=ENV,
                          capture_output=True, text=True, timeout=timeout)


def browser_problem(root=ROOT):
    """Local tool capability only: no install, browser launch or network."""
    for tool in ('node', 'npm', 'make'):
        if not shutil.which(tool):
            return f'{tool} unavailable; install Node >=22.12.0, npm and make (CI Node 22.22.3)'
    try:
        proc = command(['node', '--version'], cwd=root)
        match = re.fullmatch(r'v(\d+)\.(\d+)\.(\d+)\s*', proc.stdout)
        if proc.returncode or not match or tuple(map(int, match.groups())) < (22, 12, 0):
            return 'Node >=22.12.0 required; CI uses 22.22.3'
        if command(['npm', '--version'], cwd=root).returncode:
            return 'npm cannot execute; repair the Node/npm installation'
    except (OSError, subprocess.SubprocessError):
        return 'Node/npm capability check failed; repair the installation'
    return ''


def pins(root=ROOT):
    result = {}
    for line in (root / 'requirements.lock').read_text().splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            match = re.fullmatch(r'([\w.-]+)==([^\s;]+)', line)
            if not match:
                raise ValueError(f'Unsupported lock entry: {line}')
            result[match[1]] = match[2]
    if not result:
        raise ValueError('Lock contains no packages')
    return result


def inspect_environment(root=ROOT):
    """Return problems, without attempting to repair anything."""
    expected = pins(root)
    home = root / '.venv'
    if home.is_symlink():
        return ['.venv is a symlink; maintenance refuses it']
    if not home.exists():
        return ['.venv is missing; run make bootstrap']
    if not home.is_dir() or not (home / 'pyvenv.cfg').is_file():
        return ['.venv is unrecognized; inspect manually (maintenance refuses it)']
    python = home / 'bin/python'
    if not python.is_file():
        return ['venv interpreter missing; run make repair-env']
    script = '''import sys,json,importlib,importlib.metadata as m
expected=json.loads(sys.argv[1]); issues=[]
if sys.version_info < (3,11): issues.append('Python >=3.11 required')
if sys.prefix == sys.base_prefix: issues.append('interpreter is not isolated in a venv')
for name,version in expected.items():
 try:
  actual=m.version(name)
  if actual != version: issues.append(name+': expected '+version+', installed '+actual)
 except m.PackageNotFoundError: issues.append(name+': missing')
for name in json.loads(sys.argv[2]):
 try: importlib.import_module(name)
 except Exception as exc: issues.append(name+': import failed: '+str(exc))
print(json.dumps(issues))
'''
    try:
        proc = command([python, '-I', '-B', '-c', script, json.dumps(expected),
                        json.dumps(IMPORTS)], cwd=root)
        if proc.returncode:
            return ['venv interpreter failed; run make repair-env']
        issues = json.loads(proc.stdout)
        pip = command([python, '-I', '-B', '-m', 'pip', 'check'], cwd=root)
        if pip.returncode:
            issues.append('pip check failed: ' + (pip.stdout + pip.stderr).strip()[-1500:])
        return issues
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return ['venv inspection failed; run make repair-env']


def safe_home(root):
    home = root / '.venv'
    if home.is_symlink():
        raise RuntimeError('Refusing symlink .venv; no files changed')
    if home.exists() and (not home.is_dir() or not (home / 'pyvenv.cfg').is_file()):
        raise RuntimeError('Refusing unrecognized .venv; inspect it manually, no files changed')
    return home


@contextmanager
def maintenance_lock(root):
    lock = root / '.venv-maintenance.lock'
    try:
        lock.mkdir()
    except FileExistsError:
        raise RuntimeError('Environment maintenance lock exists. Check for another operation; '
                           'remove only the empty stale lock directory after inspection.')
    try:
        yield
    finally:
        lock.rmdir()


def install(root=ROOT, *, recreate=False):
    if sys.version_info < (3, 11):
        raise RuntimeError('Use Python >=3.11 (CI uses 3.11)')
    pins(root)  # Validate the lock before any modification.
    with maintenance_lock(root):
        home = safe_home(root)
        backup = root / '.venv.repair-backup'
        if backup.exists() or backup.is_symlink():
            raise RuntimeError('Repair backup already exists; inspect it manually, no files changed')
        if not recreate and not inspect_environment(root):
            print('Environment healthy: lock versions, imports and pip check agree.')
            return
        existed = home.exists()
        # Any unhealthy environment is replaced transactionally, not patched blindly.
        if existed:
            home.rename(backup)
        try:
            subprocess.run([sys.executable, '-B', '-m', 'venv', str(home)],
                           cwd=root, env=ENV, check=True)
            subprocess.run([str(home / 'bin/python'), '-I', '-B', '-m', 'pip',
                            'install', '-r', str(root / 'requirements.lock')],
                           cwd=root, env=ENV, check=True)
            issues = inspect_environment(root)
            if issues:
                raise RuntimeError('; '.join(issues))
        except BaseException:
            if home.exists() and not home.is_symlink():
                shutil.rmtree(home)
            if existed:
                backup.rename(home)
            raise
        else:
            if existed:
                shutil.rmtree(backup)
            print('Environment ready: pinned versions, imports and pip check passed.')


def lock_digest(root=ROOT):
    return hashlib.sha256((root / 'requirements.lock').read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['inspect', 'ensure', 'repair'])
    args = parser.parse_args()
    try:
        if args.action == 'inspect':
            issues = inspect_environment()
            print('\n'.join(issues) if issues else 'Environment healthy')
            return int(bool(issues))
        install(recreate=args.action == 'repair')
        return 0
    except (RuntimeError, ValueError, OSError, subprocess.SubprocessError) as exc:
        print(f'Environment maintenance FAILED: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
