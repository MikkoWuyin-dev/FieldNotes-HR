"""Phase 1 safety/coverage tests: use temporary roots, never repair the real repo."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import environment as env
import doctor
import verify


class EnvironmentTests(unittest.TestCase):
    def fixture(self, root):
        (root / 'requirements.lock').write_text('example==1.0\n')
        home = root / '.venv'
        home.mkdir()
        (home / 'pyvenv.cfg').write_text('home = fixture\n')
        (home / 'old-state').write_text('preserve me')
        (root / 'source.txt').write_text('never touch')
        return home

    def test_cli_entry_point_uses_real_install_signature(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);self.fixture(root)
            # Exercise the public default-root path, not only explicit fixture roots.
            with patch.object(env, 'inspect_environment', return_value=[]), \
                 patch.object(env, 'safe_home', return_value=root/'.venv'), \
                 patch.object(env, 'maintenance_lock', return_value=contextlib.nullcontext()), \
                 patch.object(env, 'pins', return_value={'example':'1'}):
                env.install()

    def test_lock_changes_are_read_each_time(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'requirements.lock').write_text('example==1\n')
            self.assertEqual(env.pins(root), {'example':'1'})
            (root / 'requirements.lock').write_text('example==2\n')
            self.assertEqual(env.pins(root), {'example':'2'})

    def test_missing_environment_is_reported_without_creation(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); (root / 'requirements.lock').write_text('example==1\n')
            self.assertTrue(env.inspect_environment(root))
            self.assertFalse((root / '.venv').exists())

    def test_repair_failure_restores_old_environment_and_source(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); home = self.fixture(root)
            def broken(*a, **k):
                home.mkdir(); (home / 'partial').write_text('incomplete')
                raise subprocess.CalledProcessError(1, 'venv')
            with patch.object(env.subprocess, 'run', side_effect=broken):
                with self.assertRaises(subprocess.CalledProcessError):env.install(root, recreate=True)
            self.assertEqual((home / 'old-state').read_text(), 'preserve me')
            self.assertEqual((root / 'source.txt').read_text(), 'never touch')
            self.assertFalse((root / '.venv.repair-backup').exists())
            self.assertFalse((root / '.venv-maintenance.lock').exists())

    def test_existing_unhealthy_environment_is_replaced(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); home = self.fixture(root)
            def fake(*a, **k):
                if not home.exists():home.mkdir()
            with patch.object(env, 'inspect_environment', side_effect=[['missing package'], []]), \
                 patch.object(env.subprocess, 'run', side_effect=fake) as run:
                env.install(root)
            self.assertEqual(run.call_count, 2)
            self.assertFalse((home / 'old-state').exists())
            self.assertEqual((root / 'source.txt').read_text(), 'never touch')

    def test_healthy_environment_does_not_install(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); self.fixture(root)
            with patch.object(env, 'inspect_environment', return_value=[]), \
                 patch.object(env.subprocess, 'run') as run:
                env.install(root)
            run.assert_not_called()

    def test_refuses_unrecognized_directory_and_symlink(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); (root / 'requirements.lock').write_text('example==1\n')
            home = root / '.venv'; home.mkdir(); (home / 'important').write_text('source')
            with self.assertRaises(RuntimeError):env.install(root, recreate=True)
            self.assertEqual((home / 'important').read_text(), 'source')
            (home / 'important').unlink(); home.rmdir()
            elsewhere = root / 'elsewhere'; elsewhere.mkdir()
            home.symlink_to(elsewhere, target_is_directory=True)
            with self.assertRaises(RuntimeError):env.install(root, recreate=True)
            self.assertTrue(elsewhere.is_dir())

    def test_refuses_existing_backup(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); home = self.fixture(root)
            (root / '.venv.repair-backup').mkdir()
            with self.assertRaises(RuntimeError):env.install(root, recreate=True)
            self.assertTrue((home / 'old-state').exists())


class VerificationTests(unittest.TestCase):
    def run_quietly(self, **kw):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):code = verify.run(**kw)
        return code, out.getvalue()

    def test_missing_browser_is_incomplete_not_success(self):
        code, text = self.run_quietly(runner=lambda *a:(0,''), browser_ready=False)
        self.assertEqual(code, 1); self.assertIn('[NOT RUN] browser checks', text)
        self.assertIn('INCOMPLETE/FAILED', text)

    def test_bootstrap_failure_skips_python_but_still_runs_browser(self):
        calls=[]
        def runner(argv, root):
            calls.append(argv);return (1,'') if len(calls)==1 else (0,'')
        code,text=self.run_quietly(runner=runner,browser_ready=True)
        self.assertEqual(code,1);self.assertEqual(len(calls),2)
        self.assertIn('[NOT RUN] repository tests',text)
        self.assertIn('[PASSED] browser checks',text)

    def test_failure_does_not_hide_later_layers(self):
        calls=[]
        def runner(argv, root):
            calls.append(argv);return (1,'') if len(calls)==2 else (0,'')
        code,text=self.run_quietly(runner=runner,browser_ready=True)
        self.assertEqual(code,1);self.assertEqual(len(calls),5)
        self.assertIn('[PASSED] output drift',text)

    def test_warnings_and_partial_scopes_are_explicit(self):
        code,text=self.run_quietly(runner=lambda *a:(0,'[WARN] research gaps'),browser_ready=True)
        self.assertEqual(code,0);self.assertIn('COMPLETED WITH WARNINGS',text)
        code,text=self.run_quietly(scope='core',runner=lambda *a:(0,''),browser_ready=False)
        self.assertEqual(code,0);self.assertIn('PARTIAL SCOPE',text)
        self.assertIn('[NOT RUN] browser checks',text)

    def test_all_layers_pass(self):
        code,text=self.run_quietly(runner=lambda *a:(0,''),browser_ready=True)
        self.assertEqual(code,0);self.assertIn('PASSED (all required layers)',text)


class DoctorTests(unittest.TestCase):
    def test_offline_doctor_does_not_probe_network_or_write(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'requirements.lock').write_text('example==1\n')
            before={str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file()}
            def fake(argv, **kw):
                value='branch\n' if 'branch' in argv else 'false\n' if '--is-shallow-repository' in argv else ''
                return subprocess.CompletedProcess(argv,0,value,'')
            with patch.object(doctor,'command',side_effect=fake), \
                 patch.object(doctor,'protected',return_value=[]), \
                 patch.object(doctor,'inspect_environment',return_value=['missing']), \
                 patch.object(doctor,'urlopen') as network, contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(doctor.diagnose(root),1)
            network.assert_not_called()
            self.assertEqual(before,{str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file()})

    def test_preview_probe_never_follows_redirects(self):
        self.assertIsNone(doctor.NoRedirect().redirect_request(None,None,302,'Found',{},'https://example.com'))

    def test_protected_inventory_matches_real_repo(self):
        self.assertEqual(doctor.protected(),[])

    def test_preview_requires_both_identity_and_content(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);out=root/'learning-library/out';out.mkdir(parents=True)
            (out/'roadmap-app.html').write_bytes(b'current')
            class Response:
                headers={'X-FieldNotes-Artifact-SHA256':hashlib.sha256(b'old').hexdigest()}
                def read(self, size):return b'old'
                def __enter__(self):return self
                def __exit__(self,*a):pass
            with patch.object(doctor,'urlopen',return_value=Response()):
                with self.assertRaises(ValueError):doctor.preview(8000,root)


class CurrentDocsTests(unittest.TestCase):
    def test_stale_current_counts_fail_but_dated_history_is_allowed(self):
        import check
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            for folder in ('docs','learning-library/src'):(root/folder).mkdir(parents=True,exist_ok=True)
            data={'stages':[{'estimated_hours':3,'resources':[{'url':'https://example.com'}]}]}
            (root/'learning-library/src/roadmap-app.json').write_text(json.dumps(data))
            summary='1 stages, 1 resource cards, 1 distinct card URLs, 3 planned hours.'
            for rel in ('README.md','docs/SETUP.md','learning-library/README.md'):
                (root/rel).write_text(summary+'\nHistorical: 26 cards in the initial release.')
            self.assertEqual(check.current_doc_problems(root),[])
            (root/'docs/SETUP.md').write_text(summary.replace('1 resource cards','26 resource cards'))
            self.assertTrue(check.current_doc_problems(root))

    def test_preview_identifies_actual_bytes_on_get_and_head(self):
        import functools
        import http.server
        import threading
        from urllib.request import urlopen, Request
        import serve_preview
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);out=root/'learning-library/out';out.mkdir(parents=True)
            body=b'current tracker';(out/'roadmap-app.html').write_bytes(body)
            handler=functools.partial(serve_preview.Handler,directory=str(out))
            with patch.object(serve_preview,'OUT',out):
                server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler)
                thread=threading.Thread(target=server.serve_forever);thread.start()
                try:
                    digest=hashlib.sha256(body).hexdigest()
                    for method in ('GET','HEAD'):
                        with urlopen(Request(f'http://127.0.0.1:{server.server_port}/',method=method)) as reply:
                            self.assertEqual(reply.headers['X-FieldNotes-Artifact-SHA256'],digest)
                    self.assertIn(digest,doctor.preview(server.server_port,root))
                finally:
                    server.shutdown();thread.join();server.server_close()


class CapabilityTests(unittest.TestCase):
    def test_old_node_is_not_supported(self):
        with patch.object(env.shutil,'which',return_value='/tool'), \
             patch.object(env,'command',return_value=subprocess.CompletedProcess([],0,'v20.0.0\n','')):
            self.assertIn('Node >=22.12.0',env.browser_problem())

    def test_ci_uses_the_shared_scopes(self):
        workflow=(env.ROOT/'.github/workflows/verify.yml').read_text()
        self.assertIn('run: make verify-core',workflow)
        self.assertIn('run: make verify-browser',workflow)
        self.assertEqual([name for name,_,_ in verify.plan()],
                         ['environment','repository tests','fast checks','output drift','browser checks'])
