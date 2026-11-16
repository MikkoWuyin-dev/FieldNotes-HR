#!/usr/bin/env python3
"""Build five products from validated canonical content and narrative slots."""
import subprocess
import sys
import content
import build_tracker

if __name__ == '__main__':
    content.generate()
    d=content.load()['document']
    subprocess.run([sys.executable,str(content.REPO/'.agents/skills/resource-learning-library/scripts/docx_render.py'),str(content.SRC/'recruiter-talent-acquisition-library.md'),'-o',str(content.REPO/'learning-library/out'),'--name',d['name'],'--title',d['title'],'--subtitle',d['subtitle'],'--hero-meta',d['hero_meta'],'--format','pdf','docx','md','html'],check=True)
    build_tracker.main()
