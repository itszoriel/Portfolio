"""Generate two black-text resumes following the user's supplied references."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Flowable, Frame, PageTemplate, Paragraph,
    Spacer, Table, TableStyle,
)

from document_common import BLACK, PROFILE as P, ROOT, assert_black_pdf, certificate_url, link, plain

OUTPUT_DIR = ROOT / "public/resumes"
ATS_OUTPUT = OUTPUT_DIR / "Paul-John-Antigo-ATS-Resume.pdf"
PHOTO_OUTPUT = OUTPUT_DIR / "Paul-John-Antigo-PH-Resume.pdf"
PUBLIC_DEFAULT = ROOT / "public/Paul-John-Antigo-Resume.pdf"
PHOTO_PATH = ROOT / "public/images/paul-john-antigo-professional-2x2.jpg"
SUMMARY = (
    "Fourth-year Computer Science student building full-stack projects with React, TypeScript, "
    "Python, Flask, and PostgreSQL, supported by AI tools and documentation. "
    "Open to internship/OJT and entry-level roles."
)
SKILLS = [(g["title"].replace("Development / Engineering", "Engineering"), ", ".join(g["items"])) for g in P["skillGroups"][:4]]
PROJECT_CONTEXT = "Three-person CSE 2 origin; handled development with teammate testing/debugging, then continued as maintainer."
PHOTO_SKILLS = ["React", "TypeScript", "Python", "Flask", "PostgreSQL", "SQLAlchemy", "Git / GitHub", "JWT / RBAC"]


def register_fonts():
    calibri_dir = Path(os.environ.get("RESUME_CALIBRI_DIR", str(Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts")))
    for family, weight, filename in [
        ("ResumeCalibri", "Regular", "calibri.ttf"),
        ("ResumeCalibri", "Bold", "calibrib.ttf"),
        ("ResumeCalibri", "Italic", "calibrii.ttf"),
    ]:
        path = calibri_dir / filename
        if not path.is_file():
            raise FileNotFoundError(f"Calibri is required by the supplied ATS template. Set RESUME_CALIBRI_DIR to a licensed installed Calibri font directory: {path}")
        pdfmetrics.registerFont(TTFont(f"{family}-{weight}", str(path)))
    pdfmetrics.registerFontFamily("ResumeCalibri-Regular", normal="ResumeCalibri-Regular", bold="ResumeCalibri-Bold", italic="ResumeCalibri-Italic", boldItalic="ResumeCalibri-Bold")
    for weight in ["Regular", "SemiBold", "Bold"]:
        path = ROOT / "resume/fonts" / f"Montserrat-{weight}.ttf"
        pdfmetrics.registerFont(TTFont(f"ResumeMontserrat-{weight}", str(path)))
    pdfmetrics.registerFontFamily("ResumeMontserrat-Regular", normal="ResumeMontserrat-Regular", bold="ResumeMontserrat-Bold", italic="ResumeMontserrat-Regular", boldItalic="ResumeMontserrat-Bold")


def make_styles(photo=False):
    family = "ResumeMontserrat" if photo else "ResumeCalibri"

    def style(name, size=10, leading=12.4, bold=False, **kwargs):
        return ParagraphStyle(
            name, fontName=f'{family}-{"Bold" if bold else "Regular"}',
            fontSize=size, leading=leading, textColor=BLACK,
            bulletFontName=f"{family}-Regular", bulletFontSize=size, bulletColor=BLACK,
            **kwargs,
        )

    return {
        "name": style("Name", 24, 28, True, alignment=TA_CENTER, spaceAfter=4),
        "role": style("Role", 10.5, 13, alignment=TA_CENTER, spaceAfter=3),
        "contact": style("Contact", 9.6, 12, alignment=TA_CENTER, spaceAfter=3),
        "section": style("Section", 15 if photo else 14, 18, True, keepWithNext=True),
        "entry": style("Entry", 10.3 if photo else 11, 13, True, spaceAfter=3, keepWithNext=True),
        "body": style("Body", 9.8 if photo else 10.5, 12.5, spaceAfter=3),
        "meta": style("Meta", 9.2 if photo else 10, 12, spaceAfter=4, keepWithNext=True),
        "bullet": style("Bullet", 9.6 if photo else 10, 12.4, leftIndent=10 if photo else 36, firstLineIndent=0, bulletIndent=0 if photo else 18, spaceAfter=3),
        "certificate": style("Certificate", 9.5 if photo else 10, 12.3, spaceAfter=4),
        "date": style("Date", 9.5 if photo else 10, 12.2, spaceAfter=4),
        "photo_name": style("PhotoName", 30, 35, True),
        "photo_role": style("PhotoRole", 13.5, 17),
        "photo_contact": style("PhotoContact", 9, 11.5),
        "skill": style("PhotoSkill", 9.5, 12),
    }


def para(text, style):
    return Paragraph(escape(plain(text)), style)


class RuledHeading(Flowable):
    def __init__(self, title, style):
        super().__init__()
        self.paragraph = para(title, style)
        self.spaceBefore = 8
        self.spaceAfter = 3
        self.keepWithNext = True

    def wrap(self, available_width, available_height):
        self.width = available_width
        _, self.text_height = self.paragraph.wrap(available_width, available_height)
        self.height = self.text_height + 2
        return self.width, self.height

    def draw(self):
        self.paragraph.drawOn(self.canv, 0, 2)
        self.canv.setStrokeColor(BLACK)
        self.canv.setLineWidth(.5)
        self.canv.line(0, 0, self.width, 0)


class EntryLine(Flowable):
    """A title with a right-aligned date; no tables in the ATS PDF."""
    def __init__(self, title, date, style):
        super().__init__()
        self.title = para(title, style)
        self.date = date
        self.style = style
        self.keepWithNext = True
        self.spaceAfter = 3

    def wrap(self, available_width, available_height):
        self.width = available_width
        self.date_width = pdfmetrics.stringWidth(self.date, self.style.fontName, self.style.fontSize)
        _, self.height = self.title.wrap(available_width - self.date_width - 12, available_height)
        return self.width, self.height

    def draw(self):
        self.title.drawOn(self.canv, 0, 0)
        self.canv.setFont(self.style.fontName, self.style.fontSize)
        self.canv.setFillColor(BLACK)
        self.canv.drawRightString(self.width, self.height - self.style.fontSize, self.date)


def bullets(items, styles):
    return [Paragraph(escape(plain(text)), styles["bullet"], bulletText="•") for text in items]


def certificate_lines(styles):
    return [Paragraph(
        f'<b>{link(c["title"], certificate_url(c))}</b> - {escape(c["issuer"])} | {escape(c["date"])}',
        styles["certificate"],
    ) for c in P["credentials"]]


def ats_story(styles):
    e = P["education"]
    work = P["experience"]
    return [
        Spacer(1, 24),
        para(P["name"], styles["name"]),
        para("COMPUTER SCIENCE STUDENT", styles["role"]),
        Paragraph(f'{link(P["phone"], P["phoneHref"])} | {link(P["email"], "mailto:" + P["email"])} | {escape(P["location"])}', styles["contact"]),
        Paragraph(f'{link("paul-antigo.vercel.app", P["portfolio"])} | {link("github.com/itszoriel", P["github"])} | {link("LinkedIn", P["linkedin"])}', styles["contact"]),
        RuledHeading("Education", styles["section"]),
        para(e["degree"], styles["entry"]),
        para(f'{e["institution"]}, {e["campus"]}', styles["body"]),
        para(f'{e["period"]} | Expected {e["expectedGraduation"]} | {e["status"]}', styles["body"]),
        RuledHeading("Work Experience", styles["section"]),
        EntryLine(work["title"], plain(work["dates"]), styles["entry"]),
        para(f'{work["organization"]}, {work["location"]} | SPES / DOLE | {work["duration"]}', styles["meta"]),
        *bullets(work["bullets"], styles),
        RuledHeading("Project Experience", styles["section"]),
        EntryLine("MunLink | Developer / Maintainer", "Ongoing", styles["entry"]),
        para(PROJECT_CONTEXT, styles["meta"]),
        Paragraph(f'{link("Live demo", P["project"]["demo"])} | {link("Source repository", P["project"]["repository"])}', styles["meta"]),
        *bullets(P["project"]["resumeBullets"], styles),
        RuledHeading("Technical Skills", styles["section"]),
        *[Paragraph(f'<b>{escape(label)}:</b> {escape(items)}', styles["body"]) for label, items in SKILLS],
        RuledHeading("Course Certificates", styles["section"]),
        *certificate_lines(styles),
    ]


class PhotoHeader(Flowable):
    def __init__(self, styles):
        super().__init__()
        self.styles = styles
        self.height = 116

    def wrap(self, available_width, available_height):
        self.width = available_width
        return self.width, self.height

    def draw(self):
        from reportlab.lib.utils import ImageReader
        c = self.canv
        c.drawImage(ImageReader(str(PHOTO_PATH)), 0, 2, width=114, height=114, preserveAspectRatio=True, mask="auto")
        x = 138
        width = self.width - x
        name_style = self.styles["photo_name"]
        name = para(P["name"].upper(), name_style)
        _, h = name.wrap(width, 100)
        name.drawOn(c, x, self.height - h - 5)
        role = para("Computer Science Student", self.styles["photo_role"])
        _, rh = role.wrap(width, 40)
        role.drawOn(c, x, self.height - h - rh - 9)
        c.setStrokeColor(BLACK)
        c.setLineWidth(.55)
        c.line(x, 38, self.width, 38)
        row = Paragraph(
            f'{link(P["phone"], P["phoneHref"])} | {link(P["email"], "mailto:" + P["email"])} | {link("paul-antigo.vercel.app", P["portfolio"])}',
            self.styles["photo_contact"],
        )
        _, height = row.wrap(width, 30)
        row.drawOn(c, x, 25)
        second = Paragraph(f'{link("LinkedIn", P["linkedin"])} | {link("GitHub", P["github"])} | {escape(P["location"])}', self.styles["photo_contact"])
        _, height = second.wrap(width, 30)
        second.drawOn(c, x, 9)
        c.line(x, 2, self.width, 2)


def photo_entry(left, right, width):
    table = Table([[left, right]], colWidths=[138, width - 138], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (0, 0), 16),
        ("RIGHTPADDING", (1, 0), (1, 0), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return table


def photo_story(styles, width):
    e = P["education"]
    work = P["experience"]
    skills = Table(
        [[Paragraph('• ' + escape(item), styles["skill"]) for item in PHOTO_SKILLS[start:start + 4]] for start in (0, 4)],
        colWidths=[width / 4] * 4,
    )
    skills.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return [
        PhotoHeader(styles), Spacer(1, 16),
        RuledHeading("ABOUT ME", styles["section"]), para(SUMMARY, styles["body"]),
        RuledHeading("EDUCATION", styles["section"]),
        photo_entry(
            [para(e["period"], styles["date"]), para("PRMSU, Iba Campus", styles["date"])],
            [para(e["degree"], styles["entry"]), para(e["institution"], styles["body"]), para(f'Expected {e["expectedGraduation"]} | {e["status"]}', styles["body"])], width),
        RuledHeading("EXPERIENCE", styles["section"]),
        photo_entry(
            [para(work["dates"], styles["date"]), para("SPES / DOLE", styles["date"]), para(work["duration"], styles["date"])],
            [para(work["title"], styles["entry"]), para(f'{work["organization"]}, {work["location"]}', styles["meta"]), *bullets(work["bullets"], styles)], width),
        RuledHeading("PROJECT EXPERIENCE", styles["section"]),
        photo_entry(
            [para("Ongoing", styles["date"]), para("Personal project", styles["date"])],
            [para("MunLink | Developer / Maintainer", styles["entry"]),
             Paragraph(f'{link("Live demo", P["project"]["demo"])} | {link("Source repository", P["project"]["repository"])}', styles["meta"]),
             *bullets(P["project"]["resumeBullets"], styles)], width),
        RuledHeading("SKILLS", styles["section"]), skills,
        RuledHeading("COURSE CERTIFICATES", styles["section"]), *certificate_lines(styles),
    ]


def build_resume(path: Path, include_photo=False):
    styles = make_styles(include_photo)
    page_size = A4 if include_photo else (595, 842)
    margin = 38 if include_photo else 72
    top_margin = 43.5 if include_photo else 56.6
    bottom_margin = 36 if include_photo else 72
    width, height = page_size
    document = BaseDocTemplate(
        str(path), pagesize=page_size,
        leftMargin=margin, rightMargin=margin, topMargin=top_margin, bottomMargin=bottom_margin,
        title=f'{P["name"]} - {"Photo Resume" if include_photo else "ATS Resume"}',
        author=P["name"], subject="Computer Science student - internship, OJT and entry-level opportunities",
        pageCompression=1,
    )
    frame = Frame(margin, bottom_margin, width - 2 * margin, height - top_margin - bottom_margin,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    document.addPageTemplates(PageTemplate(id="Resume", frames=frame))
    document.build(photo_story(styles, width - 2 * margin) if include_photo else ats_story(styles))
    assert_black_pdf(path)
    print(f"Generated template-based resume with verified black text and links: {path}")


def main():
    register_fonts()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    build_resume(ATS_OUTPUT)
    build_resume(PHOTO_OUTPUT, include_photo=True)
    shutil.copy2(ATS_OUTPUT, PUBLIC_DEFAULT)
    from build_ats_docx import build_ats_docx
    build_ats_docx()
    print("Refreshed canonical website downloads and the legacy ATS alias.")
