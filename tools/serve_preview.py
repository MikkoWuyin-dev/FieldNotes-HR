#!/usr/bin/env python3
"""Serve the built roadmap tracker for the Arena live preview.

Stdlib only: this must work even when ``.venv/`` and ``node_modules/`` have been
wiped by a sandbox reset. Bind to 0.0.0.0 (not 127.0.0.1) so the preview proxy
can reach it, and map ``/`` to roadmap-app.html instead of a directory listing.

Usage:
    python3 tools/serve_preview.py --port 8000

This file is deliberately NOT in ``tools/visual/.cache/``: that directory is
gitignored and excluded from workspace snapshots, so a previous server script
there disappeared on reset along with the running process.
"""
from __future__ import annotations

import argparse
import functools
import http.server
import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "learning-library" / "out"
TRACKER = "roadmap-app.html"
# Presence of this marker distinguishes the Pals build from the bare generator
# output. `out/` is snapshot-excluded, so a reset can silently restore the old
# committed file; say so loudly rather than serving a tracker without Pals.
PALS_MARKER = 'id="pals-payload"'


class Handler(http.server.SimpleHTTPRequestHandler):
    def _map_root(self) -> None:
        if self.path.split("?", 1)[0] in ("/", "/index.html"):
            self.path = "/" + TRACKER

    def do_GET(self) -> None:
        self._map_root()
        return super().do_GET()

    def do_HEAD(self) -> None:
        self._map_root()
        return super().do_HEAD()

    def end_headers(self) -> None:
        # A rebuild should be visible immediately, not hidden by a cache.
        self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()

    def log_message(self, fmt: str, *args) -> None:
        print(f"[preview] {self.address_string()} - {fmt % args}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8000")))
    args = parser.parse_args()

    tracker = OUT / TRACKER
    if not tracker.is_file():
        parser.error(f"missing {tracker}. Run 'make build' first.")
    body = tracker.read_text(encoding="utf-8")
    print(f"[preview] serving {OUT} on {args.host}:{args.port}", flush=True)
    print(f"[preview] / -> {TRACKER} ({tracker.stat().st_size} bytes)", flush=True)
    if PALS_MARKER not in body:
        print(
            "[preview] WARNING: tracker has no Pals payload — this looks like a "
            "stale build (out/ is snapshot-excluded). Run 'make build'.",
            flush=True,
        )

    handler = functools.partial(Handler, directory=str(OUT))
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    with http.server.ThreadingHTTPServer((args.host, args.port), handler) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
