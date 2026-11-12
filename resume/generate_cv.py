"""Generate Paul John E. Antigo's designed CV as a PDF and editable DOCX.

Run from the repository root with:
    python resume/generate_cv.py
"""

from __future__ import annotations

from pathlib import Path

from docx import Document as WordDocument
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, PageBreak, Spacer
from xml.sax.saxutils import escape
from document_common import PROFILE as P, assert_black_pdf, blacken_docx, certificate_title, certificate_url, link, plain


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "resume"
OUTPUT_PATH = OUTPUT_DIR / "Paul-John-Antigo-CV-Editable.docx"
PDF_OUTPUT_DIR = ROOT / "public" / "resumes"
PDF_OUTPUT_PATH = PDF_OUTPUT_DIR / "Paul-John-Antigo-CV.pdf"

FONT = "Calibri"
INK = RGBColor(0, 0, 0)
MUTED = RGBColor(0, 0, 0)
ACCENT = RGBColor(0, 0, 0)
LINK = "000000"


PROFILE = (
    "Fourth-year Computer Science student with practical full-stack project experience. "
    "Used AI assistance, documentation, and developer communities while working across MunLink's frontend, API, database, and deployment, implementing features, "
    "integrating application layers, and testing workflows. Contributed to undergraduate blockchain research using Solidity, "
    "TypeScript, automated testing, gas measurement, and Ethereum Sepolia. Seeking "
    "internship, OJT, and entry-level opportunities to contribute and continue learning."
)

SKILLS = [
    ("Languages", "Python, TypeScript, JavaScript, SQL, Solidity"),
    ("Frontend", "React, HTML, CSS, Tailwind CSS, Vite"),
    ("Backend and APIs", "Flask, REST APIs, SQLAlchemy, JWT authentication, role-based access control"),
    ("Data", "PostgreSQL, database design, Supabase Storage"),
    ("Data analytics coursework", "Microsoft Excel, SQL, Tableau, data preparation, data visualization"),
    ("Blockchain and research", "Hardhat, Ethereum Sepolia, Merkle trees, Keccak-256, automated testing, gas benchmarking"),
    ("Engineering tools", "Git, GitHub, Turborepo, Docker, Visual Studio Code, ReportLab, terminal/CLI, basic Linux CLI"),
    ("Additional tools", "Adobe Photoshop, Google Docs, Discord"),
]

MUNLINK_BULLETS = [
    "Handled development in a three-person CSE 2 team during my third year, with teammates testing and debugging; continued maintaining and expanding the project after the course.",
    "Used AI tools, documentation, and community resources including Reddit to support implementation and testing, practicing detailed prompting, task decomposition, context management, output validation, and token-conscious workflows.",
    "Designed a multi-application architecture with separate resident and administrative React applications connected to a shared Flask REST API and PostgreSQL data model.",
    "Implemented resident, municipal, provincial, and super-administrator workflows scoped by province, municipality, barangay, role, and permission.",
    "Developed workflows for account and resident verification, document requests, payments, QR-verified PDF release, benefit programs, announcements, notifications, issue reporting, and marketplace transactions.",
    "Implemented JWT access and refresh tokens, password hashing, role- and location-scoped authorization, audit logging, sensitive-file access controls, and rate-limiting fundamentals.",
    "Performed manual functional, role-based, API, browser, database, responsive, and end-to-end workflow testing while debugging CORS, authentication, database, and frontend-to-API integration issues.",
    "Maintained a Zambales-scoped portfolio demo, not an official LGU deployment, with Region 3 location data retained for possible future expansion.",
]

