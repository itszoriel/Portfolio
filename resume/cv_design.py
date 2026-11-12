"""Monochrome CV design: Georgia display type, Calibri text, structured grids."""

from __future__ import annotations

import os
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Flowable, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle

from document_common import BLACK, PROFILE as P, certificate_title, certificate_url, link

MARGIN = 48
PANEL = colors.HexColor('#F5F5F3')
RULE = colors.HexColor('#C9C9C9')


def register_fonts():
    installed = Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts'
    calibri = Path(os.environ.get('RESUME_CALIBRI_DIR', str(installed)))
    georgia = Path(os.environ.get('CV_SERIF_FONT_DIR', str(installed)))
    for name, directory, filename in [
        ('CVText', calibri, 'calibri.ttf'),
        ('CVText-Bold', calibri, 'calibrib.ttf'),
        ('CVText-Italic', calibri, 'calibrii.ttf'),
        ('CVDisplay', georgia, 'georgia.ttf'),
        ('CVDisplay-Bold', georgia, 'georgiab.ttf'),
    ]:
        path = directory / filename
        if not path.is_file():
            raise FileNotFoundError(f'CV font not found: {path}. Set RESUME_CALIBRI_DIR / CV_SERIF_FONT_DIR to licensed installed font directories.')
        pdfmetrics.registerFont(TTFont(name, str(path)))
    pdfmetrics.registerFontFamily('CVText', normal='CVText', bold='CVText-Bold', italic='CVText-Italic', boldItalic='CVText-Bold')


def make_styles():
    def style(name, size=10.5, leading=13.5, font='CVText', **kwargs):
        return ParagraphStyle(name, fontName=font, fontSize=size, leading=leading,
                              textColor=BLACK, bulletColor=BLACK,
                              bulletFontName='CVText', bulletFontSize=size, **kwargs)
    return {
        'name': style('CVName', 32, 38, 'CVDisplay'),
        'contact': style('CVContact', 9.8, 12.5),
        'section': style('CVSection', 14.5, 18, 'CVDisplay-Bold'),
        'entry': style('CVEntry', 11.5, 14.5, 'CVText-Bold', spaceBefore=3, spaceAfter=4, keepWithNext=True),
        'body': style('CVBody', spaceAfter=4),
        'compact': style('CVCompact', 10.5, 13.5, spaceAfter=3),
        'meta': style('CVMeta', 9.6, 12, spaceAfter=2, keepWithNext=True),
        'bullet': style('CVBullet', leftIndent=13, firstLineIndent=0, bulletIndent=0, spaceAfter=3),
        'skill': style('CVSkill', 10, 12.6),
        'certificate': style('CVCertificate', 10.5, 13.5),
        'footer': style('CVFooter', 8.5, 11),
    }


def tracked(canvas, text, x, y, *, size=9, spacing=.65):
    canvas.saveState()
    text_object = canvas.beginText(x, y)
    text_object.setFont('CVText-Bold', size)
    text_object.setCharSpace(spacing)
    text_object.setFillColor(BLACK)
    text_object.textOut(text)
    canvas.drawText(text_object)
    canvas.restoreState()


class Masthead(Flowable):
    def __init__(self, styles):
        super().__init__()
        self.styles = styles
        self.height = 100

    def wrap(self, available_width, available_height):
        self.width = available_width
        return self.width, self.height

    def draw(self):
        canvas = self.canv
        canvas.setFillColor(BLACK)
        canvas.rect(-13, self.height - 50, 3, 43, fill=1, stroke=0)
        tracked(canvas, 'CURRICULUM VITAE', 0, self.height - 9, size=9.3)
        name = Paragraph(escape(P['name']), self.styles['name'])
        _, height = name.wrap(self.width, 48)
        name.drawOn(canvas, 0, self.height - height - 20)
        contact = Paragraph(
            f'{escape(P["location"])} | {link(P["phone"], P["phoneHref"])} | {link(P["email"], "mailto:" + P["email"])}',
            self.styles['contact'])
        _, height = contact.wrap(self.width, 28)
        contact.drawOn(canvas, 0, 25)
        networks = Paragraph(f'{link("Portfolio", P["portfolio"])} | {link("LinkedIn", P["linkedin"])} | {link("GitHub", P["github"])}', self.styles['contact'])
        _, height = networks.wrap(self.width, 28)
        networks.drawOn(canvas, 0, 8)
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(.65)
        canvas.line(0, 0, self.width, 0)


