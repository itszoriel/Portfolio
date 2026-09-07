import { useEffect, useId, useRef, useState } from 'react'
import { Download, Files, FileText, UserRound, X } from 'lucide-react'
import { cvUrl, phResumeUrl, resumeUrl } from '../content'

type ResumePickerProps = {
  variant?: 'hero' | 'header' | 'mobile'
}

export function ResumePicker({ variant = 'hero' }: ResumePickerProps) {
  const [open, setOpen] = useState(false)
  const dialogRef = useRef<HTMLDialogElement>(null)
  const titleId = useId()

  useEffect(() => {
    const dialog = dialogRef.current
    if (!dialog) return
    if (open && !dialog.open) dialog.showModal()
    if (!open && dialog.open) dialog.close()
  }, [open])

  const close = () => setOpen(false)

  const trigger = variant === 'header' ? (
    <button className="icon-button resume-button" type="button" onClick={() => setOpen(true)} title="Choose an application document">
      <Download size={16} aria-hidden="true" /><span>Documents</span>
    </button>
  ) : variant === 'mobile' ? (
    <button className="mobile-resume-trigger" type="button" onClick={() => setOpen(true)}>
      <span>PDF</span>Application documents
    </button>
  ) : (
    <button className="button text-button" type="button" onClick={() => setOpen(true)}>
      Download documents <Download size={16} aria-hidden="true" />
    </button>
  )

  return (
    <>
      {trigger}
      <dialog
        ref={dialogRef}
        className="resume-dialog"
        aria-labelledby={titleId}
        onClose={close}
        onClick={(event) => event.target === event.currentTarget && close()}
      >
        <div className="resume-dialog-panel">
          <div className="resume-dialog-heading">
            <div>
              <span>Application documents</span>
              <p className="resume-dialog-title" id={titleId}>Choose a document</p>
            </div>
            <button type="button" onClick={close} aria-label="Close document options"><X size={18} /></button>
          </div>
          <p className="resume-dialog-intro">Use the concise resume for job applications or the detailed curriculum vitae for academic and professional review.</p>
          <div className="resume-options">
            <a href={resumeUrl} download onClick={close}>
              <FileText size={21} aria-hidden="true" />
              <span><strong>ATS resume</strong><small>Single-column and optimized for online applications.</small></span>
              <Download size={16} aria-hidden="true" />
            </a>
            <a href={phResumeUrl} download onClick={close}>
              <UserRound size={21} aria-hidden="true" />
              <span><strong>Photo resume</strong><small>Philippine-style layout with a formal portrait.</small></span>
              <Download size={16} aria-hidden="true" />
            </a>
            <a href={cvUrl} download onClick={close}>
              <Files size={21} aria-hidden="true" />
              <span><strong>Curriculum vitae</strong><small>Detailed project, research, education, and training record.</small></span>
              <Download size={16} aria-hidden="true" />
            </a>
          </div>
        </div>
      </dialog>
    </>
  )
}