THESIS_BULLETS = [
    "Contributed to the design and development of a framework that anchors one Merkle root per credential batch while preserving individual verification through Merkle inclusion proofs.",
    "Worked on TypeScript-based credential processing, canonical encoding, deterministic synthetic data generation, Merkle tree construction, proof generation, and proof verification.",
    "Participated in Solidity prototype development, issuer access control, automated testing, gas measurement, technical documentation, results analysis, and defense preparation.",
    "Helped execute correctness, tamper-evidence, encoding-integrity, access-control, authenticity, and cross-implementation TypeScript/Solidity verification tests.",
    "Participated in a controlled four-arm evaluation covering batch sizes from 1 to 3,000 credentials with three repetitions per measurement cell and live-network confirmation on Ethereum Sepolia.",
    "The supplied study reports approximately 48,730 gas per Merkle batch versus 47,712 gas for a single literature-baseline credential write; matched durability-tier comparisons broke even at two credentials.",
    "At 1,000 credentials, the four-arm study measured 99.9% lower anchoring gas than the literature baseline and 97.3% lower than its log-based baseline; all 12 Sepolia confirmation cells matched local measurements. Results are specific to the study setup.",
    "Deployed and source-verified the BaselineAnchor and MerkleAnchor Solidity contracts on Ethereum Sepolia.",
]

SPES_BULLETS = [
    "Encoded and validated student information for identification-card processing and checked record consistency before production.",
    "Captured and prepared student photographs using Adobe Photoshop and organized records through Microsoft Excel and the school's information system.",
    "Supported the end-to-end ID production workflow using network-connected PCs, shared storage, and student files covering Grade 7 through college-level records.",
    "Performed quality checks on completed IDs and assisted with their organized release and distribution.",
]

CERTIFICATIONS = P["credentials"]


RECOGNITION = [
    "Dean's Lister, Bachelor of Science in Computer Science, President Ramon Magsaysay State University - First Semester, A.Y. 2023-2024.",
    "With Honors, Northern Zambales College, Inc. - First Quarter, S.Y. 2022-2023; academic average: 93.44%.",
    "With Honors, Northern Zambales College, Inc. - Grade 9, Third Quarter, S.Y. 2019-2020.",
    "First Runner-Up and Best in Music, Festival Dance Competition, PRMSU PE Culminating Activity - November 21, 2024.",
]


def set_font(run, size=None, color=INK, bold=None, italic=None, font_name=None):
    face = font_name or FONT
    run.font.name = face
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), face)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), face)
    if size is not None:
        run.font.size = Pt(size)
    run.font.color.rgb = color
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic


def set_cell_margins(cell, top=80, start=120, bottom=80, end=120):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for edge, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        element = tc_mar.find(qn(f"w:{edge}"))
        if element is None:
            element = OxmlElement(f"w:{edge}")
            tc_mar.append(element)
        element.set(qn("w:w"), str(value))
        element.set(qn("w:type"), "dxa")


def add_hyperlink(paragraph, text, url, color=LINK, underline=False, size=9.5, bold=False):
    part = paragraph.part
    relationship_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), relationship_id)
    run = OxmlElement("w:r")
    run_properties = OxmlElement("w:rPr")
    run_fonts = OxmlElement("w:rFonts")
    run_fonts.set(qn("w:ascii"), FONT)
    run_fonts.set(qn("w:hAnsi"), FONT)
    run_properties.append(run_fonts)
    run_color = OxmlElement("w:color")
    run_color.set(qn("w:val"), color)
    run_properties.append(run_color)
    run_size = OxmlElement("w:sz")
    run_size.set(qn("w:val"), str(int(size * 2)))
    run_properties.append(run_size)
    if bold:
        run_properties.append(OxmlElement("w:b"))
    if underline:
        underline_element = OxmlElement("w:u")
        underline_element.set(qn("w:val"), "single")
        run_properties.append(underline_element)
    run.append(run_properties)
    text_element = OxmlElement("w:t")
    text_element.text = text
    run.append(text_element)
    hyperlink.append(run)
    paragraph._p.append(hyperlink)


def add_page_field(paragraph):
    run = paragraph.add_run()
    field_begin = OxmlElement("w:fldChar")
    field_begin.set(qn("w:fldCharType"), "begin")
    instruction = OxmlElement("w:instrText")
    instruction.set(qn("xml:space"), "preserve")
    instruction.text = " PAGE "
    field_end = OxmlElement("w:fldChar")
    field_end.set(qn("w:fldCharType"), "end")
    run._r.extend((field_begin, instruction, field_end))
    set_font(run, size=8, color=MUTED)


