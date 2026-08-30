import { ArrowUpRight } from 'lucide-react'

type SocialLinkProps = {
  label: string
  href: string
  compact?: boolean
}

export function SocialLink({ label, href, compact = false }: SocialLinkProps) {
  if (!href) {
    return (
      <span className={`social-link is-placeholder ${compact ? 'compact' : ''}`} aria-disabled="true" title={`${label} URL has not been added yet`}>
        {label}
        {!compact && <small>Add link</small>}
      </span>
    )
  }

  const opensNewTab = href.startsWith('http')

  return (
    <a
      className={`social-link ${compact ? 'compact' : ''}`}
      href={href}
      target={opensNewTab ? '_blank' : undefined}
      rel={opensNewTab ? 'noreferrer' : undefined}
    >
      {label}<ArrowUpRight size={15} aria-hidden="true" />
    </a>
  )
}
