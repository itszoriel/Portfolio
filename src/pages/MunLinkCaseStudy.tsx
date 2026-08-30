import { ArrowLeft, ArrowUpRight, Check, CircleAlert } from 'lucide-react'
import { Link } from 'react-router-dom'
import { Architecture } from '../components/Architecture'
import { Footer } from '../components/Footer'
import { MunLinkPreview } from '../components/MunLinkPreview'
import { Reveal } from '../components/Reveal'
import { projectUrl } from '../content'

const challenges = [
  ['Location-scoped authorization', 'Keeping resident, staff, and administrator access aligned with province, municipality, barangay, role, and permission boundaries.'],
  ['Workflow state and rules', 'Making submissions, reviews, payments, approvals, fulfillment, and notifications follow valid transitions and prerequisites.'],
  ['Shared API contracts', 'Maintaining consistent behavior while two separate React applications consume the same Flask API.'],
  ['Sensitive document handling', 'Restricting access to resident IDs and selfies while recording when authorized staff view protected files.'],
  ['Reliable notifications', 'Queueing email and SMS events so delivery work stays separate from the user-facing request lifecycle.'],
  ['Cross-domain data modeling', 'Connecting users, locations, documents, benefits, reports, listings, transactions, notifications, and audit records coherently.'],
] as const

const learnings = [
  'Multi-application monorepo architecture',
  'REST API contracts across two clients',
  'Role, permission, and location-scoped authorization',
  'Access and refresh token lifecycles',
  'Workflow and state modeling',
  'Relational schemas and database migrations',
  'PDF and QR document generation',
  'Payment and fulfillment prerequisites',
  'Notification outbox and retry behavior',
  'Privacy-aware file access and audit logging',
]

const features = [
  ['Documents and fulfillment', 'Residents can submit requests while staff handle review, fees or exemptions, payment, and digital or pickup release. Generated documents can include QR verification and claim tickets.'],
  ['Scoped information', 'Announcements and other public information can be targeted by province, municipality, or barangay instead of being shown to every account.'],
  ['Resident verification', 'Email verification and ID or selfie review support resident onboarding, with permission-gated and audited access to sensitive identity files.'],
  ['Benefits and issue reporting', 'Residents can apply for benefit programs with supporting documents and report municipal problems that staff can review and update.'],
  ['Marketplace workflows', 'Buy, sell, donate, and lend listings move through transaction states, participant actions, moderation, notifications, and audit history.'],
  ['Administrative operations', 'Municipal, barangay, provincial, and superadmin views support permissions, service processing, moderation, reports, and oversight.'],
] as const

export function MunLinkCaseStudy() {
  return (
    <>
      <main id="main-content" className="case-study">
        <section className="case-hero" id="top">
          <Link className="back-link" to="/#projects"><ArrowLeft size={16} /> Back to selected work</Link>
          <div className="case-hero-grid">
            <Reveal>
              <span className="eyebrow">Independent full-stack civic-tech system</span>
              <h1>MunLink</h1>
              <p>A Zambales-scoped service platform connecting residents, staff, and administrators across document processing, community services, and operational workflows.</p>
            </Reveal>
            <Reveal className="case-facts">
              <div><span>ROLE</span><strong>Independent developer</strong></div>
              <div><span>SYSTEM</span><strong>Resident web + admin portal + REST API</strong></div>
              <div><span>SCOPE</span><strong>Zambales portfolio deployment</strong></div>
            </Reveal>
          </div>
          <Reveal className="case-preview"><MunLinkPreview /></Reveal>
        </section>

        <section className="case-section two-column-case">
          <Reveal className="case-index"><span>01</span><h2>Overview</h2></Reveal>
          <Reveal className="case-body large-case-copy">
            <p>MunLink is a multi-application civic-tech project that models how residents and local government staff could move through common service workflows in one connected system.</p>
            <p>Separate React applications for residents and administrators communicate with a shared Flask REST API backed by PostgreSQL. The public-facing scope is Zambales, with province, municipality, and barangay boundaries represented throughout the data and access model.</p>
          </Reveal>
        </section>

        <section className="case-section two-column-case">
          <Reveal className="case-index"><span>02</span><h2>Why I built it</h2></Reveal>
          <Reveal className="case-body">
            <p>I wanted practical experience modeling an application where a feature is more than a screen. A document request, for example, has rules, roles, states, records, notifications, and fulfillment steps that must agree across the system.</p>
            <p>MunLink became a way to learn how a larger full-stack product is structured and how real-world processes can be translated into understandable software. It was built as an independent learning project, not as an official government product.</p>
          </Reveal>
        </section>

        <section className="case-section two-column-case">
          <Reveal className="case-index"><span>03</span><h2>My role</h2></Reveal>
          <Reveal className="case-body">
            <p>I designed and developed the system independently across its product, application, data, and deployment layers.</p>
            <div className="role-matrix">
              {['Systems design', 'Resident frontend', 'Admin frontend', 'REST API', 'Data modeling', 'Authentication', 'Authorization and scoping', 'Document generation', 'Integrations', 'Deployment'].map((role) => <span key={role}><Check size={14} />{role}</span>)}
            </div>
          </Reveal>
        </section>

        <section className="case-section">
          <Reveal className="case-index"><span>04</span><h2>Core features</h2></Reveal>
          <div className="core-feature-grid">
            {features.map(([title, text], index) => <Reveal className="core-feature" key={title}><span>0{index + 1}</span><h3>{title}</h3><p>{text}</p></Reveal>)}
          </div>
        </section>

        <section className="case-section architecture-section">
          <Reveal className="case-index light"><span>05</span><h2>Technical architecture</h2></Reveal>
          <Reveal><p className="architecture-intro">The Turborepo contains separate resident and admin React clients, a shared interface package, and a Flask API. SQLAlchemy maps application data to PostgreSQL, while supporting services handle identity, files, documents, payments, and notifications.</p></Reveal>
          <Reveal><Architecture /></Reveal>
        </section>

        <section className="case-section">
          <Reveal className="case-index"><span>06</span><h2>Engineering challenges</h2></Reveal>
          <div className="challenge-list">
            {challenges.map(([title, text], index) => <Reveal className="challenge-item" key={title}><span>0{index + 1}</span><h3>{title}</h3><p>{text}</p></Reveal>)}
          </div>
        </section>

        <section className="case-section learning-section">
          <Reveal className="case-index"><span>07</span><h2>What I learned</h2></Reveal>
          <div className="learning-grid">
            <Reveal><p>Building MunLink pushed me to think about software as a system of connected decisions, not a collection of isolated screens. I had to consider who can perform an action, what must already be true, what changes afterward, and how that change is recorded.</p></Reveal>
            <Reveal className="learning-list">{learnings.map((learning) => <span key={learning}>{learning}</span>)}</Reveal>
          </div>
        </section>

        <section className="case-status">
          <Reveal className="case-index light"><span>08</span><h2>Current status</h2></Reveal>
          <Reveal className="status-message">
            <CircleAlert size={23} />
            <p>MunLink is actively developed and publicly deployed as a portfolio and learning system. The public deployment is a demo; it is not an official government service and is not operated, commissioned, or endorsed by an LGU.</p>
          </Reveal>
          <Reveal className="case-status-actions">
            <a className="button light-button" href={projectUrl} target="_blank" rel="noreferrer">View live project <ArrowUpRight size={17} /></a>
          </Reveal>
        </section>
      </main>
      <Footer />
    </>
  )
}