def configure_numbering(document):
    numbering = document.part.numbering_part.element
    abstract_id = 200
    num_id = 200

    abstract = OxmlElement("w:abstractNum")
    abstract.set(qn("w:abstractNumId"), str(abstract_id))
    multi = OxmlElement("w:multiLevelType")
    multi.set(qn("w:val"), "singleLevel")
    abstract.append(multi)
    level = OxmlElement("w:lvl")
    level.set(qn("w:ilvl"), "0")
    start = OxmlElement("w:start")
    start.set(qn("w:val"), "1")
    level.append(start)
    num_format = OxmlElement("w:numFmt")
    num_format.set(qn("w:val"), "bullet")
    level.append(num_format)
    level_text = OxmlElement("w:lvlText")
    level_text.set(qn("w:val"), "•")
    level.append(level_text)
    justification = OxmlElement("w:lvlJc")
    justification.set(qn("w:val"), "left")
    level.append(justification)
    p_pr = OxmlElement("w:pPr")
    tabs = OxmlElement("w:tabs")
    tab = OxmlElement("w:tab")
    tab.set(qn("w:val"), "num")
    tab.set(qn("w:pos"), "260")
    tabs.append(tab)
    p_pr.append(tabs)
    indent = OxmlElement("w:ind")
    indent.set(qn("w:left"), "260")
    indent.set(qn("w:hanging"), "260")
    p_pr.append(indent)
    spacing = OxmlElement("w:spacing")
    spacing.set(qn("w:after"), "30")
    spacing.set(qn("w:line"), "247")
    spacing.set(qn("w:lineRule"), "auto")
    p_pr.append(spacing)
    level.append(p_pr)
    r_pr = OxmlElement("w:rPr")
    fonts = OxmlElement("w:rFonts")
    fonts.set(qn("w:ascii"), FONT)
    fonts.set(qn("w:hAnsi"), FONT)
    r_pr.append(fonts)
    level.append(r_pr)
    abstract.append(level)
    numbering.append(abstract)

    num = OxmlElement("w:num")
    num.set(qn("w:numId"), str(num_id))
    abstract_reference = OxmlElement("w:abstractNumId")
    abstract_reference.set(qn("w:val"), str(abstract_id))
    num.append(abstract_reference)
    numbering.append(num)
    return num_id


def configure_styles(document):
    from cv_word_design import rule
    styles = document.styles
    normal = styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(10.5)
    normal.font.color.rgb = INK
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(3)
    normal.paragraph_format.line_spacing = Pt(13.5)
    for style_name, face, size, leading, bold, before, after in (
        ("Heading 1", "Georgia", 14.5, 18, True, 8, 4),
        ("Heading 2", FONT, 11.5, 14.5, True, 3, 4),
    ):
        style = styles[style_name]
        style.font.name = face
        style._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), face)
        style._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), face)
        style.font.size = Pt(size)
        style.font.bold = bold
        style.font.color.rgb = INK
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.line_spacing = Pt(leading)
        style.paragraph_format.keep_with_next = True
        style.paragraph_format.keep_together = True
    for style_name, face, size, leading, bold, after in (
        ("CV Kicker", FONT, 9.5, 12, True, 8),
        ("CV Name", "Georgia", 32, 38, False, 8),
        ("CV Contact", FONT, 9.5, 12.5, False, 2),
        ("CV Meta", FONT, 9.5, 12, False, 2),
        ("CV Compact", FONT, 10.5, 13.5, False, 3),
        ("CV Skill", FONT, 10, 12.5, False, 0),
        ("CV Certificate", FONT, 10.5, 13.5, False, 0),
    ):
        style = styles.add_style(style_name, WD_STYLE_TYPE.PARAGRAPH)
        style.base_style = normal
        style.font.name = face
        style._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), face)
        style._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), face)
        style.font.size = Pt(size)
        style.font.bold = bold
        style.font.color.rgb = INK
        style.paragraph_format.space_before = Pt(0)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.line_spacing = Pt(leading)
    styles["CV Meta"].paragraph_format.keep_with_next = True


def add_section_heading(document, title):
    paragraph = document.add_paragraph(style="Heading 1")
    paragraph.add_run(title)
    from cv_word_design import rule
    rule(paragraph, space=3)
    return paragraph


