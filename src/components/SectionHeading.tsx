type SectionHeadingProps = {
  number: string
  title: string
  description?: string
}

export function SectionHeading({ number, title, description }: SectionHeadingProps) {
  return (
    <div className="section-heading">
      <div className="section-index" aria-hidden="true">{number}</div>
      <div>
        <h2>{title}</h2>
        {description && <p>{description}</p>}
      </div>
    </div>
  )
}
