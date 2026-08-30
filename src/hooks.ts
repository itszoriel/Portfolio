import { useEffect, useRef, useState } from 'react'

const revealElements = new Set<HTMLElement>()
let revealObserver: IntersectionObserver | null = null

function getRevealObserver() {
  if (revealObserver || !('IntersectionObserver' in window)) return revealObserver

  revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return
        const element = entry.target as HTMLElement
        element.dataset.visible = 'true'
        revealObserver?.unobserve(element)
        revealElements.delete(element)
      })
    },
    { threshold: 0.12, rootMargin: '0px 0px 80px' },
  )

  return revealObserver
}

export function useTheme() {
  const [isDark, setIsDark] = useState(() => document.documentElement.classList.contains('dark'))

  useEffect(() => {
    document.documentElement.classList.toggle('dark', isDark)
    localStorage.setItem('theme', isDark ? 'dark' : 'light')
  }, [isDark])

  return { isDark, toggleTheme: () => setIsDark((value) => !value) }
}

export function useReveal<T extends HTMLElement>() {
  const ref = useRef<T>(null)

  useEffect(() => {
    const element = ref.current
    if (!element) return

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      element.dataset.visible = 'true'
      return
    }

    const observer = getRevealObserver()
    if (!observer) {
      element.dataset.visible = 'true'
      return
    }

    revealElements.add(element)
    observer.observe(element)
    return () => {
      observer.unobserve(element)
      revealElements.delete(element)
    }
  }, [])

  return ref
}