class SectionHeading(Flowable):
    def __init__(self, title, style):
        super().__init__()
        self.title = title
        self.style = style
        self.paragraph = Paragraph(escape(title), style)
        self.spaceBefore = 8
        self.spaceAfter = 4
        self.keepWithNext = True

    def wrap(self, available_width, available_height):
        self.width = available_width
        _, self.height = self.paragraph.wrap(available_width, available_height)
        return self.width, self.height

    def draw(self):
        self.paragraph.drawOn(self.canv, 0, 0)
        end = pdfmetrics.stringWidth(self.title, self.style.fontName, self.style.fontSize) + 16
        if end < self.width - 20:
            self.canv.setStrokeColor(RULE)
            self.canv.setLineWidth(.5)
            self.canv.line(end, self.height * .48, self.width, self.height * .48)


def grid(paragraphs, width, *, padding=6):
    gutter = 14
    column = (width - gutter) / 2
    data = [[paragraphs[index], '', paragraphs[index + 1] if index + 1 < len(paragraphs) else ''] for index in range(0, len(paragraphs), 2)]
    table = Table(data, colWidths=[column, gutter, column], hAlign='LEFT')
    instructions = [
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), padding),
        ('RIGHTPADDING', (0, 0), (-1, -1), padding),
        ('TOPPADDING', (0, 0), (-1, -1), padding),
        ('BOTTOMPADDING', (0, 0), (-1, -1), padding),
        ('BACKGROUND', (0, 0), (0, -1), PANEL),
        ('BACKGROUND', (2, 0), (2, -1), PANEL),
        ('LEFTPADDING', (1, 0), (1, -1), 0),
        ('RIGHTPADDING', (1, 0), (1, -1), 0),
    ]
    for row in range(len(data) - 1):
        instructions += [('LINEBELOW', (0, row), (0, row), 4, colors.white), ('LINEBELOW', (2, row), (2, row), 4, colors.white)]
    table.setStyle(TableStyle(instructions))
    table.spaceAfter = 5
    return table


def skill_grid(skills, styles, width):
    return grid([Paragraph(f'<b>{escape(label)}:</b> {escape(text)}', styles['skill']) for label, text in skills], width)


def certificate_grid(credentials, styles, width):
    cells = []
    for credential in credentials:
        verification = f' {link("Badge verification", credential["verificationUrl"])}' if credential['verificationUrl'] else ''
        cells.append(Paragraph(
            f'<b>{link(certificate_title(credential), certificate_url(credential))}</b><br/>'
            f'{escape(credential["issuer"])} | {escape(credential["date"])}.{verification}',
            styles['certificate']))
    return grid(cells, width, padding=9)


def page_furniture(canvas, document):
    canvas.saveState()
    width, height = A4
    if document.page > 1:
        canvas.setFont('CVText-Bold', 9)
        canvas.setFillColor(BLACK)
        canvas.drawString(MARGIN, height - 33, P['name'].upper())
        canvas.setFont('CVText', 8.5)
        canvas.drawRightString(width - MARGIN, height - 33, 'CURRICULUM VITAE')
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(.5)
        canvas.line(MARGIN, height - 43, width - MARGIN, height - 43)
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(.5)
    canvas.line(MARGIN, 36, width - MARGIN, 36)
    canvas.setFont('CVText', 8.5)
    canvas.setFillColor(BLACK)
    canvas.drawString(MARGIN, 22, 'CURRICULUM VITAE')
    canvas.setFont('CVText-Bold', 8.5)
    canvas.drawRightString(width - MARGIN, 22, f'{document.page:02d} / 03')
    canvas.restoreState()


def make_document(path):
    width, height = A4
    document = BaseDocTemplate(
        str(path), pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=42, bottomMargin=48, title=P['name'] + ' - Curriculum Vitae',
        author=P['name'], subject='Comprehensive curriculum vitae for software engineering, OJT, and academic opportunities',
    )
    def frame(top):
        return Frame(MARGIN, 48, width - MARGIN * 2, height - top - 48,
                     leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    document.addPageTemplates([
        PageTemplate(id='First', frames=frame(42), onPage=page_furniture, autoNextPageTemplate='Continuation'),
        PageTemplate(id='Continuation', frames=frame(68), onPage=page_furniture),
    ])
    return document
