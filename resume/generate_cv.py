"""Generate Paul John E. Antigo's comprehensive CV as a DOCX.

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
from reportlab.platypus import Paragraph, SimpleDocTemplate
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "resume"
OUTPUT_PATH = OUTPUT_DIR / "Paul-John-Antigo-CV.docx"
PDF_OUTPUT_DIR = ROOT / "public" / "resumes"
PDF_OUTPUT_PATH = PDF_OUTPUT_DIR / "Paul-John-Antigo-CV.pdf"

FONT = "Calibri"
INK = RGBColor(23, 33, 38)
MUTED = RGBColor(82, 97, 106)
ACCENT = RGBColor(29, 92, 99)
LINK = "164E63"


PROFILE = (
    "Fourth-year Computer Science student with practical full-stack project experience. "
    "Worked across MunLink's frontend, API, database, and deployment, implementing features, "
    "integrating application layers, and testing workflows. Contributed to undergraduate blockchain research using Solidity, "
    "TypeScript, automated testing, gas measurement, and Ethereum Sepolia. Seeking "
    "internship, OJT, and entry-level opportunities to contribute and continue learning."
)

SKILLS = [
    ("Languages", "Python, TypeScript, JavaScript, SQL, Solidity"),
    ("Frontend", "React, HTML, CSS, Tailwind CSS, Vite"),
    ("Backend and APIs", "Flask, REST APIs, SQLAlchemy, JWT authentication, role-based access control"),
    ("Data", "PostgreSQL, database design, Supabase Storage, Microsoft Excel, Tableau"),
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
    "Measured a constant 48,730 gas per Merkle batch versus 47,712 gas per credential for the literature baseline; the empirical break-even point was two credentials.",
    "At 1,000 credentials, measured gas reductions reached 99.9% against the literature baseline and 97.3% against the study's cheapest baseline; all 12 live Sepolia confirmation cells matched local measurements exactly.",
    "Deployed and source-verified the BaselineAnchor and MerkleAnchor Solidity contracts on Ethereum Sepolia.",
]

SPES_BULLETS = [
    "Encoded and validated student information for identification-card processing and checked record consistency before production.",
    "Captured and prepared student photographs using Adobe Photoshop and organized records through Microsoft Excel and the school's information system.",
    "Supported the end-to-end ID production workflow using network-connected PCs, shared storage, and student files covering Grade 7 through college-level records.",
    "Performed quality checks on completed IDs and assisted with their organized release and distribution.",
]

CERTIFICATIONS = [
    ("Data Analytics Essentials", "Cisco Networking Academy - Issued August 29, 2026. Practical exposure to Microsoft Excel, SQL, and Tableau."),
    ("Microsoft Artificial Intelligence Course: Azure AI Fundamentals", "TESDA Online Program - Completed July 13, 2026."),
    ("Microsoft Cybersecurity Course: Security, Compliance, and Identity Fundamentals", "TESDA Online Program - Completed July 14, 2026."),
    ("Developing Designs for User Experience", "TESDA Online Program - Completed July 15, 2026."),
]

RECOGNITION = [
    "Dean's Lister, Bachelor of Science in Computer Science, President Ramon Magsaysay State University - First Semester, A.Y. 2023-2024.",
    "With Honors, Northern Zambales College, Inc. - First Quarter, S.Y. 2022-2023; academic average: 93.44%.",
    "With Honors, Northern Zambales College, Inc. - Grade 9, Third Quarter, S.Y. 2019-2020.",
    "First Runner-Up and Best in Music, Festival Dance Competition, PRMSU PE Culminating Activity - November 21, 2024.",
]


def set_font(run, size=None, color=INK, bold=None, italic=None):
    run.font.name = FONT
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), FONT)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), FONT)
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


def add_hyperlink(paragraph, text, url, color=LINK, underline=False):
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
    run_size.set(qn("w:val"), "17")
    run_properties.append(run_size)
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
    tab.set(qn("w:pos"), "547")
    tabs.append(tab)
    p_pr.append(tabs)
    indent = OxmlElement("w:ind")
    indent.set(qn("w:left"), "547")
    indent.set(qn("w:hanging"), "288")
    p_pr.append(indent)
    spacing = OxmlElement("w:spacing")
    spacing.set(qn("w:after"), "30")
    spacing.set(qn("w:line"), "247")
    spacing.set(qn("w:lineRule"), "auto")
    p_pr.append(spacing)
    level.append(p_pr)
    r_pr = OxmlElement("w:rPr")
    fonts = OxmlElement("w:rFonts")
    fonts.set(qn("w:ascii"), "Arial")
    fonts.set(qn("w:hAnsi"), "Arial")
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
    styles = document.styles
    normal = styles["Normal"]
    normal.font.name = FONT
    normal._element.rPr.rFonts.set(qn("w:ascii"), FONT)
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), FONT)
    normal.font.size = Pt(9.4)
    normal.font.color.rgb = INK
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(2)
    normal.paragraph_format.line_spacing = 1.05

    heading_1 = styles["Heading 1"]
    heading_1.font.name = FONT
    heading_1._element.rPr.rFonts.set(qn("w:ascii"), FONT)
    heading_1._element.rPr.rFonts.set(qn("w:hAnsi"), FONT)
    heading_1.font.size = Pt(10.5)
    heading_1.font.bold = True
    heading_1.font.color.rgb = ACCENT
    heading_1.paragraph_format.space_before = Pt(8)
    heading_1.paragraph_format.space_after = Pt(3)
    heading_1.paragraph_format.keep_with_next = True
    heading_1.paragraph_format.keep_together = True

    heading_2 = styles["Heading 2"]
    heading_2.font.name = FONT
    heading_2._element.rPr.rFonts.set(qn("w:ascii"), FONT)
    heading_2._element.rPr.rFonts.set(qn("w:hAnsi"), FONT)
    heading_2.font.size = Pt(10)
    heading_2.font.bold = True
    heading_2.font.color.rgb = INK
    heading_2.paragraph_format.space_before = Pt(3)
    heading_2.paragraph_format.space_after = Pt(1)
    heading_2.paragraph_format.keep_with_next = True
    heading_2.paragraph_format.keep_together = True

    for name, size, color, bold, before, after in (
        ("CV Contact", 8.5, INK, False, 0, 1),
        ("CV Meta", 8.6, MUTED, False, 0, 1),
        ("CV Compact", 8.8, INK, False, 0, 1),
    ):
        style = styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        style.base_style = normal
        style.font.name = FONT
        style._element.rPr.rFonts.set(qn("w:ascii"), FONT)
        style._element.rPr.rFonts.set(qn("w:hAnsi"), FONT)
        style.font.size = Pt(size)
        style.font.color.rgb = color
        style.font.bold = bold
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.line_spacing = 1.0


def add_section_heading(document, title):
    paragraph = document.add_paragraph(style="Heading 1")
    paragraph.add_run(title.upper())
    return paragraph


def add_entry_heading(document, title):
    paragraph = document.add_paragraph(style="Heading 2")
    paragraph.add_run(title)
    return paragraph


def add_meta(document, text):
    return document.add_paragraph(text, style="CV Meta")


def add_bullet(document, text, num_id):
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(1.5)
    paragraph.paragraph_format.line_spacing = 1.03
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
    section.top_margin = Inches(0.65)
    section.bottom_margin = Inches(0.68)
    section.left_margin = Inches(0.68)
    section.right_margin = Inches(0.68)
    section.header_distance = Inches(0.3)
    section.footer_distance = Inches(0.3)
    section.different_first_page_header_footer = True

    header = section.header
    paragraph = header.paragraphs[0]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
    paragraph.paragraph_format.space_after = Pt(0)
    run = paragraph.add_run("PAUL JOHN E. ANTIGO  |  CURRICULUM VITAE")
    set_font(run, size=8, color=MUTED, bold=True)

    footer = section.footer
    paragraph = footer.paragraphs[0]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    paragraph.paragraph_format.space_after = Pt(0)
    prefix = paragraph.add_run("Page ")
    set_font(prefix, size=8, color=MUTED)
    add_page_field(paragraph)


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

    name = document.add_paragraph()
    name.paragraph_format.space_after = Pt(0)
    run = name.add_run("PAUL JOHN E. ANTIGO")
    set_font(run, size=22, color=INK, bold=True)

    contact = document.add_paragraph(style="CV Contact")
    contact.add_run("Masinloc, Zambales, Philippines | 0951 137 8115 | ")
    add_hyperlink(contact, "Pauljohn.antigo@gmail.com", "mailto:Pauljohn.antigo@gmail.com")

    links = document.add_paragraph(style="CV Contact")
    add_hyperlink(links, "Portfolio", "https://paul-antigo.vercel.app/")
    links.add_run(" | ")
    add_hyperlink(links, "LinkedIn", "https://www.linkedin.com/in/paul-john-antigo-708047364/")
    links.add_run(" | ")
    add_hyperlink(links, "GitHub", "https://github.com/itszoriel")

    add_section_heading(document, "Professional Profile")
    document.add_paragraph(PROFILE)

    add_section_heading(document, "Technical Competencies")
    for label, text in SKILLS:
        add_labeled_paragraph(document, label, text, style="CV Compact")

    add_section_heading(document, "Project Experience")
    add_entry_heading(document, "MunLink | Developer and Maintainer")
    add_meta(document, "Civic-technology learning project | Active personal project")
    add_meta(document, "React, TypeScript, Tailwind CSS, Python, Flask, SQLAlchemy, PostgreSQL, Supabase Storage, JWT, ReportLab, Turborepo, Docker")
    project_links = document.add_paragraph(style="CV Meta")
    add_hyperlink(project_links, "Live demo", "https://munlink-web-9s3r.onrender.com/")
    for item in MUNLINK_BULLETS:
        add_bullet(document, item, num_id)

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
    add_meta(document, "President Ramon Magsaysay State University, Iba Campus | Expected July 2027 | Fourth-year student")
    add_entry_heading(document, "Senior High School - General Academic Strand")
    add_meta(document, "Northern Zambales College, Inc., Inhobol, Masinloc, Zambales | Completed S.Y. 2022-2023")

    add_section_heading(document, "Certifications and Training")
    for index, (title, detail) in enumerate(CERTIFICATIONS):
        paragraph = add_bullet(document, "", num_id)
        paragraph.runs[0].clear()
        title_run = paragraph.add_run(f"{title} - ")
        set_font(title_run, bold=True)
        detail_run = paragraph.add_run(detail)
        set_font(detail_run)
        if index == 0:
            paragraph.add_run(" ")
            add_hyperlink(
                paragraph,
                "Credential verification",
                "https://www.credly.com/badges/9f98bddd-f5d7-4246-9c03-25fe7a72c35e/public_url",
            )

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
        "AWS Certified AI Practitioner exam preparation - self-directed study in progress.",
        "Planned certification path: AWS Certified Generative AI Developer - Professional, followed by AWS Certified DevOps Engineer - Professional. Neither credential has been earned yet.",
        "Continues MunLink development and creates mini-projects to apply unfamiliar technologies and concepts.",
    ):
        add_bullet(document, item, num_id)

    add_section_heading(document, "Additional Information")
    add_labeled_paragraph(document, "Languages", "Filipino/Tagalog and English")
    add_labeled_paragraph(document, "Opportunity interests", "Internship/OJT and entry-level software engineering, full-stack development, data, or general IT roles")
    add_labeled_paragraph(document, "Work arrangements", "Open to remote, hybrid, or onsite opportunities")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    document.save(OUTPUT_PATH)
    print(f"Generated {OUTPUT_PATH}")


def make_pdf_styles():
    sample = getSampleStyleSheet()
    return {
        "name": ParagraphStyle(
            "CVName",
            parent=sample["Normal"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=23,
            textColor=colors.HexColor("#172126"),
            spaceAfter=0,
        ),
        "contact": ParagraphStyle(
            "CVContact",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=10,
            textColor=colors.HexColor("#172126"),
            spaceAfter=1,
        ),
        "section": ParagraphStyle(
            "CVSection",
            parent=sample["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=12,
            textColor=colors.HexColor("#1D5C63"),
            spaceBefore=7,
            spaceAfter=3,
            keepWithNext=True,
        ),
        "entry": ParagraphStyle(
            "CVEntry",
            parent=sample["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=11.5,
            textColor=colors.HexColor("#172126"),
            spaceBefore=2,
            spaceAfter=1,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "CVBody",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=9.2,
            leading=10.9,
            textColor=colors.HexColor("#172126"),
            spaceAfter=2,
        ),
        "compact": ParagraphStyle(
            "CVCompact",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=8.8,
            leading=10.2,
            textColor=colors.HexColor("#172126"),
            spaceAfter=1,
        ),
        "meta": ParagraphStyle(
            "CVMeta",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=8.4,
            leading=9.7,
            textColor=colors.HexColor("#52616A"),
            spaceAfter=1,
            keepWithNext=True,
        ),
        "bullet": ParagraphStyle(
            "CVBullet",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=8.8,
            leading=10.4,
            leftIndent=13,
            firstLineIndent=-8,
            textColor=colors.HexColor("#172126"),
            spaceAfter=1.4,
        ),
        "footer": ParagraphStyle(
            "CVFooter",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=7.8,
            leading=9,
            textColor=colors.HexColor("#52616A"),
        ),
    }


def pdf_section(story, styles, title):
    story.append(Paragraph(escape(title.upper()), styles["section"]))


def pdf_entry(story, styles, title, meta_lines=()):
    story.append(Paragraph(escape(title), styles["entry"]))
    for line in meta_lines:
        story.append(Paragraph(escape(line), styles["meta"]))


def pdf_bullet(story, styles, text):
    story.append(Paragraph(f"- {escape(text)}", styles["bullet"]))


def pdf_labeled(story, styles, label, text, style="compact"):
    story.append(Paragraph(f"<b>{escape(label)}:</b> {escape(text)}", styles[style]))


def pdf_page(canvas, document):
    canvas.saveState()
    width, height = A4
    if document.page > 1:
        canvas.setFont("Helvetica-Bold", 7.8)
        canvas.setFillColor(colors.HexColor("#52616A"))
        canvas.drawString(document.leftMargin, height - 0.35 * inch, "PAUL JOHN E. ANTIGO  |  CURRICULUM VITAE")
    canvas.setFont("Helvetica", 7.8)
    canvas.setFillColor(colors.HexColor("#52616A"))
    canvas.drawRightString(width - document.rightMargin, 0.32 * inch, f"Page {document.page}")
    canvas.restoreState()


def build_pdf():
    styles = make_pdf_styles()
    story = []

    story.append(Paragraph("PAUL JOHN E. ANTIGO", styles["name"]))
    story.append(
        Paragraph(
            "Masinloc, Zambales, Philippines | 0951 137 8115 | "
            '<link href="mailto:Pauljohn.antigo@gmail.com" color="#164E63">Pauljohn.antigo@gmail.com</link>',
            styles["contact"],
        )
    )
    story.append(
        Paragraph(
            '<link href="https://paul-antigo.vercel.app/" color="#164E63">Portfolio</link> | '
            '<link href="https://www.linkedin.com/in/paul-john-antigo-708047364/" color="#164E63">LinkedIn</link> | '
            '<link href="https://github.com/itszoriel" color="#164E63">GitHub</link>',
            styles["contact"],
        )
    )

    pdf_section(story, styles, "Professional Profile")
    story.append(Paragraph(escape(PROFILE), styles["body"]))

    pdf_section(story, styles, "Technical Competencies")
    for label, text in SKILLS:
        pdf_labeled(story, styles, label, text)

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
            '<link href="https://munlink-web-9s3r.onrender.com/" color="#164E63">Live demo</link>',
            styles["meta"],
        )
    )
    for item in MUNLINK_BULLETS:
        pdf_bullet(story, styles, item)

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
            '<link href="https://sepolia.etherscan.io/address/0xE569641E67C10f9a127fb3c01686D06DbA90dEEA#code" color="#164E63">BaselineAnchor 0xE569...dEEA</link> | '
            '<link href="https://sepolia.etherscan.io/address/0x2f5D48A9AC370e3cA81301107f1828E21500deF8#code" color="#164E63">MerkleAnchor 0x2f5D...deF8</link>',
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
        ("President Ramon Magsaysay State University, Iba Campus | Expected July 2027 | Fourth-year student",),
    )
    pdf_entry(
        story,
        styles,
        "Senior High School - General Academic Strand",
        ("Northern Zambales College, Inc., Inhobol, Masinloc, Zambales | Completed S.Y. 2022-2023",),
    )

    pdf_section(story, styles, "Certifications and Training")
    for index, (title, detail) in enumerate(CERTIFICATIONS):
        link = ""
        if index == 0:
            link = ' <link href="https://www.credly.com/badges/9f98bddd-f5d7-4246-9c03-25fe7a72c35e/public_url" color="#164E63">Credential verification</link>'
        story.append(Paragraph(f"- <b>{escape(title)}</b> - {escape(detail)}{link}", styles["bullet"]))

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
        "AWS Certified AI Practitioner exam preparation - self-directed study in progress.",
        "Planned certification path: AWS Certified Generative AI Developer - Professional, followed by AWS Certified DevOps Engineer - Professional. Neither credential has been earned yet.",
        "Continues MunLink development and creates mini-projects to apply unfamiliar technologies and concepts.",
    ):
        pdf_bullet(story, styles, item)

    pdf_section(story, styles, "Additional Information")
    pdf_labeled(story, styles, "Languages", "Filipino/Tagalog and English", "body")
    pdf_labeled(story, styles, "Opportunity interests", "Internship/OJT and entry-level software engineering, full-stack development, data, or general IT roles", "body")
    pdf_labeled(story, styles, "Work arrangements", "Open to remote, hybrid, or onsite opportunities", "body")

    PDF_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(PDF_OUTPUT_PATH),
        pagesize=A4,
        rightMargin=0.68 * inch,
        leftMargin=0.68 * inch,
        topMargin=0.58 * inch,
        bottomMargin=0.9 * inch,
        title="Paul John E. Antigo - Curriculum Vitae",
        author="Paul John E. Antigo",
        subject="Comprehensive curriculum vitae for software engineering, OJT, and academic opportunities",
    )
    document.build(story, onFirstPage=pdf_page, onLaterPages=pdf_page)
    print(f"Generated {PDF_OUTPUT_PATH}")


if __name__ == "__main__":
    build_cv()
    build_pdf()
