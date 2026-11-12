"""Verify selectable text, black text, contact data, and links after regeneration."""

from __future__ import annotations

import re
from zipfile import ZipFile
from xml.etree import ElementTree as ET

from pypdf import PdfReader

from document_common import PROFILE, ROOT, assert_black_pdf


def main():
    for name, count in [("ATS-Resume", 1), ("PH-Resume", 1), ("CV", 3)]:
        path = ROOT / f"public/resumes/Paul-John-Antigo-{name}.pdf"
        assert_black_pdf(path)
        reader = PdfReader(path)
        assert len(reader.pages) == count, f"Unexpected page count: {path}"
        text = " ".join(page.extract_text() for page in reader.pages)
        normalized = re.sub(r"\s+", " ", text)
        assert "AWS Certified" not in normalized, f"Unearned certification listed in {path}"
        assert len(text.split()) >= 240, f"Missing selectable text: {path}"
        for value in [PROFILE["name"].upper(), PROFILE["email"], PROFILE["phone"], "July 2027", "20 days"]:
            assert value.casefold() in normalized.casefold(), f"Missing {value}: {path}"
        for credential in PROFILE["credentials"]:
            for value in [credential["title"], credential["issuer"], credential["date"]]:
                assert value in normalized, f"Missing {value}: {path}"
            assert (ROOT / "public" / credential["credentialUrl"].lstrip("/")).is_file()
        urls = [a.get_object().get("/A", {}).get("/URI") for page in reader.pages for a in page.get("/Annots", [])]
        assert PROFILE["portfolio"] in urls
        assert PROFILE["linkedin"] in urls
        assert PROFILE["github"] in urls
        print(f"PASS {path.name}: {count} pages; selectable black text; consistent facts; {len(urls)} links")

    canonical = ROOT / "public/resumes/Paul-John-Antigo-ATS-Resume.pdf"
    assert canonical.read_bytes() == (ROOT / "public/Paul-John-Antigo-Resume.pdf").read_bytes()
    print("PASS legacy resume alias is identical to the standard ATS resume")

    ats_word = ROOT / "resume/Paul-John-Antigo-ATS-Resume-Editable.docx"
    template = ROOT / "resume/templates/ATS-Friendly-Resume-Template.docx"
    with ZipFile(ats_word) as output, ZipFile(template) as source:
        w = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        main = ET.fromstring(output.read("word/document.xml"))
        text = " ".join(t.text or "" for t in main.iter(w + "t"))
        for value in [PROFILE["name"], PROFILE["phone"], PROFILE["email"], "July 2027", "20 days"]:
            assert value in text, f"Missing ATS Word fact: {value}"
        for value in ["David Thompson", "Lorem ipsum", "AWS Certified", "Course completion; not Microsoft", "AI/documentation-assisted learning project;"]:
            assert value not in text, f"Unwanted ATS Word content: {value}"
        assert not list(main.iter(w + "tbl")), "ATS Word source must be single-column without tables"
        assert not list(main.iter(w + "drawing")), "ATS Word source must have no photo"
        assert len(list(main.iter(w + "numPr"))) == 7, "ATS bullets must retain real numbering"
        assert ET.tostring(main.find('.//' + w + 'sectPr')) == ET.tostring(ET.fromstring(source.read('word/document.xml')).find('.//' + w + 'sectPr'))
        for part in ["word/fontTable.xml", "word/theme/theme1.xml", "word/settings.xml", "word/webSettings.xml"]:
            assert output.read(part) == source.read(part), f"Unexpected template change: {part}"
        for name in output.namelist():
            if name.startswith('word/') and name.endswith('.xml'):
                for color in ET.fromstring(output.read(name)).iter(w + 'color'):
                    assert color.get(w + 'val') in ('000000', 'auto') and not color.get(w + 'themeColor')
        relationships = output.read('word/_rels/document.xml.rels').decode()
        for url in [PROFILE['phoneHref'], 'mailto:' + PROFILE['email'], PROFILE['portfolio'], PROFILE['linkedin'], PROFILE['github']]:
            assert url in relationships
        for credential in PROFILE['credentials']:
            assert credential['title'] in text and credential['date'] in text
            assert PROFILE['portfolio'].rstrip('/') + credential['credentialUrl'] in relationships
        print('PASS editable ATS: original template geometry/parts; real bullets; black text; verified content and links')

    word_path = ROOT / "resume/Paul-John-Antigo-CV-Editable.docx"
    with ZipFile(word_path) as archive:
        w = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        for name in archive.namelist():
            if name.startswith("word/") and name.endswith(".xml"):
                xml = ET.fromstring(archive.read(name))
                for color in xml.iter(w + "color"):
                    assert color.get(w + "val") in ("000000", "auto"), f"Colored DOCX text: {name}"
                    assert not color.get(w + "themeColor"), f"Themed DOCX color: {name}"
        doc = ET.fromstring(archive.read("word/document.xml"))
        text = " ".join(t.text or "" for t in doc.iter(w + "t"))
        assert PROFILE["phone"] in text and PROFILE["email"] in text
        relationships = archive.read("word/_rels/document.xml.rels").decode()
        assert PROFILE["phoneHref"] in relationships
        print("PASS editable CV: black OOXML styles/runs and clickable phone link")


if __name__ == "__main__":
    main()
