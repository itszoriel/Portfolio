import { useEffect, useMemo, useRef, useState, type FormEvent, type KeyboardEvent } from 'react'
import { ArrowRight, ChevronDown, Download, ExternalLink, Search, X } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { emailAddress, phResumeUrl, resumeUrl, socialLinks } from '../content'

type CommandMenuProps = {
  open: boolean
  onClose: () => void
}

type SearchCommand = {
  label: string
  keywords: string
  href: string
  kind: 'internal' | 'external' | 'download'
}

const navigationCommands: SearchCommand[] = [
  { label: 'View Projects', keywords: 'work portfolio', href: '/#projects', kind: 'internal' },
  { label: 'MunLink', keywords: 'project case study civic tech', href: '/work/munlink', kind: 'internal' },
  { label: 'Experience', keywords: 'work spes cisco', href: '/#experience', kind: 'internal' },
  { label: 'Skills', keywords: 'technical technologies stack', href: '/#skills', kind: 'internal' },
  { label: 'Credentials', keywords: 'certificates learning courses', href: '/#credentials', kind: 'internal' },
  { label: 'About Me', keywords: 'profile biography', href: '/#about', kind: 'internal' },
  { label: 'Contact Me', keywords: 'connect opportunities', href: '/#contact', kind: 'internal' },
]

const resumeCommands: SearchCommand[] = [
  { label: 'ATS Resume', keywords: 'download cv', href: resumeUrl, kind: 'download' },
  { label: 'Photo Resume', keywords: 'download cv portrait philippines', href: phResumeUrl, kind: 'download' },
]

const socialCommands: SearchCommand[] = [
  ...(socialLinks.linkedin ? [{ label: 'LinkedIn', keywords: 'social professional', href: socialLinks.linkedin, kind: 'external' as const }] : []),
  ...(socialLinks.github ? [{ label: 'GitHub', keywords: 'social code repositories', href: socialLinks.github, kind: 'external' as const }] : []),
  ...(socialLinks.instagram ? [{ label: 'Instagram', keywords: 'social', href: socialLinks.instagram, kind: 'external' as const }] : []),
  ...(socialLinks.email ? [{ label: emailAddress, keywords: 'email gmail contact', href: socialLinks.email, kind: 'external' as const }] : []),
]

const searchCommands = [...navigationCommands, ...resumeCommands, ...socialCommands]

function normalize(value: string) {
  return value.toLocaleLowerCase().replace(/[^a-z0-9@.]+/g, '')
}

function greedyMatch(command: SearchCommand, query: string) {
  const haystack = normalize(`${command.label} ${command.keywords}`)
  const needle = normalize(query)

  if (!needle) return true
  if (haystack.includes(needle)) return true

  let index = 0
  for (const character of haystack) {
    if (character === needle[index]) index += 1
    if (index === needle.length) return true
  }

  return false
}