def add_entry_heading(document, title):
    paragraph = document.add_paragraph(style="Heading 2")
    paragraph.add_run(title)
    return paragraph


def add_meta(document, text):
    return document.add_paragraph(text, style="CV Meta")


def add_bullet(document, text, num_id):
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(3)
    paragraph.paragraph_format.line_spacing = Pt(13.5)
    p_pr = paragraph._p.get_or_add_pPr()
    num_pr = OxmlElement("w:numPr")
    ilvl = OxmlElement("w:ilvl")
    ilvl.set(qn("w:val"), "0")
    num_id_element = OxmlElement("w:numId")
    num_id_element.set(qn("w:val"), str(num_id))
    num_pr.extend((ilvl, num_id_element))
    p_pr.append(num_pr)
    paragraph.add_run(text)
    return paragraph


def add_labeled_paragraph(document, label, text, style=None):
    paragraph = document.add_paragraph(style=style)
    label_run = paragraph.add_run(f"{label}: ")
    set_font(label_run, bold=True)
    value_run = paragraph.add_run(text)
    set_font(value_run)
    return paragraph


def configure_document(document):
    section = document.sections[0]
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = Pt(58)
    section.bottom_margin = Pt(48)
    section.left_margin = Pt(48)
    section.right_margin = Pt(48)
    section.header_distance = Pt(24)
    section.footer_distance = Pt(22)
    section.different_first_page_header_footer = True

    header = section.header
    paragraph = header.paragraphs[0]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
    paragraph.paragraph_format.space_after = Pt(0)
    run = paragraph.add_run("PAUL JOHN E. ANTIGO  |  CURRICULUM VITAE")
    set_font(run, size=9, color=INK, bold=True)
    from cv_word_design import rule
    rule(paragraph, space=5)

    from docx.enum.text import WD_TAB_ALIGNMENT
    for footer in (section.footer, section.first_page_footer):
        paragraph = footer.paragraphs[0]
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.paragraph_format.tab_stops.add_tab_stop(section.page_width - section.left_margin - section.right_margin, WD_TAB_ALIGNMENT.RIGHT)
        set_font(paragraph.add_run("CURRICULUM VITAE\tPage "), size=8.5)
        add_page_field(paragraph)
        set_font(paragraph.add_run(" / "), size=8.5)
        run = paragraph.add_run()
        begin = OxmlElement("w:fldChar")
        begin.set(qn("w:fldCharType"), "begin")
        instruction = OxmlElement("w:instrText")
        instruction.text = " NUMPAGES "
        end = OxmlElement("w:fldChar")
        end.set(qn("w:fldCharType"), "end")
        run._r.extend((begin, instruction, end))
        set_font(run, size=8.5)


