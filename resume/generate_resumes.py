"""Generate the ATS and Philippine photo resume PDFs.

Run from the repository root with:
    python resume/generate_resumes.py
"""

from __future__ import annotations

import shutil
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    Flowable,
    HRFlowable,
    Image,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "public" / "resumes"
PHOTO_PATH = ROOT / "public" / "images" / "paul-john-antigo-professional-2x2.jpg"

ATS_OUTPUT = OUTPUT_DIR / "Paul-John-Antigo-ATS-Resume.pdf"
PHOTO_OUTPUT = OUTPUT_DIR / "Paul-John-Antigo-PH-Resume.pdf"

PUBLIC_DEFAULT = ROOT / "public" / "Paul-John-Antigo-Resume.pdf"


COLORS = {
    "ink": colors.HexColor("#172126"),
    "muted": colors.HexColor("#52616A"),
    "accent": colors.HexColor("#1D5C63"),
    "rule": colors.HexColor("#8C9AA1"),
    "link": colors.HexColor("#164E63"),
}


SUMMARY = (
    "Fourth-year Computer Science student with practical full-stack project experience using "
    "React, TypeScript, Python, Flask, SQLAlchemy, and PostgreSQL. Develops features across "
    "frontend, API, and database layers, integrates authentication and permissions, and "
    "tests end-to-end workflows."
)

SKILLS = [
    ("Frontend", "React, TypeScript, JavaScript, HTML, CSS, Tailwind CSS, Vite"),
    ("Backend", "Python, Flask, REST APIs, SQLAlchemy, ReportLab"),
    ("Data", "PostgreSQL, SQL, database design, Supabase Storage"),
    (
        "Engineering",
        "Git, GitHub, Turborepo, Docker, JWT, authentication, authorization, RBAC, API integration",
    ),
]

PROJECT_BULLETS = [
    "Handled development in a three-person CSE 2 team during my third year, with teammates testing and debugging; continued maintaining and expanding the project after the course.",
    "Used AI tools, documentation, and community resources to support implementation and testing, practicing detailed prompting, task decomposition, context management, output validation, and token-conscious workflows.",
    "Built resident and administrative React applications using a shared Flask REST API and PostgreSQL database. The demo is scoped to Zambales and is not an official LGU deployment.",
    "Modeled end-to-end workflows for document requests, review, payments, QR-verified PDF release, program applications, announcements, issue reports, notifications, and marketplace transactions.",
    "Implemented JWT access and refresh tokens, password hashing, role- and location-scoped authorization, audit logging, sensitive-file access controls, and rate-limiting fundamentals.",
]

EXPERIENCE_BULLETS = [
    "Encoded and validated student information to support accurate identification-card processing and confirm information consistency before printing.",
    "Captured and prepared student photographs, organized records, and supported the end-to-end workflow from data preparation through card production.",
    "Performed final quality checks and assisted with the organized release and distribution of completed student IDs.",
]


class RoundedPortrait(Flowable):
    """Draw the source photo inside a rounded white portrait frame."""

    def __init__(self, path: Path, size: float, radius: float = 10) -> None:
        super().__init__()
        self.path = path
        self.width = size
        self.height = size
        self.radius = radius

    def draw(self) -> None:
        canvas = self.canv
        canvas.saveState()
        canvas.setFillColor(colors.white)
        canvas.roundRect(0, 0, self.width, self.height, self.radius, stroke=0, fill=1)

        inset = 2.2
        clip = canvas.beginPath()
        clip.roundRect(
            inset,
            inset,
            self.width - (inset * 2),
            self.height - (inset * 2),
            self.radius - 1,
        )
        canvas.clipPath(clip, stroke=0, fill=0)
        canvas.drawImage(
            ImageReader(str(self.path)),
            inset,
            inset,
            width=self.width - (inset * 2),
            height=self.height - (inset * 2),
            preserveAspectRatio=True,
            anchor="c",
            mask="auto",
        )
        canvas.restoreState()

CREDENTIALS = [
    "Data Analytics Essentials - Cisco Networking Academy, Aug 2026",
    "Azure AI Fundamentals - TESDA course completion, Jul 2026",
    "Security, Compliance, and Identity Fundamentals - TESDA course completion, Jul 2026",
    "Developing Designs for User Experience - TESDA course completion, Jul 2026",
]