export function CommandMenu({ open, onClose }: CommandMenuProps) {
  const [query, setQuery] = useState('')
  const [projectsPinned, setProjectsPinned] = useState(false)
  const [projectsHovered, setProjectsHovered] = useState(false)
  const dialogRef = useRef<HTMLDialogElement>(null)
  const searchRef = useRef<HTMLInputElement>(null)
  const navigate = useNavigate()
  const projectsVisible = projectsPinned || projectsHovered

  const searchResults = useMemo(
    () => searchCommands.filter((command) => greedyMatch(command, query)),
    [query],
  )

  useEffect(() => {
    const dialog = dialogRef.current
    if (!dialog) return

    if (open && !dialog.open) {
      setQuery('')
      setProjectsPinned(false)
      setProjectsHovered(false)
      dialog.showModal()
      requestAnimationFrame(() => searchRef.current?.focus())
    }

    if (!open && dialog.open) dialog.close()
  }, [open])

  const go = (href: string) => {
    onClose()

    if (href.startsWith('/#')) {
      navigate(href)
      const sectionId = href.split('#')[1]
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          document.getElementById(sectionId)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
        })
      })
      return
    }

    navigate(href)
  }

  const submitSearch = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    dialogRef.current?.querySelector<HTMLElement>('[data-search-result]')?.click()
  }

  const handleKeyDown = (event: KeyboardEvent<HTMLDialogElement>) => {
    if (!['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(event.key)) return

    const items = Array.from(dialogRef.current?.querySelectorAll<HTMLElement>('[data-command-item]') ?? [])
      .filter((item) => item.offsetParent !== null)
    if (!items.length) return

    event.preventDefault()
    const currentIndex = items.indexOf(document.activeElement as HTMLElement)
    const nextIndex = event.key === 'Home'
      ? 0
      : event.key === 'End'
        ? items.length - 1
        : event.key === 'ArrowDown'
          ? (currentIndex + 1) % items.length
          : (currentIndex <= 0 ? items.length : currentIndex) - 1

    items[nextIndex]?.focus()
  }

  const renderCommand = (command: SearchCommand, searchResult = false) => {
    const icon = command.kind === 'download'
      ? <Download size={15} aria-hidden="true" />
      : command.kind === 'external'
        ? <ExternalLink size={15} aria-hidden="true" />
        : <ArrowRight size={15} aria-hidden="true" />
    const dataProps = {
      'data-command-item': true,
      ...(searchResult ? { 'data-search-result': true } : {}),
    }

    if (command.kind === 'internal') {
      return (
        <button key={command.href} type="button" {...dataProps} onClick={() => go(command.href)}>
          <span>{command.label}</span>{icon}
        </button>
      )
    }

    return (
      <a
        key={command.href}
        href={command.href}
        {...dataProps}
        {...(command.kind === 'download' ? { download: true } : {})}
        {...(command.href.startsWith('http') ? { target: '_blank', rel: 'noreferrer' } : {})}
        onClick={onClose}
      >
        <span>{command.label}</span>{icon}
      </a>
    )
  }

  return (
    <dialog
      ref={dialogRef}
      className="command-menu"
      onClose={onClose}
      onKeyDown={handleKeyDown}
      onClick={(event) => event.target === event.currentTarget && onClose()}
    >
      <div className="command-panel">
        <form className="command-header" role="search" onSubmit={submitSearch}>
          <input
            ref={searchRef}
            type="search"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Go somewhere"
            aria-label="Search portfolio navigation"
            autoComplete="off"
          />
          <button className="command-search-button" type="submit" aria-label="Open first search result">
            <Search size={17} aria-hidden="true" />
          </button>
          <button className="command-close-button" type="button" onClick={onClose} aria-label="Close quick navigation">
            <X size={17} aria-hidden="true" />
          </button>
        </form>

        <div className="command-list">
          {query ? (
            <section className="command-group" aria-label="Search results">
              <div className="command-group-title"><span>Results</span></div>
              {searchResults.length > 0
                ? searchResults.map((command) => renderCommand(command, true))
                : <p className="command-empty">No matching destination.</p>}
            </section>
          ) : (
            <>
              <section className="command-group" aria-label="Navigate">
                <div className="command-group-title"><span>Navigate</span></div>
                <div
                  className={`command-projects${projectsVisible ? ' is-open' : ''}`}
                  onMouseEnter={() => setProjectsHovered(true)}
                  onMouseLeave={() => setProjectsHovered(false)}
                >
                  <button
                    type="button"
                    data-command-item
                    aria-expanded={projectsVisible}
                    aria-controls="command-project-list"
                    onClick={() => setProjectsPinned((current) => !current)}
                  >
                    <span>View Projects</span>
                    <ChevronDown size={15} aria-hidden="true" />
                  </button>
                  <div id="command-project-list" className="command-submenu" aria-hidden={!projectsVisible}>
                    <button type="button" data-command-item tabIndex={projectsVisible ? 0 : -1} onClick={() => go('/work/munlink')}>
                      <span>MunLink</span>
                      <ArrowRight size={15} aria-hidden="true" />
                    </button>
                  </div>
                </div>
                {navigationCommands.slice(2).map((command) => renderCommand(command))}
              </section>

              <section className="command-group" aria-label="Resume">
                <div className="command-group-title"><span>Resume</span></div>
                {resumeCommands.map((command) => renderCommand(command))}
              </section>

              <section className="command-group" aria-label="Socials">
                <div className="command-group-title"><span>Socials</span></div>
                {socialCommands.map((command) => renderCommand(command))}
              </section>
            </>
          )}
        </div>

        <div className="command-footer">
          <span><kbd>up</kbd><kbd>down</kbd> navigate</span>
          <span><kbd>enter</kbd> open</span>
          <span><kbd>esc</kbd> close</span>
        </div>
      </div>
    </dialog>
  )
}