def build_cv():
    document = WordDocument()
    configure_document(document)
    configure_styles(document)
    num_id = configure_numbering(document)

    properties = document.core_properties
    properties.title = "Paul John E. Antigo - Curriculum Vitae"
    properties.author = "Paul John E. Antigo"
    properties.subject = "Comprehensive curriculum vitae for software engineering, OJT, and academic opportunities"
    properties.keywords = "software engineer, full-stack developer, computer science, React, TypeScript, Python, Flask, PostgreSQL, Solidity"

    document.add_paragraph("CURRICULUM VITAE", style="CV Kicker")
    name = document.add_paragraph(style="CV Name")
    run = name.add_run(P["name"])
    set_font(run, size=32, bold=False, font_name="Georgia")
    from cv_word_design import rule, skills as word_skills, certificates as word_certificates
    rule(name, edge="left", color="000000", size=18, space=8)

    contact = document.add_paragraph(style="CV Contact")
    contact.add_run(f'{P["location"]} | ')
    add_hyperlink(contact, P["phone"], P["phoneHref"])
    contact.add_run(" | ")
    add_hyperlink(contact, "Pauljohn.antigo@gmail.com", "mailto:Pauljohn.antigo@gmail.com")

    links = document.add_paragraph(style="CV Contact")
    add_hyperlink(links, "Portfolio", "https://paul-antigo.vercel.app/")
    links.add_run(" | ")
    add_hyperlink(links, "LinkedIn", "https://www.linkedin.com/in/paul-john-antigo-708047364/")
    links.add_run(" | ")
    add_hyperlink(links, "GitHub", "https://github.com/itszoriel")
    rule(links, space=6)
    links.paragraph_format.space_after = Pt(9)

    add_section_heading(document, "Professional Profile")
    document.add_paragraph(PROFILE)

    add_section_heading(document, "Technical Competencies")
    word_skills(document, SKILLS, set_font)

    add_section_heading(document, "Project Experience")
    add_entry_heading(document, "MunLink | Developer and Maintainer")
    add_meta(document, "Civic-technology learning project | Active personal project")
    add_meta(document, "React, TypeScript, Tailwind CSS, Python, Flask, SQLAlchemy, PostgreSQL, Supabase Storage, JWT, ReportLab, Turborepo, Docker")
    project_links = document.add_paragraph(style="CV Meta")
    add_hyperlink(project_links, "Live demo", "https://munlink-web-9s3r.onrender.com/")
    for item in MUNLINK_BULLETS:
        add_bullet(document, item, num_id)

    document.add_page_break()
    add_section_heading(document, "Research Experience")
    add_entry_heading(document, "Merkle Root Framework for Micro-Credential Verification Authenticity and Gas-Efficient Issuance")
    add_meta(document, "Undergraduate Thesis, President Ramon Magsaysay State University | Researcher / Developer, four-member team | Final defense pending")
    add_meta(document, "Solidity 0.8.28, TypeScript, Hardhat, Ethereum Sepolia, Merkle trees, Keccak-256")
    for item in THESIS_BULLETS:
        add_bullet(document, item, num_id)

    contract_label = document.add_paragraph(style="CV Meta")
    label_run = contract_label.add_run("Verified contracts: ")
    set_font(label_run, size=8.6, color=MUTED, bold=True)
    add_hyperlink(
        contract_label,
        "BaselineAnchor 0xE569...dEEA",
        "https://sepolia.etherscan.io/address/0xE569641E67C10f9a127fb3c01686D06DbA90dEEA#code",
    )
    contract_label.add_run(" | ")
    add_hyperlink(
        contract_label,
        "MerkleAnchor 0x2f5D...deF8",
        "https://sepolia.etherscan.io/address/0x2f5D48A9AC370e3cA81301107f1828E21500deF8#code",
    )
    add_labeled_paragraph(document, "Thesis adviser", "Amelia E. Damian", style="CV Meta")
    add_labeled_paragraph(document, "Panel members", "Dr. John Lenon E. Agatep, Nerissa L. Javier, Israel M. Cabasug", style="CV Meta")

    add_section_heading(document, "Professional Experience")
    add_entry_heading(document, "IT Support Assistant - Cisco Department")
    add_meta(document, "Special Program for Employment of Students (SPES), Northern Zambales College, Inc. | Masinloc, Zambales | June 4-July 31, 2025 (20 days)")
    for item in SPES_BULLETS:
        add_bullet(document, item, num_id)

    add_section_heading(document, "Education")
    add_entry_heading(document, "Bachelor of Science in Computer Science")
    add_meta(document, f'{P["education"]["institution"]}, {P["education"]["campus"]} | 2023-2027 | Expected {P["education"]["expectedGraduation"]} | {P["education"]["status"]}')
    add_entry_heading(document, "Senior High School - General Academic Strand")
    add_meta(document, "Northern Zambales College, Inc., Inhobol, Masinloc, Zambales | Completed S.Y. 2022-2023")

    document.add_page_break()
    add_section_heading(document, "Earned Course Certificates")
    word_certificates(document, CERTIFICATIONS, add_hyperlink, set_font)

    add_section_heading(document, "Academic Recognition")
    for item in RECOGNITION:
        add_bullet(document, item, num_id)

    add_section_heading(document, "Relevant Coursework")
    add_labeled_paragraph(
        document,
        "Software and algorithms",
        "Data Structures and Algorithms, Object-Oriented Programming, Algorithms and Complexity, Programming Languages, Software Engineering I and II",
    )
    add_labeled_paragraph(
        document,
        "Systems and data",
        "Information Management, Operating Systems, Networks and Communications, Computer Architecture and Organization, Probability Theory and Statistics",
    )
    add_labeled_paragraph(
        document,
        "Research and communication",
        "CS Thesis Writing I, Scientific and Technical Writing",
    )
    add_labeled_paragraph(
        document,
        "In progress",
        "Automata Theory and Formal Languages, Information Assurance and Security, Introduction to Human-Computer Interaction, CS Thesis Writing II, 600-hour Practicum",
    )

    add_section_heading(document, "Continuing Professional Development")
    for item in (
        "Studies cloud and generative AI fundamentals through self-directed learning.",
        "Continues MunLink development and creates mini-projects to apply unfamiliar technologies and concepts.",
    ):
        add_bullet(document, item, num_id)

    add_section_heading(document, "Additional Information")
    add_labeled_paragraph(document, "Languages", "Filipino/Tagalog and English")
    add_labeled_paragraph(document, "Opportunity interests", "Internship/OJT and entry-level software engineering, full-stack development, data, or general IT roles")
    add_labeled_paragraph(document, "Work arrangements", "Open to remote, hybrid, or onsite opportunities")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for style in document.styles:
        if hasattr(style, "font"):
            style.font.color.rgb = RGBColor(0, 0, 0)
    for style_name in ("Hyperlink", "FollowedHyperlink"):
        style = document.styles[style_name] if style_name in document.styles else document.styles.add_style(style_name, WD_STYLE_TYPE.CHARACTER)
        style.font.color.rgb = RGBColor(0, 0, 0)
    for element in document.element.iter(qn("w:color")):
        element.set(qn("w:val"), "000000")
        for key in ("themeColor", "themeTint", "themeShade"):
            element.attrib.pop(qn(f"w:{key}"), None)
    document.save(OUTPUT_PATH)
    blacken_docx(OUTPUT_PATH)
    print(f"Generated {OUTPUT_PATH}")


