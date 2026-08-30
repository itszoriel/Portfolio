type PALogoProps = {
  className?: string
}

export function PALogo({ className }: PALogoProps) {
  return (
    <svg className={className} viewBox="0 0 44 44" role="img" aria-label="Paul Antigo PA monogram">
      <rect className="pa-logo-frame" x="1.5" y="1.5" width="41" height="41" rx="2" />
      <path className="pa-logo-p" d="M11 33V11h8.2c5.4 0 8.3 2.7 8.3 7s-2.9 7-8.3 7H11m0-8h8c2.1 0 3.3-1.1 3.3-3" />
      <path className="pa-logo-a" d="M21.5 33 30 11l8.5 22M25.2 25.5h9.6" />
    </svg>
  )
}
