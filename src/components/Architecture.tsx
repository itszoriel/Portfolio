import { BellRing, Braces, Cloud, CreditCard, Database, FileCheck2, KeyRound, Server, ShieldCheck } from 'lucide-react'

const nodes = [
  { label: 'Resident + admin React clients', meta: 'Interfaces', icon: Braces },
  { label: 'Flask REST API', meta: 'Service layer', icon: Server },
  { label: 'SQLAlchemy', meta: 'Data layer', icon: Database },
  { label: 'PostgreSQL', meta: 'Database', icon: Database },
]

export function Architecture() {
  return (
    <div className="architecture" aria-label="MunLink technical architecture">
      <div className="architecture-flow">
        {nodes.map(({ label, meta, icon: Icon }, index) => (
          <div className="architecture-step" key={label}>
            <div className="architecture-node">
              <Icon size={20} aria-hidden="true" />
              <div><small>{meta}</small><strong>{label}</strong></div>
              <span>0{index + 1}</span>
            </div>
            {index < nodes.length - 1 && <div className="architecture-connector" aria-hidden="true"><i /></div>}
          </div>
        ))}
      </div>
      <div className="support-services">
        <span><KeyRound size={15} /> JWT + refresh tokens</span>
        <span><ShieldCheck size={15} /> Role + location scope</span>
        <span><Cloud size={15} /> Supabase file storage</span>
        <span><FileCheck2 size={15} /> PDF + QR generation</span>
        <span><BellRing size={15} /> Email + SMS outbox</span>
        <span><CreditCard size={15} /> Stripe + manual payments</span>
      </div>
    </div>
  )
}