def make_pdf_styles():
    from cv_design import make_styles
    return make_styles()


def pdf_section(story, styles, title):
    from cv_design import SectionHeading
    story.append(SectionHeading(title, styles["section"]))


def pdf_entry(story, styles, title, meta_lines=()):
    story.append(Paragraph(escape(title), styles["entry"]))
    for line in meta_lines:
        story.append(Paragraph(escape(line), styles["meta"]))


def pdf_bullet(story, styles, text):
    story.append(Paragraph(escape(plain(text)), styles["bullet"], bulletText="•"))


def pdf_labeled(story, styles, label, text, style="compact"):
    story.append(Paragraph(f"<b>{escape(label)}:</b> {escape(text)}", styles[style]))


def pdf_page(canvas, document):
    from cv_design import page_furniture
    page_furniture(canvas, document)


def build_pdf():
    from cv_design import register_fonts, Masthead, skill_grid, certificate_grid, make_document
    register_fonts()
    styles = make_pdf_styles()
    document = make_document(PDF_OUTPUT_PATH)
    story = [Masthead(styles), Spacer(1, 8)]

    pdf_section(story, styles, "Professional Profile")
    story.append(Paragraph(escape(PROFILE), styles["body"]))

    pdf_section(story, styles, "Technical Competencies")
    story.append(skill_grid(SKILLS, styles, document.width))

    pdf_section(story, styles, "Project Experience")
    pdf_entry(
        story,
        styles,
        "MunLink | Developer and Maintainer",
        (
            "Civic-technology learning project | Active personal project",
            "React, TypeScript, Tailwind CSS, Python, Flask, SQLAlchemy, PostgreSQL, Supabase Storage, JWT, ReportLab, Turborepo, Docker",
        ),
    )
    story.append(
        Paragraph(
            '<link href="https://munlink-web-9s3r.onrender.com/" color="#000000">Live demo</link>',
            styles["meta"],
        )
    )
    for item in MUNLINK_BULLETS:
        pdf_bullet(story, styles, item)

    story.append(PageBreak())
    pdf_section(story, styles, "Research Experience")
    pdf_entry(
        story,
        styles,
        "Merkle Root Framework for Micro-Credential Verification Authenticity and Gas-Efficient Issuance",
        (
            "Undergraduate Thesis, President Ramon Magsaysay State University | Researcher / Developer, four-member team | Final defense pending",
            "Solidity 0.8.28, TypeScript, Hardhat, Ethereum Sepolia, Merkle trees, Keccak-256",
        ),
    )
    for item in THESIS_BULLETS:
        pdf_bullet(story, styles, item)
    story.append(
        Paragraph(
            '<b>Verified contracts:</b> '
            '<link href="https://sepolia.etherscan.io/address/0xE569641E67C10f9a127fb3c01686D06DbA90dEEA#code" color="#000000">BaselineAnchor 0xE569...dEEA</link> | '
            '<link href="https://sepolia.etherscan.io/address/0x2f5D48A9AC370e3cA81301107f1828E21500deF8#code" color="#000000">MerkleAnchor 0x2f5D...deF8</link>',
            styles["meta"],
        )
    )
    pdf_labeled(story, styles, "Thesis adviser", "Amelia E. Damian", "meta")
    pdf_labeled(story, styles, "Panel members", "Dr. John Lenon E. Agatep, Nerissa L. Javier, Israel M. Cabasug", "meta")

    pdf_section(story, styles, "Professional Experience")
    pdf_entry(
        story,
        styles,
        "IT Support Assistant - Cisco Department",
        ("Special Program for Employment of Students (SPES), Northern Zambales College, Inc. | Masinloc, Zambales | June 4-July 31, 2025 (20 days)",),
    )
    for item in SPES_BULLETS:
        pdf_bullet(story, styles, item)

    pdf_section(story, styles, "Education")
    pdf_entry(
        story,
        styles,
        "Bachelor of Science in Computer Science",
        (f'{P["education"]["institution"]}, {P["education"]["campus"]} | 2023-2027 | Expected {P["education"]["expectedGraduation"]} | {P["education"]["status"]}',),
    )
    pdf_entry(
        story,
        styles,
        "Senior High School - General Academic Strand",
        ("Northern Zambales College, Inc., Inhobol, Masinloc, Zambales | Completed S.Y. 2022-2023",),
    )

    story.append(PageBreak())
    pdf_section(story, styles, "Earned Course Certificates")
    story.append(certificate_grid(CERTIFICATIONS, styles, document.width))

    pdf_section(story, styles, "Academic Recognition")
    for item in RECOGNITION:
        pdf_bullet(story, styles, item)

    pdf_section(story, styles, "Relevant Coursework")
    pdf_labeled(story, styles, "Software and algorithms", "Data Structures and Algorithms, Object-Oriented Programming, Algorithms and Complexity, Programming Languages, Software Engineering I and II", "body")
    pdf_labeled(story, styles, "Systems and data", "Information Management, Operating Systems, Networks and Communications, Computer Architecture and Organization, Probability Theory and Statistics", "body")
    pdf_labeled(story, styles, "Research and communication", "CS Thesis Writing I, Scientific and Technical Writing", "body")
    pdf_labeled(story, styles, "In progress", "Automata Theory and Formal Languages, Information Assurance and Security, Introduction to Human-Computer Interaction, CS Thesis Writing II, 600-hour Practicum", "body")

    pdf_section(story, styles, "Continuing Professional Development")
    for item in (
        "Studies cloud and generative AI fundamentals through self-directed learning.",
        "Continues MunLink development and creates mini-projects to apply unfamiliar technologies and concepts.",
    ):
        pdf_bullet(story, styles, item)

    pdf_section(story, styles, "Additional Information")
    pdf_labeled(story, styles, "Languages", "Filipino/Tagalog and English", "body")
    pdf_labeled(story, styles, "Opportunity interests", "Internship/OJT and entry-level software engineering, full-stack development, data, or general IT roles", "body")
    pdf_labeled(story, styles, "Work arrangements", "Open to remote, hybrid, or onsite opportunities", "body")

    PDF_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    document.build(story)
    from pypdf import PdfReader
    assert len(PdfReader(PDF_OUTPUT_PATH).pages) == 3, "CV layout must retain three balanced pages"
    assert_black_pdf(PDF_OUTPUT_PATH)
    print(f"Generated {PDF_OUTPUT_PATH}")


if __name__ == "__main__":
    build_cv()
    build_pdf()
