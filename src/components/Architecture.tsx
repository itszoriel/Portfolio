import { Braces, Database, LayoutDashboard, Server, UsersRound } from 'lucide-react'

const clients = [
  { label: 'Resident web app', meta: 'React + TypeScript', icon: UsersRound },
  { label: 'Administrative app', meta: 'React + TypeScript', icon: LayoutDashboard },
] as const

function ArchitectureNode({ label, meta, icon: Icon }: { label: string; meta: string; icon: typeof Braces }) {
  return (
    <div className="architecture-node">
      <Icon size={20} aria-hidden="true" />
      <div><small>{meta}</small><strong>{label}</strong></div>
    </div>
  )
}

export function Architecture() {
  return (
    <div className="architecture" aria-label="MunLink application architecture">
      <div className="architecture-flow">
        <div className="architecture-clients">
          {clients.map((client) => <ArchitectureNode key={client.label} {...client} />)}
        </div>
        <div className="architecture-connector" aria-hidden="true"><i /></div>
        <ArchitectureNode label="Shared Flask REST API" meta="Python + SQLAlchemy" icon={Server} />
        <div className="architecture-connector" aria-hidden="true"><i /></div>
        <ArchitectureNode label="PostgreSQL" meta="Relational database" icon={Database} />
      </div>
      <div className="architecture-repo">
        <Braces size={17} aria-hidden="true" />
        <p><strong>Turborepo monorepo</strong><span>Resident application, administrative application, Flask API, and shared UI components.</span></p>
      </div>
    </div>
  )
}
