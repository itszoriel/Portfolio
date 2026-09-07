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

The active content and layout sources are `resume/generate_resumes.py` and
`resume/generate_cv.py`.

```bash
python -m pip install reportlab python-docx
python resume/generate_resumes.py
python resume/generate_cv.py
```

PDFs are generated directly into `public/resumes/`. The default ATS download at
`public/Paul-John-Antigo-Resume.pdf` is also refreshed. The editable CV is generated
at `resume/Paul-John-Antigo-CV.docx`. Run the site build after regenerating documents.
