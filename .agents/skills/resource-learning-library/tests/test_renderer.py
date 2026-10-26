from __future__ import annotations

import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import docx_render  # noqa: E402
import interactive_app  # noqa: E402
import style_audit  # noqa: E402
import validate_build  # noqa: E402


class RendererSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = ROOT / "example" / "01-getting-started.md"
        cls.markdown = cls.source.read_text(encoding="utf-8")
        cls.blocks = docx_render.parse(cls.markdown)

    def test_parser_finds_supported_block_types(self) -> None:
        kinds = [block["type"] for block in self.blocks]
        self.assertIn("heading", kinds)
        self.assertIn("paragraph", kinds)
        self.assertIn("callout", kinds)
        self.assertIn("table", kinds)
        self.assertIn("list", kinds)
        self.assertIn("code", kinds)
        self.assertTrue(any(block.get("type") == "table" and len(block["rows"]) == 3 for block in self.blocks))

    def test_rendered_docx_html_and_pdf_pass_validators(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out_dir = Path(temp_dir)
            docx_path = docx_render.build_docx(
                self.blocks, out_dir / "Demo.docx", title="Demo", skip_first_h1=True
            )
            html_path = docx_render.build_html(
                self.blocks, out_dir / "Demo.html", title="Demo", skip_first_h1=True
            )
            pdf_path = docx_render.build_pdf(
                self.blocks, out_dir / "Demo.pdf", title="Demo", skip_first_h1=True
            )

            docx_errors, docx_notes = validate_build.validate_docx(docx_path)
            html_errors, html_notes = validate_build.validate_html(html_path)
            pdf_errors, pdf_notes = validate_build.validate_pdf(pdf_path)
            self.assertEqual(docx_errors, [], "\n".join(docx_errors + docx_notes))
            self.assertEqual(html_errors, [], "\n".join(html_errors + html_notes))
            self.assertEqual(pdf_errors, [], "\n".join(pdf_errors + pdf_notes))

            with zipfile.ZipFile(docx_path) as archive:
                document_xml = archive.read("word/document.xml").decode("utf-8")
                relationships = archive.read("word/_rels/document.xml.rels").decode("utf-8")
            self.assertNotIn("DEMO1", document_xml)
            self.assertIn("hyperlink", document_xml)
            self.assertIn("TargetMode=\"External\"", relationships)

            html_text = html_path.read_text(encoding="utf-8")
            self.assertNotIn("DEMO1", html_text)
            self.assertNotIn("<script", html_text.lower())
            self.assertNotIn("url(", html_text.lower())

    def test_interactive_app_is_inline_and_validated_in_app_mode(self) -> None:
        demo_path = ROOT / "example" / "interactive-demo.json"
        data = json.loads(demo_path.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as temp_dir:
            app_path = interactive_app.build_app(data, Path(temp_dir) / "index.html")
            errors, notes = validate_build.validate_html(app_path, allow_inline_script=True)
            self.assertEqual(errors, [], "\n".join(errors + notes))
            text = app_path.read_text(encoding="utf-8")
            self.assertIn("localStorage", text)
            self.assertIn("activityDates", text)
            self.assertIn("requestPermission", text)
            self.assertNotIn("<script src=", text.lower())
            self.assertNotIn("DEMO1", text)

    def test_interactive_data_cannot_close_the_inline_script(self) -> None:
        hostile = {"title": "</script><script>alert(1)</script>", "stages": []}
        with tempfile.TemporaryDirectory() as temp_dir:
            app_path = interactive_app.build_app(hostile, Path(temp_dir) / "safe.html")
            text = app_path.read_text(encoding="utf-8")
            self.assertNotIn("</script><script>alert(1)", text)
            self.assertIn(r"\u003c/script", text)

    def test_style_audit_and_output_name_guard(self) -> None:
        errors, _findings = style_audit.audit_text(self.markdown)
        self.assertEqual(errors, [])
        self.assertEqual(docx_render._safe_output_name("../Demo.docx"), "Demo")
        self.assertEqual(docx_render._safe_output_name("../../"), "resource-library")


if __name__ == "__main__":
    unittest.main()