def make_styles() -> dict[str, ParagraphStyle]:
    sample = getSampleStyleSheet()
    return {
        "name": ParagraphStyle(
            "Name",
            parent=sample["Normal"],
            fontName="Helvetica-Bold",
            fontSize=21,
            leading=22,
            textColor=COLORS["ink"],
            alignment=TA_LEFT,
            spaceAfter=1,
        ),
        "contact": ParagraphStyle(
            "Contact",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=7.9,
            leading=10,
            textColor=COLORS["ink"],
            spaceAfter=0,
        ),
        "section": ParagraphStyle(
            "Section",
            parent=sample["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=11,
            textColor=COLORS["ink"],
            spaceBefore=4.5,
            spaceAfter=1,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=8.8,
            leading=10.7,
            textColor=COLORS["ink"],
            spaceAfter=0,
        ),
        "skill": ParagraphStyle(
            "Skill",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=9.9,
            textColor=COLORS["ink"],
            spaceAfter=0.5,
        ),
        "entry": ParagraphStyle(
            "Entry",
            parent=sample["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.3,
            leading=10.6,
            textColor=COLORS["ink"],
            spaceAfter=0.5,
            keepWithNext=True,
        ),
        "meta": ParagraphStyle(
            "Meta",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=7.9,
            leading=9.4,
            textColor=COLORS["muted"],
            spaceAfter=0.5,
            keepWithNext=True,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=10.1,
            leftIndent=9,
            firstLineIndent=-9,
            textColor=COLORS["ink"],
            spaceAfter=0.7,
        ),
        "credential": ParagraphStyle(
            "Credential",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=8.3,
            leading=9.6,
            leftIndent=9,
            firstLineIndent=-9,
            textColor=COLORS["ink"],
            spaceAfter=0.2,
        ),
    }


def make_photo_styles() -> dict[str, ParagraphStyle]:
    sample = getSampleStyleSheet()
    return {
        "name": ParagraphStyle(
            "PhotoName",
            parent=sample["Normal"],
            fontName="Helvetica-Bold",
            fontSize=21,
            leading=22,
            textColor=COLORS["ink"],
            spaceAfter=3,
        ),
        "left_section": ParagraphStyle(
            "PhotoLeftSection",
            parent=sample["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.2,
            leading=10.5,
            textColor=COLORS["ink"],
            spaceBefore=8,
            spaceAfter=3,
            keepWithNext=True,
        ),
        "right_section": ParagraphStyle(
            "PhotoRightSection",
            parent=sample["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10.3,
            leading=11.5,
            textColor=COLORS["accent"],
            spaceBefore=8,
            spaceAfter=3,
            keepWithNext=True,
        ),
        "contact": ParagraphStyle(
            "PhotoContact",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=7.2,
            leading=9.2,
            textColor=COLORS["ink"],
            spaceAfter=2.2,
        ),
        "skill": ParagraphStyle(
            "PhotoSkill",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=7.2,
            leading=8.8,
            textColor=COLORS["ink"],
            spaceAfter=2.2,
        ),
        "credential": ParagraphStyle(
            "PhotoCredential",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=7.05,
            leading=8.6,
            textColor=COLORS["ink"],
            spaceAfter=3,
        ),
        "body": ParagraphStyle(
            "PhotoBody",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=9.6,
            textColor=COLORS["ink"],
            spaceAfter=1,
        ),
        "entry": ParagraphStyle(
            "PhotoEntry",
            parent=sample["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.7,
            leading=10,
            textColor=COLORS["ink"],
            spaceAfter=1,
            keepWithNext=True,
        ),
        "meta": ParagraphStyle(
            "PhotoMeta",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=7.15,
            leading=8.6,
            textColor=COLORS["muted"],
            spaceAfter=1.2,
            keepWithNext=True,
        ),
        "bullet": ParagraphStyle(
            "PhotoBullet",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=7.65,
            leading=9.15,
            leftIndent=9,
            firstLineIndent=-7,
            textColor=COLORS["ink"],
            spaceAfter=1.2,
        ),
    }


def contact_block(styles: dict[str, ParagraphStyle]) -> list[Paragraph]:
    return [
        Paragraph("PAUL JOHN E. ANTIGO", styles["name"]),
        Paragraph(
            "Zambales, Philippines | 0951 137 8115 | "
            '<link href="mailto:Pauljohn.antigo@gmail.com" color="#164E63">Pauljohn.antigo@gmail.com</link>',
            styles["contact"],
        ),
        Paragraph(
            '<link href="https://www.linkedin.com/in/paul-john-antigo-708047364/" color="#164E63">LinkedIn: https://www.linkedin.com/in/paul-john-antigo-708047364/</link>'
            " | "
            '<link href="https://github.com/itszoriel" color="#164E63">GitHub: https://github.com/itszoriel</link>',
            styles["contact"],
        ),
    ]


def photo_section(title: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(escape(title), style)


def build_photo_story():
    styles = make_photo_styles()

    header_text = [
        Paragraph("PAUL JOHN E. ANTIGO", styles["name"]),
    ]
    portrait = RoundedPortrait(PHOTO_PATH, 1.36 * inch, radius=12)
    header_table = Table(
        [[header_text, portrait]],
        colWidths=[6.06 * inch, 1.52 * inch],
        rowHeights=[1.48 * inch],
        hAlign="LEFT",
    )
    header_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E3E5E4")),
                ("VALIGN", (0, 0), (0, 0), "MIDDLE"),
                ("ALIGN", (1, 0), (1, 0), "CENTER"),
                ("VALIGN", (1, 0), (1, 0), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (0, 0), 18),
                ("RIGHTPADDING", (0, 0), (0, 0), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (1, 0), (1, 0), 4),
                ("RIGHTPADDING", (1, 0), (1, 0), 4),
            ]
        )
    )

    left = [
        photo_section("CONTACT", styles["left_section"]),
        Paragraph("Masinloc, Zambales, Philippines", styles["contact"]),
        Paragraph("0951 137 8115", styles["contact"]),
        Paragraph(
            '<link href="mailto:Pauljohn.antigo@gmail.com" color="#164E63">Pauljohn.antigo@gmail.com</link>',
            styles["contact"],
        ),
        Paragraph(
            '<link href="https://www.linkedin.com/in/paul-john-antigo-708047364/" color="#164E63">linkedin.com/in/<br/>paul-john-antigo-708047364</link>',
            styles["contact"],
        ),
        Paragraph(
            '<link href="https://github.com/itszoriel" color="#164E63">github.com/itszoriel</link>',
            styles["contact"],
        ),
        photo_section("TECHNICAL SKILLS", styles["left_section"]),
    ]
    for label, items in SKILLS:
        left.append(Paragraph(f"<b>{escape(label)}</b><br/>{escape(items)}", styles["skill"]))

    left.append(photo_section("CREDENTIALS", styles["left_section"]))
    for item in CREDENTIALS:
        left.append(Paragraph(escape(item), styles["credential"]))

    right = [
        photo_section("PROFESSIONAL SUMMARY", styles["right_section"]),
        Paragraph(escape(SUMMARY), styles["body"]),
        photo_section("SELECTED PROJECT", styles["right_section"]),
        Paragraph("MunLink | Developer / Maintainer | Personal Project", styles["entry"]),
        Paragraph(
            "React, TypeScript, Tailwind CSS, Python, Flask, SQLAlchemy, PostgreSQL, "
            "Supabase Storage, JWT, ReportLab, Turborepo, Docker",
            styles["meta"],
        ),
        Paragraph(
            '<link href="https://munlink-web-9s3r.onrender.com/" color="#164E63">Live demo: https://munlink-web-9s3r.onrender.com/</link>',
            styles["meta"],
        ),
    ]
    right.extend(Paragraph(f"- {escape(item)}", styles["bullet"]) for item in PROJECT_BULLETS)
    right.extend(
        [
            photo_section("EXPERIENCE", styles["right_section"]),
            Paragraph("IT Support Assistant - Cisco Department | June 4-July 31, 2025 (20 days)", styles["entry"]),
            Paragraph(
                "Special Program for Employment of Students (DOLE) | Northern Zambales College, Inc. | Masinloc, Zambales",
                styles["meta"],
            ),
        ]
    )
    right.extend(Paragraph(f"- {escape(item)}", styles["bullet"]) for item in EXPERIENCE_BULLETS)
    right.extend(
        [
            photo_section("EDUCATION", styles["right_section"]),
            Paragraph("Bachelor of Science in Computer Science | 2023 - 2027", styles["entry"]),
            Paragraph("President Ramon Magsaysay State University | Fourth-year student", styles["meta"]),
        ]
    )

    body_table = Table(
        [[left, right]],
        colWidths=[2.22 * inch, 5.36 * inch],
        rowHeights=[9.2 * inch],
        hAlign="LEFT",
    )
    body_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#F5F6F6")),
                ("LINEAFTER", (0, 0), (0, 0), 0.55, colors.HexColor("#B7BFC1")),
                ("LEFTPADDING", (0, 0), (0, 0), 14),
                ("RIGHTPADDING", (0, 0), (0, 0), 13),
                ("LEFTPADDING", (1, 0), (1, 0), 18),
                ("RIGHTPADDING", (1, 0), (1, 0), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    return [header_table, Spacer(1, 6), body_table]


def header(styles: dict[str, ParagraphStyle], include_photo: bool):
    blocks = contact_block(styles)
    if not include_photo:
        return blocks + [Spacer(1, 2)]

    if not PHOTO_PATH.exists():
        raise FileNotFoundError(f"Missing photo asset: {PHOTO_PATH}")

    text_cell = blocks
    photo = Image(str(PHOTO_PATH), width=1.15 * inch, height=1.15 * inch)
    table = Table(
        [[text_cell, photo]],
        colWidths=[6.05 * inch, 1.15 * inch],
        rowHeights=[1.15 * inch],
        hAlign="LEFT",
    )
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return [table, Spacer(1, 3)]


def section_title(title: str, styles: dict[str, ParagraphStyle]):
    return [
        Paragraph(title, styles["section"]),
        HRFlowable(
            width="100%",
            thickness=0.65,
            color=COLORS["rule"],
            spaceBefore=0,
            spaceAfter=2,
        ),
    ]


def bullet(text: str, styles: dict[str, ParagraphStyle]) -> Paragraph:
    return Paragraph(f"- {escape(text)}", styles["bullet"])


def build_story(styles: dict[str, ParagraphStyle], include_photo: bool):
    story = header(styles, include_photo)

    story.extend(section_title("PROFESSIONAL SUMMARY", styles))
    story.append(Paragraph(escape(SUMMARY), styles["body"]))

    story.extend(section_title("TECHNICAL SKILLS", styles))
    for label, items in SKILLS:
        story.append(Paragraph(f"<b>{escape(label)}:</b> {escape(items)}", styles["skill"]))

    story.extend(section_title("SELECTED PROJECT", styles))
    story.append(
        Paragraph(
            "MunLink | Developer / Maintainer | Personal Project",
            styles["entry"],
        )
    )
    story.append(
        Paragraph(
            "React, TypeScript, Tailwind CSS, Python, Flask, SQLAlchemy, PostgreSQL, "
            "Supabase Storage, JWT, ReportLab, Turborepo, Docker",
            styles["meta"],
        )
    )
    story.append(
        Paragraph(
            '<link href="https://munlink-web-9s3r.onrender.com/" color="#164E63">Live demo: https://munlink-web-9s3r.onrender.com/</link>',
            styles["meta"],
        )
    )
    story.extend(bullet(item, styles) for item in PROJECT_BULLETS)

    story.extend(section_title("EXPERIENCE", styles))
    experience_heading = [
        Paragraph("IT Support Assistant - Cisco Department | June 4-July 31, 2025 (20 days)", styles["entry"]),
        Paragraph(
            "Special Program for Employment of Students (DOLE) | Northern Zambales College, Inc. | Masinloc, Zambales",
            styles["meta"],
        ),
    ]
    story.append(KeepTogether(experience_heading))
    story.extend(bullet(item, styles) for item in EXPERIENCE_BULLETS)

    story.extend(section_title("EDUCATION", styles))
    story.append(Paragraph("Bachelor of Science in Computer Science | 2023 - 2027", styles["entry"]))
    story.append(
        Paragraph("President Ramon Magsaysay State University | Fourth-year student", styles["meta"])
    )

    story.extend(section_title("CREDENTIALS", styles))
    story.extend(Paragraph(f"- {escape(item)}", styles["credential"]) for item in CREDENTIALS)
    return story


def build_resume(path: Path, include_photo: bool) -> None:
    styles = make_styles()
    document = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=(0.34 if include_photo else 0.52) * inch,
        leftMargin=(0.34 if include_photo else 0.52) * inch,
        topMargin=(0.28 if include_photo else 0.42) * inch,
        bottomMargin=(0.28 if include_photo else 0.4) * inch,
        title="Paul John E. Antigo - Resume",
        author="Paul John E. Antigo",
        subject="Entry-level Software Engineer and Full-Stack Developer resume",
    )
    document.build(build_photo_story() if include_photo else build_story(styles, False))


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    build_resume(ATS_OUTPUT, include_photo=False)
    build_resume(PHOTO_OUTPUT, include_photo=True)

    shutil.copy2(ATS_OUTPUT, PUBLIC_DEFAULT)

    print(f"Generated {ATS_OUTPUT}")
    print(f"Generated {PHOTO_OUTPUT}")
    print("Updated public resume downloads.")


if __name__ == "__main__":
    main()
