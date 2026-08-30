import { emailAddress, socialLinks } from '../content'
import { SocialLink } from './SocialLink'

export function Footer() {
  return (
    <footer className="site-footer">
      <div className="footer-main">
        <div>
          <strong>Paul John Antigo</strong>
          <span>Curious about technology, open to different paths, &amp; always looking for ways to learn, improve, &amp; contribute.</span>
        </div>
        <div className="footer-links">
          <SocialLink label="GitHub" href={socialLinks.github} compact />
          <SocialLink label="LinkedIn" href={socialLinks.linkedin} compact />
          <SocialLink label="Instagram" href={socialLinks.instagram} compact />
          <SocialLink label={emailAddress} href={socialLinks.email} compact />
          <a href="#top">Back to top ↑</a>
        </div>
      </div>
      <div className="footer-meta"><span>© {new Date().getFullYear()}</span><span>Taltal, MAsinloc, Zambales, Philippines · PHT (UTC+8)</span></div>
    </footer>
  )
}
