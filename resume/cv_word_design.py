"""Editable Word counterpart to the CV's monochrome typesetting."""

from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Twips

from document_common import certificate_title, certificate_url


def rule(paragraph, edge='bottom', *, color='C9C9C9', size=4, space=5):
    properties = paragraph._p.get_or_add_pPr()
    borders = properties.find(qn('w:pBdr'))
    if borders is None:
        borders = OxmlElement('w:pBdr')
        properties.append(borders)
    line = OxmlElement('w:' + edge)
    for key, value in [('val', 'single'), ('sz', size), ('space', space), ('color', color)]:
        line.set(qn('w:' + key), str(value))
    borders.append(line)


def table_grid(document, entries, *, padding=120):
    section = document.sections[0]
    total = section.page_width.twips - section.left_margin.twips - section.right_margin.twips
    gap = 280
    first = (total - gap) // 2
    widths = [first, gap, total - gap - first]
    table = document.add_table(rows=(entries + 1) // 2, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    table.autofit = False
    properties = table._tbl.tblPr
    properties.find(qn('w:tblW')).set(qn('w:type'), 'dxa')
    properties.find(qn('w:tblW')).set(qn('w:w'), str(total))
    indent = OxmlElement('w:tblInd')
    indent.set(qn('w:w'), '0')
    indent.set(qn('w:type'), 'dxa')
    properties.append(indent)
    for column, width in zip(table.columns, widths):
        column.width = Twips(width)
    result = []
    for row in table.rows:
        for index, (cell, width) in enumerate(zip(row.cells, widths)):
            cell.width = Twips(width)
            cell_properties = cell._tc.get_or_add_tcPr()
            margins = OxmlElement('w:tcMar')
            for edge in ('top', 'bottom', 'start', 'end'):
                margin = OxmlElement('w:' + edge)
                margin.set(qn('w:w'), str(0 if index == 1 else padding))
                margin.set(qn('w:type'), 'dxa')
                margins.append(margin)
            cell_properties.append(margins)
            if index != 1:
                shading = OxmlElement('w:shd')
                shading.set(qn('w:val'), 'clear')
                shading.set(qn('w:fill'), 'F5F5F3')
                cell_properties.append(shading)
                borders = OxmlElement('w:tcBorders')
                bottom = OxmlElement('w:bottom')
                for key, value in [('val', 'single'), ('sz', '32'), ('color', 'FFFFFF')]:
                    bottom.set(qn('w:' + key), value)
                borders.append(bottom)
                cell_properties.append(borders)
                result.append(cell)
            for paragraph in cell.paragraphs:
                paragraph.paragraph_format.space_before = Pt(0)
                paragraph.paragraph_format.space_after = Pt(0)
    return result[:entries]


def skills(document, groups, set_font):
    for cell, (label, value) in zip(table_grid(document, len(groups)), groups):
        paragraph = cell.paragraphs[0]
        paragraph.style = document.styles['CV Skill']
        set_font(paragraph.add_run(label + ': '), bold=True)
        set_font(paragraph.add_run(value))


def certificates(document, credentials, add_hyperlink, set_font):
    for cell, credential in zip(table_grid(document, len(credentials), padding=180), credentials):
        paragraph = cell.paragraphs[0]
        paragraph.style = document.styles['CV Certificate']
        add_hyperlink(paragraph, certificate_title(credential), certificate_url(credential), size=10.5, bold=True)
        paragraph.add_run().add_break()
        set_font(paragraph.add_run(f'{credential["issuer"]} | {credential["date"]}.'))
        if credential['verificationUrl']:
            paragraph.add_run(' ')
            add_hyperlink(paragraph, 'Badge verification', credential['verificationUrl'], size=10.5)
