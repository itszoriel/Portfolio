import { useEffect, useId, useRef, useState } from 'react'
import { Download, FileText, UserRound, X } from 'lucide-react'
import { phResumeUrl, resumeUrl } from '../content'

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
    <button className="icon-button resume-button" type="button" onClick={() => setOpen(true)} title="Choose a resume format">
      <Download size={16} aria-hidden="true" /><span>Resume</span>
    </button>
  ) : variant === 'mobile' ? (
    <button className="mobile-resume-trigger" type="button" onClick={() => setOpen(true)}>
      <span>PDF</span>Download resume
    </button>
  ) : (
    <button className="button text-button" type="button" onClick={() => setOpen(true)}>
      Download resume <Download size={16} aria-hidden="true" />
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
              <span>Resume formats</span>
              <h2 id={titleId}>Choose a version</h2>
            </div>
            <button type="button" onClick={close} aria-label="Close resume options"><X size={18} /></button>
          </div>
          <p className="resume-dialog-intro">Both versions contain the same verified experience, project work, education, and credentials.</p>
          <div className="resume-options">
            <a href={resumeUrl} download onClick={close}>
              <FileText size={21} aria-hidden="true" />
              <span><strong>ATS resume</strong><small>Single-column and optimized for online applications.</small></span>
              <Download size={16} aria-hidden="true" />
            </a>
            <a href={phResumeUrl} download onClick={close}>
              <UserRound size={21} aria-hidden="true" />
              <span><strong>Photo resume</strong><small>Professional layout with a formal portrait.</small></span>
              <Download size={16} aria-hidden="true" />
            </a>
          </div>
        </div>
      </dialog>
    </>
  )
}
