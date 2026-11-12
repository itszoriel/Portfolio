"""Fill a copy of the supplied ATS Word template, preserving its package design."""

from __future__ import annotations

from copy import deepcopy
from zipfile import ZipFile, ZIP_DEFLATED

from lxml import etree

from document_common import PROFILE as P, ROOT, blacken_docx, certificate_url, plain

TEMPLATE_PATH = ROOT / "resume/templates/ATS-Friendly-Resume-Template.docx"
OUTPUT_PATH = ROOT / "resume/Paul-John-Antigo-ATS-Resume-Editable.docx"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
REL = "{http://schemas.openxmlformats.org/package/2006/relationships}"
XML = "{http://www.w3.org/XML/1998/namespace}"


def build_ats_docx():
    from build_resumes import PROJECT_CONTEXT, SKILLS

    with ZipFile(TEMPLATE_PATH) as source:
        parts = {entry.filename: (entry, source.read(entry.filename)) for entry in source.infolist()}
    root = etree.fromstring(parts["word/document.xml"][1])
    body = root.find(W + "body")
    patterns = [deepcopy(p) for p in body.findall(W + "p")]
    section = deepcopy(body.find(W + "sectPr"))
    body.clear()
    relationships = etree.fromstring(parts["word/_rels/document.xml.rels"][1])
    next_relationship = 100

    def paragraph(index, *, before=0, after=3, centered=False):
        p = deepcopy(patterns[index])
        for child in list(p):
            if child.tag != W + "pPr":
                p.remove(child)
        properties = p.find(W + "pPr")
        if properties is None:
            properties = etree.Element(W + "pPr")
            p.insert(0, properties)
        spacing = properties.find(W + "spacing")
        if spacing is None:
            spacing = etree.SubElement(properties, W + "spacing")
        for key, value in {"before": before * 20, "after": after * 20, "line": 276, "lineRule": "auto"}.items():
            spacing.set(W + key, str(value))
        if centered:
            alignment = properties.find(W + "jc")
            if alignment is None:
                alignment = etree.SubElement(properties, W + "jc")
            alignment.set(W + "val", "center")
        body.append(p)
        return p

    def run(p, text, *, size=10.5, bold=False):
        r = etree.SubElement(p, W + "r")
        properties = etree.SubElement(r, W + "rPr")
        fonts = etree.SubElement(properties, W + "rFonts")
        for key in ("ascii", "hAnsi", "cs"):
            fonts.set(W + key, "Calibri")
        etree.SubElement(properties, W + "color").set(W + "val", "000000")
        etree.SubElement(properties, W + "sz").set(W + "val", str(int(size * 2)))
        if bold:
            etree.SubElement(properties, W + "b")
        node = etree.SubElement(r, W + "t")
        node.set(XML + "space", "preserve")
        node.text = plain(text)
        return r

    def hyperlink(p, label, url, *, size=9.5, bold=False):
        nonlocal next_relationship
        next_relationship += 1
        rid = f"rIdPaulResume{next_relationship}"
        relation = etree.SubElement(relationships, REL + "Relationship")
        relation.set("Id", rid)
        relation.set("Type", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink")
        relation.set("Target", url)
        relation.set("TargetMode", "External")
        h = etree.SubElement(p, W + "hyperlink")
        h.set(R + "id", rid)
        r = run(h, label, size=size, bold=bold)
        return h

    def heading(title):
        run(paragraph(3, before=8, after=3), title, size=14, bold=True)

    def text(value, *, after=3, size=10.5):
        run(paragraph(5, after=after), value, size=size)

    def entry(title, date=None):
        p = paragraph(7, before=3, after=2)
        properties = p.find(W + "pPr")
        old_tabs = properties.find(W + "tabs")
        if old_tabs is not None:
            properties.remove(old_tabs)
        tabs = etree.SubElement(properties, W + "tabs")
        tab = etree.SubElement(tabs, W + "tab")
        tab.set(W + "val", "right")
        tab.set(W + "pos", "9020")
        run(p, title, size=11, bold=True)
        if date:
            etree.SubElement(etree.SubElement(p, W + "r"), W + "tab")
            run(p, date, size=10, bold=True)

    def bullet(value):
        run(paragraph(9, after=3), value, size=10)

    run(paragraph(0, before=24, after=4, centered=True), P["name"], size=24, bold=True)
    run(paragraph(1, after=3, centered=True), "COMPUTER SCIENCE STUDENT", size=10.5)
    contact = paragraph(2, after=3, centered=True)
    hyperlink(contact, P["phone"], P["phoneHref"])
    run(contact, " | ", size=9.5)
    hyperlink(contact, P["email"], "mailto:" + P["email"])
    run(contact, " | " + P["location"], size=9.5)
    links = paragraph(2, after=3, centered=True)
    for index, (label, url) in enumerate([
        ("paul-antigo.vercel.app", P["portfolio"]),
        ("github.com/itszoriel", P["github"]),
        ("LinkedIn", P["linkedin"]),
    ]):
        if index:
            run(links, " | ", size=9.5)
        hyperlink(links, label, url)

    e = P["education"]
    work = P["experience"]
    heading("Education")
    entry(e["degree"])
    text(f'{e["institution"]}, {e["campus"]}')
    text(f'{e["period"]} | Expected {e["expectedGraduation"]} | {e["status"]}')
    heading("Work Experience")
    entry(work["title"], work["dates"])
    text(f'{work["organization"]}, {work["location"]} | SPES / DOLE | {work["duration"]}', size=10)
    for value in work["bullets"]:
        bullet(value)
    heading("Project Experience")
    entry("MunLink | Developer / Maintainer", "Ongoing")
    text(PROJECT_CONTEXT, size=10)
    p = paragraph(5, after=4)
    hyperlink(p, "Live demo", P["project"]["demo"], size=10)
    run(p, " | ", size=10)
    hyperlink(p, "Source repository", P["project"]["repository"], size=10)
    for value in P["project"]["resumeBullets"]:
        bullet(value)
    heading("Technical Skills")
    for label, items in SKILLS:
        p = paragraph(5, after=3)
        run(p, label + ": ", bold=True)
        run(p, items)
    heading("Course Certificates")
    for c in P["credentials"]:
        p = paragraph(5, after=4)
        hyperlink(p, c["title"], certificate_url(c), size=10, bold=True)
        run(p, f' - {c["issuer"]} | {c["date"]}', size=10)
    body.append(section)

    def serialize(tree):
        return etree.tostring(tree, xml_declaration=True, encoding="UTF-8", standalone=True)

    replacements = {
        "word/document.xml": serialize(root),
        "word/_rels/document.xml.rels": serialize(relationships),
    }
    core = etree.fromstring(parts["docProps/core.xml"][1])
    for node in core:
        key = etree.QName(node).localname
        if key in ("creator", "lastModifiedBy"):
            node.text = P["name"]
        elif key == "title":
            node.text = P["name"] + " - ATS Resume"
        elif key in ("subject", "description", "keywords", "lastPrinted"):
            node.text = ""
    replacements["docProps/core.xml"] = serialize(core)
    app = etree.fromstring(parts["docProps/app.xml"][1])
    for node in list(app):
        if etree.QName(node).localname in {"HeadingPairs", "TitlesOfParts", "Pages", "Words", "Characters", "CharactersWithSpaces", "Lines", "Paragraphs"}:
            app.remove(node)
    replacements["docProps/app.xml"] = serialize(app)
    package_rel = etree.fromstring(parts["_rels/.rels"][1])
    for node in list(package_rel):
        if "thumbnail" in node.get("Type", ""):
            package_rel.remove(node)
    replacements["_rels/.rels"] = serialize(package_rel)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUTPUT_PATH, "w", ZIP_DEFLATED) as output:
        for name, (entry, blob) in parts.items():
            if "thumbnail" in name.lower():
                continue
            output.writestr(entry, replacements.get(name, blob))
    blacken_docx(OUTPUT_PATH)
    print(f"Generated editable ATS resume from the supplied Word package: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_ats_docx()
