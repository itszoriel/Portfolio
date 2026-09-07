import { ArrowLeft, ArrowUpRight, Check, Info } from 'lucide-react'
import { Link } from 'react-router-dom'
import { Architecture } from '../components/Architecture'
import { Footer } from '../components/Footer'
import { MunLinkPreview } from '../components/MunLinkPreview'
import { PageMetadata } from '../components/PageMetadata'
import { Reveal } from '../components/Reveal'
import { personName, projectUrl, siteUrl } from '../content'

const evolution = [
  ['Academic origin', 'MunLink started during my third year as a CSE 2 project with a three-person team.'],
  ['Continued as a personal project', 'After the course, I kept maintaining and expanding MunLink, refining existing workflows and adding features.'],
  ['Ongoing learning project', 'I continue refining existing functionality and experimenting with useful ideas as I learn.'],
] as const

const featureGroups = [
  {
    title: 'Resident experience',
    items: [
      'Account registration, authentication, and resident verification',
      'Document requests, generated PDFs, QR verification, and claim workflows',
      'Benefit-program applications and problem-report status tracking',
      'Barangay, municipal, and provincial announcements',
      'Buy, sell, donate, and lend marketplace workflows',
      'Notifications, profiles, and preference management',
    ],
  },
  {
    title: 'Administration',
    items: [
      'Resident verification and document processing',
      'Marketplace moderation and problem-report management',
      'Benefit-program and scoped announcement management',
      'Reporting and analytics views',
      'Barangay, municipal, provincial, and super-admin workflows',
      'Administrative account management and super-admin email 2FA',
    ],
  },
  {
    title: 'Privacy-oriented controls',
    items: [
      'JWT authentication and bcrypt password hashing',
      'Role, permission, and location-based authorization',
      'Rate limiting and audit logging',
      'Restricted access to resident ID and selfie images',
      'Watermarks that add accountability to sensitive-image viewing',
      'Configurable retention cleanup for stored files',
    ],
  },
] as const

const roleAreas = [
  'Resident frontend',
  'Administrative frontend',
  'Flask REST API',
  'Database design',
  'Authentication',
  'Role and permission controls',
  'UI implementation',
  'System integration',
  'Deployment',
  'Debugging and maintenance',
] as const

const stackGroups = [
  ['Frontend', ['React', 'TypeScript', 'Vite', 'Tailwind CSS']],
  ['Backend', ['Python', 'Flask', 'SQLAlchemy', 'REST APIs']],
  ['Database', ['PostgreSQL', 'Database migrations']],
  ['Authentication and security', ['JWT', 'bcrypt', 'Role and permission controls', 'Rate limiting']],
  ['Architecture and tooling', ['Turborepo', 'Git', 'GitHub']],
] as const

const challenges = [
  {
    title: 'API and CORS integration',
    text: 'Getting both frontends and the Flask API to communicate across local and deployed environments required work on allowed origins, authenticated requests, API configuration, environment-specific URLs, and request/response debugging. I investigated configuration differences and tested requests across both environments to work through integration issues.',
    lesson: 'This taught me a repeatable process for researching and debugging integration problems I did not already know how to solve.',
  },
  {
    title: 'Evolving the database design',
    text: 'As MunLink grew, I had to connect residents, locations, documents, programs, reports, announcements, marketplace activity, and administrative records. I refined relationships and migrations as new workflows exposed limitations in earlier decisions.',
    lesson: 'I learned to treat the data model as something that must evolve carefully with the application, rather than assuming the first structure will be final.',
  },
  {
    title: 'Authentication and permission boundaries',
    text: 'The system includes residents plus barangay, municipal, provincial, and super-admin roles, so access could not be reduced to logged in versus logged out. I worked through authentication, authorization, role permissions, and geographic scope checks for different actions and records.',
    lesson: 'This helped me understand why identity and permission checks must be considered throughout a workflow, not only at the login screen.',
  },
] as const

const testing = [
  'Manual functional testing',
  'Role-based access testing',
  'API request and response testing',
  'Browser and responsive testing',
  'Database checks and debugging',
  'End-to-end workflow testing',
] as const

const munlinkDescription = `${personName}'s civic-technology project using React, TypeScript, Python, Flask, and PostgreSQL, with resident and administrative workflows.`

