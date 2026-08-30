import { useEffect, useState, type MouseEvent } from 'react'
import { ArrowUpRight, Menu, Moon, Sun, X } from 'lucide-react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { emailAddress, navigation, socialLinks } from '../content'
import { PALogo } from './PALogo'
import { ResumePicker } from './ResumePicker'

type HeaderProps = {
  isDark: boolean
  toggleTheme: () => void
  openCommandMenu: () => void
}

export function Header({ isDark, toggleTheme, openCommandMenu }: HeaderProps) {
  const [menuOpen, setMenuOpen] = useState(false)
  const [activeSection, setActiveSection] = useState<string | null>(null)
  const location = useLocation()
  const navigate = useNavigate()

  useEffect(() => setMenuOpen(false), [location])

  useEffect(() => {
    if (location.pathname !== '/') {
      setActiveSection(null)
      return
    }

    let animationFrame = 0
    let disposed = false

    const updateActiveSection = () => {
      animationFrame = 0
      const marker = window.scrollY + 72 + window.innerHeight * 0.45
      const sections = navigation
        .map((item) => {
          const id = item.href.split('#')[1]
          const element = document.getElementById(id)
          return element ? { id, top: element.offsetTop } : null
        })
        .filter((section): section is { id: string; top: number } => section !== null)
        .sort((a, b) => a.top - b.top)

      let nextSection: string | null = null
      for (const section of sections) {
        if (section.top > marker) break
        nextSection = section.id
      }

      const pageBottom = window.scrollY + window.innerHeight
      if (sections.length && pageBottom >= document.documentElement.scrollHeight - 4) {
        nextSection = sections.at(-1)?.id ?? null
      }

      setActiveSection((current) => current === nextSection ? current : nextSection)
    }

    const scheduleUpdate = () => {
      if (disposed || animationFrame) return
      animationFrame = requestAnimationFrame(updateActiveSection)
    }

    updateActiveSection()
    window.addEventListener('scroll', scheduleUpdate, { passive: true })
    window.addEventListener('resize', scheduleUpdate)
    document.fonts.ready.then(scheduleUpdate)

    return () => {
      disposed = true
      window.removeEventListener('scroll', scheduleUpdate)
      window.removeEventListener('resize', scheduleUpdate)
      if (animationFrame) cancelAnimationFrame(animationFrame)
    }
  }, [location.pathname])

  const handleBrandClick = (event: MouseEvent<HTMLAnchorElement>) => {
    event.preventDefault()
    setMenuOpen(false)

    if (location.pathname !== '/' || location.hash !== '#top') {
      navigate('/#top')
    }

    requestAnimationFrame(() => {
      document.getElementById('top')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    })
  }

  return (
    <header className="site-header">
      <div className="header-inner">
        <Link className="brand" to="/#top" onClick={handleBrandClick} aria-label="Paul Antigo — back to top">
          <PALogo className="pa-logo" />
        </Link>

        <nav className="desktop-nav" aria-label="Primary navigation">
          {navigation.map((item) => {
            const isActive = activeSection === item.href.split('#')[1]
            return (
              <a
                key={item.href}
                href={item.href}
                className={isActive ? 'is-active' : undefined}
                aria-current={isActive ? 'location' : undefined}
              >
                <span>{item.number}</span>{item.label}
              </a>
            )
          })}
        </nav>

        <div className="header-actions">
          <button className="command-trigger" type="button" onClick={openCommandMenu} aria-label="Open quick navigation">
            <span>Jump to</span><kbd>⌘K</kbd>
          </button>
          <ResumePicker variant="header" />
          <button className="icon-button theme-toggle" type="button" onClick={toggleTheme} aria-label={`Switch to ${isDark ? 'light' : 'dark'} mode`}>
            {isDark ? <Sun size={17} /> : <Moon size={17} />}
          </button>
          <button className="icon-button mobile-menu-button" type="button" onClick={() => setMenuOpen((value) => !value)} aria-expanded={menuOpen} aria-controls="mobile-menu" aria-label="Toggle navigation menu">
            {menuOpen ? <X size={19} /> : <Menu size={19} />}
          </button>
        </div>
      </div>

      <nav id="mobile-menu" className={`mobile-nav ${menuOpen ? 'is-open' : ''}`} aria-label="Mobile navigation">
        {navigation.map((item) => {
          const isActive = activeSection === item.href.split('#')[1]
          return (
            <a
              key={item.href}
              href={item.href}
              className={isActive ? 'is-active' : undefined}
              aria-current={isActive ? 'location' : undefined}
            >
              <span>{item.number}</span>{item.label}
            </a>
          )
        })}
        <ResumePicker variant="mobile" />
        <div className="mobile-nav-socials" aria-label="Social links">
          <span>Socials</span>
          <div>
            <a href={socialLinks.linkedin} target="_blank" rel="noreferrer" onClick={() => setMenuOpen(false)}>
              <span>IN</span>LinkedIn<ArrowUpRight size={14} aria-hidden="true" />
            </a>
            <a href={socialLinks.github} target="_blank" rel="noreferrer" onClick={() => setMenuOpen(false)}>
              <span>GH</span>GitHub<ArrowUpRight size={14} aria-hidden="true" />
            </a>
            <a href={socialLinks.instagram} target="_blank" rel="noreferrer" onClick={() => setMenuOpen(false)}>
              <span>IG</span>Instagram<ArrowUpRight size={14} aria-hidden="true" />
            </a>
            <a href={socialLinks.email} onClick={() => setMenuOpen(false)}>
              <span>@</span>{emailAddress}<ArrowUpRight size={14} aria-hidden="true" />
            </a>
          </div>
        </div>
      </nav>
    </header>
  )
}
