import type { HTMLAttributes, ReactNode } from 'react'
import { useReveal } from '../hooks'

type RevealProps = HTMLAttributes<HTMLDivElement> & {
  children: ReactNode
}

export function Reveal({ children, className = '', ...props }: RevealProps) {
  const ref = useReveal<HTMLDivElement>()
  return (
    <div ref={ref} className={`reveal ${className}`} {...props}>
      {children}
    </div>
  )
}