const munlinkStructuredData = {
  '@context': 'https://schema.org',
  '@type': 'SoftwareSourceCode',
  name: 'MunLink',
  description: munlinkDescription,
  url: new URL('/work/munlink', siteUrl).href,
  sameAs: projectUrl,
  programmingLanguage: ['TypeScript', 'Python'],
  author: { '@id': `${siteUrl}#person` },
  isPartOf: { '@id': `${siteUrl}#website` },
  keywords: 'full-stack web development, civic technology, React, TypeScript, Flask, PostgreSQL',
} as const

export function MunLinkCaseStudy() {
  return (
    <>
      <PageMetadata
        title={`MunLink Full-Stack Case Study | ${personName}`}
        description={munlinkDescription}
        path="/work/munlink"
        image="/images/munlink-homepage.jpg"
        imageAlt="MunLink demo homepage showing its Zambales municipal-services interface"
        imageWidth={1881}
        imageHeight={946}
        type="article"
        structuredData={munlinkStructuredData}
      />
      <main id="main-content" className="case-study">
        <section className="case-hero" id="top">
          <Link className="back-link" to="/#projects"><ArrowLeft size={16} /> Back to selected work</Link>
          <div className="case-hero-grid">
            <Reveal>
              <span className="eyebrow">Full-stack civic-technology project</span>
              <h1>MunLink</h1>
              <p>An independent project exploring how common municipal services could be brought together in a digital platform.</p>
            </Reveal>
            <Reveal className="case-facts">
              <div><span>STATUS</span><strong>Active personal project</strong></div>
              <div><span>ROLE</span><strong>Developer / maintainer</strong></div>
              <div><span>SCOPE</span><strong>Zambales, Philippines</strong></div>
            </Reveal>
          </div>
          <Reveal className="case-context-note">
            <Info size={16} aria-hidden="true" />
            <p>Independent learning project. Not affiliated with or officially deployed by an LGU.</p>
          </Reveal>
          <Reveal className="case-preview"><MunLinkPreview /></Reveal>
        </section>

        <section className="case-section two-column-case">
          <Reveal className="case-index"><span>01</span><h2>Overview</h2></Reveal>
          <Reveal className="case-body large-case-copy">
            <p>MunLink began as a three-person CSE 2 academic project during my third year. I took responsibility for development while my teammates supported testing and debugging. After the course, I continued maintaining and expanding it as a personal project.</p>
            <p>The current user-facing application is scoped to Zambales. Region 3 location data remains in the project for possible future expansion, but expansion is not a confirmed deployment plan.</p>
          </Reveal>
        </section>

        <section className="case-section two-column-case">
          <Reveal className="case-index"><span>02</span><h2>Why I built it</h2></Reveal>
          <Reveal className="case-body">
            <p>MunLink originally started as a school requirement, but I decided to keep working on it after the course ended. It became a place where I could apply what I was learning to a larger system instead of only building small exercises.</p>
            <p>As it grew, I encountered problems involving APIs, databases, authentication, permissions, responsive interfaces, and deployment. Those problems pushed me to research and learn things I did not already know.</p>
          </Reveal>
        </section>

        <section className="case-section">
          <Reveal className="case-index"><span>03</span><h2>Project evolution</h2></Reveal>
          <div className="evolution-timeline">
            {evolution.map(([title, text], index) => (
              <Reveal className="evolution-stage" key={title}>
                <span>0{index + 1}</span><h3>{title}</h3><p>{text}</p>
              </Reveal>
            ))}
          </div>
        </section>

        <section className="case-section">
          <Reveal className="case-index"><span>04</span><h2>Main feature areas</h2></Reveal>
          <div className="core-feature-grid">
            {featureGroups.map((group, index) => (
              <Reveal className="core-feature" key={group.title}>
                <span>0{index + 1}</span><h3>{group.title}</h3>
                <ul className="feature-group-list">{group.items.map((item) => <li key={item}>{item}</li>)}</ul>
              </Reveal>
            ))}
          </div>
        </section>

        <section className="case-section two-column-case">
          <Reveal className="case-index"><span>05</span><h2>My role</h2></Reveal>
          <Reveal className="case-body">
            <p><strong>Developer and maintainer.</strong> I worked across the frontend, API, database, integrations, and deployment, with my original teammates contributing testing and debugging. My work includes implementing features, connecting application layers, resolving issues, and maintaining the project.</p>
            <h3>Development approach</h3>
            <p>I use AI tools, documentation, and community discussions, including Reddit, as supporting resources while making implementation decisions, adapting code, and testing behavior myself. This has given me practical experience with detailed prompting, task decomposition, context management, output validation, and token-conscious workflows.</p>
            <div className="role-matrix">
              {roleAreas.map((role) => <span key={role}><Check size={14} />{role}</span>)}
            </div>
          </Reveal>
        </section>

        <section className="case-section architecture-section">
          <Reveal className="case-index light"><span>06</span><h2>Architecture</h2></Reveal>
          <Reveal><p className="architecture-intro">The resident and administrative React applications use the same Flask REST API. SQLAlchemy maps the API&apos;s data models to PostgreSQL, and the repository keeps the applications and shared interface code together in a Turborepo monorepo.</p></Reveal>
          <Reveal><Architecture /></Reveal>
        </section>

        <section className="case-section">
          <Reveal className="case-index"><span>07</span><h2>Technology stack</h2></Reveal>
          <div className="stack-groups">
            {stackGroups.map(([label, technologies]) => (
              <Reveal className="stack-group" key={label}>
                <h3>{label}</h3>
                <div>{technologies.map((technology) => <code key={technology}>{technology}</code>)}</div>
              </Reveal>
            ))}
          </div>
        </section>

        <section className="case-section">
          <Reveal className="case-index"><span>08</span><h2>Challenges &amp; what I learned</h2></Reveal>
          <div className="challenge-list">
            {challenges.map((challenge, index) => (
              <Reveal className="challenge-item" key={challenge.title}>
                <span>0{index + 1}</span>
                <h3>{challenge.title}</h3>
                <div><p>{challenge.text}</p><p className="challenge-lesson">{challenge.lesson}</p></div>
              </Reveal>
            ))}
          </div>
        </section>

        <section className="case-section two-column-case testing-section">
          <Reveal className="case-index"><span>09</span><h2>Testing</h2></Reveal>
          <Reveal className="case-body">
            <p>I tested features manually across roles, browsers, API interactions, database records, responsive layouts, and complete workflows. During the original academic project, my two teammates also helped with testing and debugging, and we demonstrated MunLink to our professor and classmates.</p>
            <div className="testing-list">{testing.map((item) => <span key={item}><Check size={14} />{item}</span>)}</div>
          </Reveal>
        </section>

        <section className="case-section learning-section">
          <Reveal className="case-index"><span>10</span><h2>What I learned</h2></Reveal>
          <div className="learning-grid">
            <Reveal><p>The biggest value of MunLink has been the experience of maintaining a project as it became more complicated.</p></Reveal>
            <Reveal className="case-body">
              <p>I learned that adding a feature often affects the database, API, permissions, UI, and existing workflows at the same time. That taught me to trace changes across application layers, check existing behavior, and revisit earlier decisions as my understanding improved.</p>
            </Reveal>
          </div>
        </section>

        <section className="case-status">
          <Reveal className="case-index light"><span>11</span><h2>Current status</h2></Reveal>
          <Reveal className="status-summary">
            <div><span>CORE FEATURE SET</span><strong>Implemented</strong></div>
            <div><span>MAINTENANCE</span><strong>Ongoing</strong></div>
            <div><span>PUBLIC VERSION</span><strong>Portfolio demo</strong></div>
          </Reveal>
          <Reveal className="status-message">
            <Info size={23} aria-hidden="true" />
            <div>
              <p>The currently intended core feature set is implemented, but MunLink remains an active personal project. I continue to refine workflows, responsive behavior, testing, and earlier implementation decisions as I learn; there is no claimed production or government deployment roadmap.</p>
              <p className="status-disclaimer">Independent learning project. Not affiliated with, commissioned by, endorsed by, or officially deployed by an LGU.</p>
            </div>
          </Reveal>
          <Reveal className="case-status-actions">
            <a className="button light-button" href={projectUrl} target="_blank" rel="noreferrer">Open live demo <ArrowUpRight size={17} /></a>
          </Reveal>
        </section>
      </main>
      <Footer />
    </>
  )
}
