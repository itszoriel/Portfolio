import { lazy, Suspense, useEffect, useState } from 'react'
import { Route, Routes, useLocation } from 'react-router-dom'
import { CommandMenu } from './components/CommandMenu'
import { Header } from './components/Header'
import { useTheme } from './hooks'
import { HomePage } from './pages/HomePage'

const MunLinkCaseStudy = lazy(() => import('./pages/MunLinkCaseStudy').then((module) => ({ default: module.MunLinkCaseStudy })))

function App() {
  const { isDark, toggleTheme } = useTheme()
  const [commandOpen, setCommandOpen] = useState(false)
  const location = useLocation()

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      const target = event.target as HTMLElement
      const isTyping = target.matches('input, textarea, select, [contenteditable="true"]')
      if ((event.key === '/' && !isTyping) || ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k')) {
        event.preventDefault()
        setCommandOpen(true)
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  useEffect(() => {
    if (location.hash) {
      requestAnimationFrame(() => document.querySelector(location.hash)?.scrollIntoView())
    } else {
      window.scrollTo({ top: 0 })
    }
  }, [location.pathname, location.hash])

  return (
    <div className="site-shell">
      <Header isDark={isDark} toggleTheme={toggleTheme} openCommandMenu={() => setCommandOpen(true)} />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/work/munlink" element={<Suspense fallback={<main className="route-loading" aria-label="Loading case study" />}><MunLinkCaseStudy /></Suspense>} />
      </Routes>
      <CommandMenu open={commandOpen} onClose={() => setCommandOpen(false)} />
    </div>
  )
}

export default App
