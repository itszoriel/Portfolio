# Paul John E. Antigo - Portfolio

This is my personal developer portfolio. It includes my projects, experience, skills, credentials, and a case study for MunLink.

Built with React, TypeScript, Vite, and Tailwind CSS.

## Run locally

```bash
npm install
npm run dev
```

Use `npm run build` to create a production build.

## Application documents

Shared contact details, education, credentials, study plans, and project facts live
in `src/data/profile.json`. Both the website and document generators read it.
Resume layout is in `resume/build_resumes.py`; the editable ATS Word source is filled
by `resume/build_ats_docx.py` from the supplied Word template in `resume/templates/`.
The detailed CV layout and additional
research content are in `resume/generate_cv.py`. Shared PDF styles enforce black text.

```bash
python -m pip install -r resume/requirements.txt
python resume/generate_resumes.py
python resume/generate_cv.py
python resume/verify_documents.py
```

PDFs are generated directly into `public/resumes/`. The default ATS download at
`public/Paul-John-Antigo-Resume.pdf` is also refreshed. The editable CV is generated
at `resume/Paul-John-Antigo-CV-Editable.docx`, and the editable ATS resume at
`resume/Paul-John-Antigo-ATS-Resume-Editable.docx`. All three PDFs have selectable text
and clickable phone, email, social, portfolio, and certificate links. The ATS resume
follows the supplied single-column Word template with a centered header, Calibri,
ruled section headings, and right-aligned dates. The photo resume follows the supplied
PDF template with an upper-left portrait, Montserrat, full-width ruled headings, and
date/detail rows. Both resumes are one page.
The CV uses intentional section breaks across three pages, with a Georgia masthead,
Calibri body text, structured competency/certificate grids, fine section rules, and
consistent running headers and page numbers. Its typography and PDF layout live in
`resume/cv_design.py`; the editable Word counterpart is in `resume/cv_word_design.py`.

Calibri is read from the user's installed Windows fonts; set `RESUME_CALIBRI_DIR`
to a licensed installed Calibri directory on other systems. Montserrat and its OFL
license are included in `resume/fonts/`. The supplied reference documents remain
unchanged. The ATS Word package retains the template's styles, numbering, theme,
and page geometry, with black text and Paul's content replacing the example slots.
The CV also reads the user's installed Georgia fonts; `CV_SERIF_FONT_DIR` can point
to an existing licensed Georgia installation. Microsoft font files are not redistributed.

The final PDFs are rendered and visually checked. The editable Word files are checked
structurally; their Word-rendered layout could not be verified here because LibreOffice
is unavailable and the installed Word PDF exporter did not complete.

The generators reject colored PDF text or missing contact/certificate links.
The verifier also checks page counts, consistent facts, DOCX text colors, and the
legacy download alias. Render the PDFs and review every page after content changes;
automated checks do not establish visual quality or universal ATS compatibility.
See `resume/content-review.md` for evidence and items that still need owner review.

Run `npm run build` after regenerating documents, followed by `npm run preview` to
check the production output. Every document menu reads the canonical paths in
`src/content.ts`; `/Paul-John-Antigo-Resume.pdf` remains a supported legacy alias.
The original hero is preserved. Credentials is the first content section after the
hero, followed by Experience, Skills, Projects, About, and Contact. Website colors continue to adapt
to light and dark themes.
