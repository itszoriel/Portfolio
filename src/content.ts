export const projectUrl = 'https://munlink-web-9s3r.onrender.com/'
export const resumeUrl = '/Paul-John-Antigo-Resume.pdf'
export const phResumeUrl = '/resumes/Paul-John-Antigo-PH-Resume.pdf'
export const emailAddress = 'Pauljohn.antigo@gmail.com'

export const socialLinks = {
  email: `mailto:${emailAddress}`,
  github: 'https://github.com/itszoriel',
  linkedin: 'https://www.linkedin.com/in/paul-john-antigo-708047364/',
  instagram: 'https://www.instagram.com/ptnagooo/',
} as const

export const navigation = [
  { number: '01', label: 'Projects', href: '/#projects' },
  { number: '02', label: 'Experience', href: '/#experience' },
  { number: '03', label: 'Skills', href: '/#skills' },
  { number: '04', label: 'Credentials', href: '/#credentials' },
  { number: '05', label: 'About', href: '/#about' },
  { number: '06', label: 'Contact', href: '/#contact' },
]

export const skillGroups = [
  { title: 'Frontend', items: ['React', 'TypeScript', 'JavaScript', 'HTML', 'CSS', 'Tailwind CSS', 'Vite'] },
  { title: 'Backend', items: ['Python', 'Flask', 'REST APIs', 'SQLAlchemy'] },
  { title: 'Database', items: ['PostgreSQL', 'SQL', 'Database Design'] },
  {
    title: 'Development / Engineering',
    items: ['Git', 'GitHub', 'Turborepo', 'Authentication', 'Authorization', 'JWT', 'Role-Based Access Control', 'API Integration'],
  },
]

export const exploring = [
  'Data Analytics',
  'User Experience Design',
  'Cybersecurity Fundamentals',
  'Artificial Intelligence Fundamentals',
]

export const credentials = [
  {
    title: 'Data Analytics Essentials',
    issuer: 'Cisco Networking Academy',
    date: 'August 29, 2026',
    type: 'Certificate of Course Completion',
    credentialUrl: '/credentials/data-analytics-essentials.pdf',
    description: 'Foundational training in the data analytics process, data preparation, analysis, and communicating insights.',
    topics: ['Excel', 'SQL', 'Tableau', 'Data preparation', 'Basic statistical analysis', 'Data visualization'],
  },
  {
    title: 'Azure AI Fundamentals',
    kicker: 'Microsoft Artificial Intelligence Course',
    issuer: 'TESDA',
    date: 'July 13, 2026',
    type: 'Certificate of Completion',
    credentialUrl: '/credentials/azure-ai-fundamentals.pdf',
  },
  {
    title: 'Security, Compliance, and Identity Fundamentals',
    kicker: 'Microsoft Cybersecurity Course',
    issuer: 'TESDA',
    date: 'July 14, 2026',
    type: 'Certificate of Completion',
    credentialUrl: '/credentials/security-compliance-identity-fundamentals.pdf',
  },
  {
    title: 'Developing Designs for User Experience',
    issuer: 'TESDA',
    date: 'July 15, 2026',
    type: 'Certificate of Completion',
    credentialUrl: '/credentials/developing-designs-for-user-experience.pdf',
  },
] as const
