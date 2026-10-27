"""Narrow inline favicon exception; vendored validation rules stay unchanged."""
from pathlib import Path
import sys
import unittest
from urllib.parse import unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'learning-library' / 'tools'))
import build_tracker as bt


class FaviconTests(unittest.TestCase):
    def test_svg_and_reference_colours(self):
        tag = bt.favicon_tag()
        uri = tag.split('href="', 1)[1].split('"', 1)[0]
        self.assertTrue(uri.startswith('data:image/svg+xml,'))
        svg = ET.fromstring(unquote(uri.split(',', 1)[1]))
        self.assertEqual(svg.attrib['viewBox'], '0 0 32 32')
        self.assertEqual([r.attrib['fill'] for r in svg],
                         ['#11142B', '#FFE168', '#65E8FF', '#FF4E91'])
        self.assertEqual(len(list(svg)), 4)

    def test_delivered_tracker_has_one_favicon(self):
        html = (ROOT / 'learning-library' / 'out' / 'roadmap-app.html').read_text()
        bt.assert_self_contained(html)
        self.assertNotIn('<link', bt.without_inline_favicon(html))

    def test_invalid_or_missing_favicon_rejected(self):
        html = (ROOT / 'learning-library' / 'out' / 'roadmap-app.html').read_text()
        tag = bt.favicon_tag()
        for modified in (html.replace(tag, ''), html.replace(tag, tag + tag),
                         html.replace(tag, '<link rel="icon" href="https://example.com/icon.svg">'),
                         html.replace(tag, tag.replace('<link ', '<link onload="alert(1)" ')),
                         html + '<link rel="stylesheet" href="https://example.com/style.css">',
                         html + '<link rel="icon" href="data:image/svg+xml,bad">'):
            with self.subTest(modified=modified[-100:]):
                with self.assertRaises(RuntimeError):
                    bt.assert_self_contained(modified)
