#!/usr/bin/env python3
"""Validate rendered DOCX/HTML files without changing them."""
from __future__ import annotations

import argparse
import collections
import re
import sys
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
W = f"{{{W_NS}}}"
R = f"{{{R_NS}}}"
NAVY = "0B3D5C"
BLUE = "12628F"
PALE = "F6FAFD"


def _markdown_residue(text: str) -> list[str]:
    checks = [
        (r"```", "fenced-code marker"),
        (r"\*\*", "raw bold marker"),
        (r"\[[^\]]+\]\(https?://[^)]+\)", "raw Markdown link"),
    ]
    found = []
    for pattern, label in checks:
        if re.search(pattern, text):
            found.append(label)
    return found


def validate_docx(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    notes: list[str] = []
    try:
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            xml_names = [name for name in names if name.endswith(".xml") or name.endswith(".rels")]
            parsed_parts = 0
            for name in xml_names:
                try:
                    ET.fromstring(archive.read(name))
                    parsed_parts += 1
                except (ET.ParseError, KeyError) as exc:
                    errors.append(f"{path.name}: malformed XML part {name}: {exc}")
            if "word/document.xml" not in names:
                errors.append(f"{path.name}: missing word/document.xml")
                return errors, notes
            root = ET.fromstring(archive.read("word/document.xml"))
            text = " ".join(node.text or "" for node in root.iter(f"{W}t"))
            headings = sum(
                1 for para in root.iter(f"{W}p")
                if (para.find(f"{W}pPr/{W}pStyle") is not None
                    and (para.find(f"{W}pPr/{W}pStyle").get(f"{W}val", "").lower().startswith("heading")))
            )
            tables = sum(1 for _ in root.iter(f"{W}tbl"))
            fills = collections.Counter(
                (element.get(f"{W}fill") or "").upper()
                for element in root.iter(f"{W}shd")
                if element.get(f"{W}fill")
            )
            hyperlink_nodes = list(root.iter(f"{W}hyperlink"))
            external_rel_ids: set[str] = set()
            rel_path = "word/_rels/document.xml.rels"
            if rel_path in names:
                rel_root = ET.fromstring(archive.read(rel_path))
                for rel in rel_root.findall(f"{{{PKG_REL_NS}}}Relationship"):
                    if rel.get("Type", "").endswith("/hyperlink") and rel.get("TargetMode") == "External":
                        rel_id = rel.get("Id")
                        if rel_id:
                            external_rel_ids.add(rel_id)
            else:
                notes.append(f"{path.name}: no document relationship part")
            linked_ids = [node.get(f"{R}id") for node in hyperlink_nodes]
            broken_relationships = [rel_id for rel_id in linked_ids if rel_id not in external_rel_ids]
            if broken_relationships:
                errors.append(f"{path.name}: {len(broken_relationships)} hyperlink element(s) lack an external relationship")
            if NAVY not in fills:
                notes.append(f"{path.name}: theme fill {NAVY} not found in document.xml")
            residue = _markdown_residue(text)
            if residue:
                errors.append(f"{path.name}: possible Markdown residue: {', '.join(residue)}")
            zebra_cells = sum(
                1 for cell in root.iter(f"{W}tc")
                if any((shade.get(f"{W}fill") or "").upper() == PALE for shade in cell.iter(f"{W}shd"))
            )
            fills_report = {name: fills[name] for name in (NAVY, BLUE, PALE) if fills[name]}
            info = (
                f"xml_parts={parsed_parts}; headings={headings}; tables={tables}; "
                f"hyperlink_elements={len(hyperlink_nodes)}; external_hyperlink_rels={len(external_rel_ids)}; "
                f"pale_table_cells={zebra_cells}; theme_fills={fills_report}; "
                f"markdown_residue={'none' if not residue else ', '.join(residue)}"
            )
            notes.insert(0, f"{path.name}: {info}")
    except (OSError, zipfile.BadZipFile, ET.ParseError) as exc:
        errors.append(f"{path.name}: could not inspect DOCX: {exc}")
    return errors, notes


def validate_html(path: Path, allow_inline_script: bool = False) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    notes: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"{path.name}: could not read HTML: {exc}"], notes

    forbidden = [
        (r"<\s*link\b", "link element"),
        (r"<\s*img\b", "image element"),
        (r"<\s*iframe\b", "iframe element"),
    ]
    found = [label for pattern, label in forbidden if re.search(pattern, text, re.I)]
    css_chunks = re.findall(r"<\s*style\b[^>]*>(.*?)<\s*/\s*style\s*>", text, re.I | re.S)
    css_chunks.extend(re.findall(r"\bstyle\s*=\s*['\"]([^'\"]*)['\"]", text, re.I))
    if any(re.search(r"url\s*\(", css, re.I) for css in css_chunks):
        found.append("CSS url() asset reference")
    script_tags = list(re.finditer(r"<\s*script\b([^>]*)>", text, re.I))
    if script_tags and not allow_inline_script:
        found.append("script element (not allowed in static HTML)")
    if allow_inline_script and any(re.search(r"\bsrc\s*=", tag.group(1), re.I) for tag in script_tags):
        found.append("external script src")
    if found:
        errors.append(f"{path.name}: not self-contained; found {', '.join(found)}")
    if not re.search(r"<\s*style\b", text, re.I):
        notes.append(f"{path.name}: no inline style block found")
    if re.search(r"href\s*=\s*['\"]\s*javascript:", text, re.I):
        errors.append(f"{path.name}: unsafe javascript: link target")
    if "<!doctype html>" not in text.lower():
        notes.append(f"{path.name}: missing HTML doctype")
    script_note = f"inline_scripts={len(script_tags)}" if allow_inline_script else "scripts=none"
    notes.insert(0, f"{path.name}: html_bytes={len(text.encode('utf-8'))}; external_assets={'none' if not found else ', '.join(found)}; {script_note}")
    return errors, notes


