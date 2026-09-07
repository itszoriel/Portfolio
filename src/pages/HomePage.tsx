import { ArrowDownRight, ArrowRight, ArrowUpRight, Check, MapPin } from 'lucide-react'
import { Link } from 'react-router-dom'
import { credentials, emailAddress, exploring, homeDescription, homeTitle, personName, projectUrl, skillGroups, socialLinks } from '../content'
import { Footer } from '../components/Footer'
import { PageMetadata } from '../components/PageMetadata'
import { Reveal } from '../components/Reveal'
import { ResumePicker } from '../components/ResumePicker'
import { SectionHeading } from '../components/SectionHeading'
import { SocialLink } from '../components/SocialLink'

const munlinkFeatures = [
  'Resident and administrative applications',
  'Zambales-scoped content and permissions',
  'Document, payment, and claim workflows',
  'PDF generation and QR verification',
  'Programs, announcements, and issue reports',
  'Marketplace and notification workflows',
  'Role and permission controls',
  'Audited sensitive-file access',
]

const projectStack = ['React', 'TypeScript', 'Vite', 'Tailwind CSS', 'Python', 'Flask', 'SQLAlchemy', 'PostgreSQL', 'JWT', 'Turborepo']

export function HomePage() {
  return (
    <>
      <PageMetadata
        title={homeTitle}
        description={homeDescription}
        path="/"
      />
      <main id="main-content">
        <section className="hero" id="top">
          <div className="hero-copy">
            <Reveal className="hero-kicker">
              <h1 className="hero-name">{personName}</h1><i /><span className="hero-location">Taltal, Masinloc, Zambales, PH</span>
            </Reveal>
            <Reveal className="hero-title-wrap">
              <p className="hero-statement">
                Learning, building,<br />
                <span>&amp; figuring things out.</span>
              </p>
            </Reveal>
            <Reveal className="hero-intro">
              <p className="hero-role">Computer Science Student<br /> Technology & Software</p>
              <div>
                <p>I enjoy learning how technology can be used to solve practical problems — whether through software, data, systems, or simply understanding how things work.</p>
                <p className="student-note">BS Computer Science at President Ramon Magsaysay State University, <br/> 2023–2027.</p>
              </div>
            </Reveal>
            <Reveal className="hero-actions">
              <a className="button primary-button" href="#projects">View my work <ArrowDownRight size={17} /></a>
              <ResumePicker />
            </Reveal>
            <Reveal className="hero-bottom">
              <div className="status"><i /><span>Currently learning, building, and open to opportunities.</span></div>
              <div className="hero-socials">
                <SocialLink label="GitHub" href={socialLinks.github} compact />
                <SocialLink label="LinkedIn" href={socialLinks.linkedin} compact />
                <SocialLink label="Instagram" href={socialLinks.instagram} compact />
              </div>
            </Reveal>
          </div>

          <Reveal className="portrait-column">
            <figure className="portrait">
              <img src="/images/paul-john-antigo.jpg" alt={`Portrait of ${personName}, Computer Science student`} width="960" height="958" decoding="async" fetchPriority="high" />
              <figcaption><span>Current Profile</span><span> / 2026</span></figcaption>
            </figure>
            <div className="location-note"><MapPin size={14} /><span>Based in Philippines</span></div>
          </Reveal>
        </section>

        <section className="section project-section" id="projects">
          <Reveal><SectionHeading number="01" title="Selected Work" description="A collection of work and experiences that reflect my curiosity, learning, and growth." /></Reveal>
          <Reveal className="project-heading-row">
            <div>
              <span className="eyebrow">Academic origin / Personal project</span>
              <h3>MunLink</h3>
            </div>
            <span className="project-year">ACTIVE PERSONAL PROJECT</span>
          </Reveal>

          <div className="project-detail-grid">
            <Reveal className="project-story">
              <p className="project-lede">An independent civic-technology project exploring how common municipal services could be brought together in a digital platform.</p>
              <p>MunLink began as a three-person CSE 2 project during my third year. I took responsibility for development while my teammates supported testing and debugging. After the course, I continued maintaining and expanding it as a personal project.</p>
              <div className="project-actions">
                <a className="button primary-button" href={projectUrl} target="_blank" rel="noreferrer">Open demo <ArrowUpRight size={17} /></a>
                <Link className="button text-button" to="/work/munlink">Case study <ArrowRight size={17} /></Link>
              </div>
            </Reveal>
            <Reveal className="feature-list">
              {munlinkFeatures.map((feature) => <div key={feature}><Check size={14} /><span>{feature}</span></div>)}
            </Reveal>
          </div>

          <Reveal className="stack-row">
            <span>BUILT WITH</span>
            <div>{projectStack.map((technology) => <code key={technology}>{technology}</code>)}</div>
          </Reveal>

          <Reveal className="disclaimer">
            <span>Project context</span>
            <p>The current demo is scoped to Zambales, with Region 3 location data retained only for possible future expansion. MunLink is an independent learning project, not an official government service or an LGU deployment.</p>
          </Reveal>
        </section>

        <section className="section experience-section" id="experience">
          <Reveal><SectionHeading number="02" title="Experience" description="Early workplace experience in technical support and careful data handling." /></Reveal>
          <Reveal className="experience-item">
            <div className="experience-date"><span>JUNE 4-JULY 31, 2025<br />20 DAYS</span><b>SPES</b></div>
            <div className="experience-content">
              <span className="eyebrow">Special Program for Employment of Students (DOLE)</span>
              <h3>IT Support Assistant <span>— Cisco Department</span></h3>
              <p className="experience-place">NZC Cisco Department · Northern Zambales College, Inc.<br />Masinloc, Zambales, Philippines</p>
              <p>Selected under the Special Program for Employment of Students (SPES) and assigned to the Cisco Department of Northern Zambales College, Inc., supporting the production and processing of official student identification cards.</p>
              <div className="responsibility-grid">
                <span>Encoded and validated student information for accurate ID processing</span>
                <span>Captured and prepared student photographs for identification card production</span>
                <span>Organized student records and checked information consistency before printing</span>
                <span>Assisted with the end-to-end ID production workflow, from data preparation to final output</span>
                <span>Performed quality checks on completed identification cards</span>
                <span>Assisted with the organized release and distribution of finished student IDs</span>
              </div>
              <div className="experience-takeaways">
                {['Accuracy', 'Responsibility', 'Data handling', 'Technical support', 'Communication', 'Organization'].map((item) => <code key={item}>{item}</code>)}
              </div>
            </div>
          </Reveal>
        </section>

        <section className="section skills-section" id="skills">
          <Reveal><SectionHeading number="03" title="What I Work With" description="Tools used in projects, separated from areas I am still exploring." /></Reveal>
          <div className="skill-intro-grid">
            <Reveal><p className="large-copy">I build practical experience by developing features, connecting systems, and testing real workflows. Each project helps me deepen my understanding of the technologies I use.</p></Reveal>
            <Reveal className="skill-legend"><i /><span>Practical project experience</span></Reveal>
          </div>
          <div className="skill-grid">
            {skillGroups.map((group, index) => (
              <Reveal className="skill-group" key={group.title}>
                <div className="skill-group-heading"><span>0{index + 1}</span><h3>{group.title}</h3></div>
                <div className="skill-tags">{group.items.map((item) => <span key={item}>{item}</span>)}</div>
              </Reveal>
            ))}
          </div>
          <Reveal className="exploring-row">
            <div><span className="eyebrow">Currently learning / exploring</span><p>Adjacent disciplines that help me build with more context.</p></div>
            <div>{exploring.map((item) => <span key={item}>{item}</span>)}</div>
          </Reveal>
        </section>

        <section className="section credentials-section" id="credentials">
          <Reveal><SectionHeading number="04" title="Credentials & Learning" description="Foundational coursework that broadens my engineering perspective." /></Reveal>
          <div className="credential-list">
            {credentials.map((credential, index) => (
              <Reveal className={`credential-card ${index === 0 ? 'featured' : ''}`} key={credential.title}>
                <div className="credential-number">0{index + 1}</div>
                <div className="credential-main">
                  {'kicker' in credential && credential.kicker && <span className="eyebrow">{credential.kicker}</span>}
                  <h3>{credential.title}</h3>
                  <p>{credential.issuer}</p>
                  {'description' in credential && credential.description && <p className="credential-description">{credential.description}</p>}
                  {'topics' in credential && credential.topics && <div className="credential-topics">{credential.topics.map((topic) => <code key={topic}>{topic}</code>)}</div>}
                </div>
                <div className="credential-meta">
                  <span>{credential.date}</span>
                  <span>{credential.type}</span>
                  <a className="credential-link" href={credential.credentialUrl} target="_blank" rel="noreferrer">
                    View credential <ArrowUpRight size={13} aria-hidden="true" />
                  </a>
                </div>
              </Reveal>
            ))}
          </div>
          <Reveal className="credential-note"><span>Note</span><p>The TESDA Microsoft courses listed here are course completion certificates, not Microsoft professional certifications.</p></Reveal>
        </section>

        <section className="section about-section" id="about">
          <Reveal><SectionHeading number="05" title="A little about me" /></Reveal>
          <div className="about-layout">
            <Reveal className="about-lede"><p>I like figuring things out, trying ideas, and learning from the process of making them work.</p></Reveal>
            <Reveal className="about-copy">
              <p>I&apos;m Paul John E. Antigo.</p>
              <p>I learn best through hands-on experience. Projects, coursework, and real-world opportunities have allowed me to explore different areas of technology—from software and databases to data, user experience, security, and emerging technologies.</p>
              <p>I’m still early in my journey, so I try to stay open-minded about where my interests may lead. What matters most to me right now is building strong fundamentals, learning from experience, and becoming more confident in solving unfamiliar problems.</p>
              <p>I don’t expect to have everything figured out yet. I’m simply focused on staying curious, improving over time, and finding opportunities where I can contribute while continuing to learn.</p>
            </Reveal>
          </div>
          <Reveal className="now-panel">
            <div><span className="live-dot" /><h3>Right now</h3></div>
            <ul>
              <li>Completing my BS Computer Science degree at PRMSU</li>
              <li>Strengthening my technical and problem-solving fundamentals</li>
              <li>Studying for AWS Certified AI Practitioner</li>
              <li>Planning to pursue AWS Certified Generative AI Developer - Professional next, followed by AWS Certified DevOps Engineer - Professional</li>
              <li>Developing personal projects and strengthening my skills through hands-on implementation and testing</li>
              <li>Exploring software, data analytics, cybersecurity, AI, and UX</li>
              <li>Looking for opportunities to learn, contribute, and gain real-world experience</li>
            </ul>
          </Reveal>
        </section>

        <section className="contact-section" id="contact">
          <Reveal className="contact-top"><h2 className="contact-label">06 / CONTACT</h2><span>OPEN TO OPPORTUNITIES</span></Reveal>
          <Reveal><p className="contact-heading">Let’s build<br /><em>something.</em></p></Reveal>
          <div className="contact-grid">
            <Reveal><p>I’m open to internships, entry-level opportunities, collaborations, and projects where I can contribute, learn from experienced developers, and continue growing as a software engineer.</p></Reveal>
            <Reveal className="contact-links">
              <SocialLink label={emailAddress} href={socialLinks.email} />
              <SocialLink label="LinkedIn" href={socialLinks.linkedin} />
              <SocialLink label="GitHub" href={socialLinks.github} />
              <SocialLink label="Instagram" href={socialLinks.instagram} />
            </Reveal>
          </div>
        </section>
      </main>
      <Footer />
    </>
  )
}
