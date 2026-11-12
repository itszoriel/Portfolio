"""Shared, evidence-based profile and black-text PDF helpers."""

from __future__ import annotations

import json
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle

ROOT = Path(__file__).resolve().parents[1]
PROFILE = json.loads((ROOT / "src/data/profile.json").read_text(encoding="utf-8"))
BLACK = colors.black


def plain(text: str) -> str:
    return text.replace("–", "-").replace("—", "-").replace("’", "'")


def link(label: str, url: str) -> str:
    return f'<link href="{escape(url, {chr(34): "&quot;"})}" color="#000000">{escape(plain(label))}</link>'


def certificate_title(credential: dict) -> str:
    prefix = credential["kicker"]
    return f'{prefix}: {credential["title"]}' if prefix else credential["title"]


def certificate_url(credential: dict) -> str:
    return PROFILE["portfolio"].rstrip("/") + credential["credentialUrl"]


def pdf_style(name: str, *, size=10, leading=12.5, bold=False, **kwargs) -> ParagraphStyle:
    return ParagraphStyle(
        name, fontName="Helvetica-Bold" if bold else "Helvetica",
        fontSize=size, leading=leading, textColor=BLACK,
        bulletFontName="Helvetica", bulletFontSize=size, bulletColor=BLACK, **kwargs,
    )


def assert_black_pdf(path: Path) -> None:
    """Fail regeneration if text color, phone, or certificate links regress."""
    from pypdf import PdfReader
    from pypdf.generic import ContentStream

    reader = PdfReader(path)
    text = "\n".join(page.extract_text() for page in reader.pages)
    if PROFILE["phone"] not in text:
        raise ValueError(f"Missing canonical phone number in {path}")
    urls = {
        str(annotation.get_object().get("/A", {}).get("/URI", ""))
        for page in reader.pages for annotation in page.get("/Annots", [])
    }
    for url in [PROFILE["phoneHref"], f'mailto:{PROFILE["email"]}'] + [certificate_url(c) for c in PROFILE["credentials"]]:
        if url not in urls:
            raise ValueError(f"Missing clickable link {url} in {path}")
    for page in reader.pages:
        fill = (0.0,)
        stack = []
        for operands, operator in ContentStream(page.get_contents(), reader).operations:
            if operator == b"q":
                stack.append(fill)
            elif operator == b"Q":
                fill = stack.pop()
            elif operator in (b"g", b"rg"):
                fill = tuple(float(value) for value in operands)
            elif operator == b"k":
                c, m, y, k = (float(value) for value in operands)
                fill = (1 - min(1, c + k), 1 - min(1, m + k), 1 - min(1, y + k))
            elif operator in (b"Tj", b"TJ", b"'", b'"') and any(value != 0 for value in fill):
                raise ValueError(f"Non-black text in {path}: {fill}")


def blacken_docx(path: Path) -> None:
    """Normalize every Word style, including unused template and effect styles."""
    from io import BytesIO
    from zipfile import ZipFile, ZIP_DEFLATED
    from lxml import etree

    namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    source = BytesIO(path.read_bytes())
    with ZipFile(source) as archive, ZipFile(path, "w", ZIP_DEFLATED) as output:
        for entry in archive.infolist():
            blob = archive.read(entry.filename)
            if entry.filename.startswith("word/") and entry.filename.endswith(".xml"):
                root = etree.fromstring(blob)
                changed = False
                for color in root.iter(namespace + "color"):
                    if color.get(namespace + "val") != "000000" or any(color.get(namespace + key) for key in ("themeColor", "themeTint", "themeShade")):
                        changed = True
                    color.set(namespace + "val", "000000")
                    for attribute in ("themeColor", "themeTint", "themeShade"):
                        color.attrib.pop(namespace + attribute, None)
                if changed:
                    blob = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
            output.writestr(entry, blob)
