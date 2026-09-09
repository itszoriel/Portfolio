type PALogoProps = {
  className?: string
}

export function PALogo({ className }: PALogoProps) {
  return <img className={className} src="/pa-logo-header.png" alt="" width="46" height="30" aria-hidden="true" />
}
