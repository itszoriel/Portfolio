import profile from './data/profile.json'

export { profile }
export const siteUrl = profile.portfolio
export const personName = profile.name
export const homeTitle = `${personName} | Computer Science Student & Portfolio`
export const homeDescription = `Portfolio of ${personName}, a Computer Science student exploring software development, cybersecurity, data, cloud, and AI.`

export const projectUrl = profile.project.demo
export const resumeUrl = '/resumes/Paul-John-Antigo-ATS-Resume.pdf'
export const phResumeUrl = '/resumes/Paul-John-Antigo-PH-Resume.pdf'
export const cvUrl = '/resumes/Paul-John-Antigo-CV.pdf'
export const emailAddress = profile.email
export const phoneNumber = profile.phone

export const socialLinks = {
  email: `mailto:${emailAddress}`,
  phone: profile.phoneHref,
  github: profile.github,
  linkedin: profile.linkedin,
  instagram: profile.instagram,
} as const

export const navigation = [
  { number: '01', label: 'Credentials', href: '/#credentials' },
  { number: '02', label: 'Experience', href: '/#experience' },
  { number: '03', label: 'Skills', href: '/#skills' },
  { number: '04', label: 'Projects', href: '/#projects' },
  { number: '05', label: 'About', href: '/#about' },
  { number: '06', label: 'Contact', href: '/#contact' },
]

export const skillGroups = profile.skillGroups

export const exploring = [
  'Data Analytics',
  'User Experience Design',
  'Cybersecurity Fundamentals',
  'Artificial Intelligence Fundamentals',
]

export const credentials = profile.credentials