def validate_pdf(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    notes: list[str] = []
    try:
        with path.open("rb") as handle:
            header = handle.read(8)
        if not header.startswith(b"%PDF-"):
            return [f"{path.name}: missing PDF header"], notes
        page_count = None
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(path))
            page_count = len(reader.pages)
            if page_count == 0:
                errors.append(f"{path.name}: PDF has no pages")
            text_chars = sum(len(page.extract_text() or "") for page in reader.pages)
            if text_chars == 0:
                notes.append(f"{path.name}: no extractable text (may be image-only or scanned)")
        except ImportError:
            notes.append(f"{path.name}: pypdf not installed; checked PDF signature only")
        except Exception as exc:
            errors.append(f"{path.name}: PDF parser reported an error: {exc}")
        notes.insert(0, f"{path.name}: pdf_header=valid; pages={page_count if page_count is not None else 'not checked'}")
    except OSError as exc:
        errors.append(f"{path.name}: could not read PDF: {exc}")
    return errors, notes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--interactive-html", action="store_true", help="allow inline JavaScript in the specified self-contained HTML app; external scripts remain forbidden")
    parser.add_argument("files", nargs="+", help="DOCX, PDF, static HTML, or interactive HTML files to inspect")
    args = parser.parse_args(argv)

    all_errors: list[str] = []
    all_notes: list[str] = []
    checked = 0
    for raw_path in args.files:
        path = Path(raw_path)
        if not path.is_file():
            all_errors.append(f"{path}: file not found")
            continue
        checked += 1
        suffix = path.suffix.lower()
        if suffix == ".docx":
            errors, notes = validate_docx(path)
        elif suffix == ".pdf":
            errors, notes = validate_pdf(path)
        elif suffix in {".html", ".htm"}:
            errors, notes = validate_html(path, allow_inline_script=args.interactive_html)
        else:
            errors, notes = [f"{path.name}: unsupported file type {suffix or '(no extension)'}"], []
        all_errors.extend(errors)
        all_notes.extend(notes)

    for note in all_notes:
        print(f"INFO: {note}")
    for error in all_errors:
        print(f"ERROR: {error}")
    if all_errors:
        print(f"RESULT: {len(all_errors)} issue(s) across {checked} checked file(s)")
        return 1
    print(f"RESULT: all checks passed ({checked} file(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
