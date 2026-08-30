import { ShieldCheck } from 'lucide-react'

export function MunLinkPreview() {
  return (
    <div className="browser-frame" aria-label="MunLink public homepage screenshot">
      <div className="browser-bar">
        <div className="browser-dots"><i /><i /><i /></div>
        <span>munlink-web-9s3r.onrender.com</span>
        <ShieldCheck size={15} />
      </div>
      <img
        className="munlink-screenshot"
        src="/images/munlink-homepage.jpg"
        alt="MunLink public homepage showing the Lalawigan ng Zambales hero"
        width="1881"
        height="946"
        loading="lazy"
        decoding="async"
        fetchPriority="low"
      />
      <div className="mockup-note">Authentic project capture · public homepage</div>
    </div>
  )
}
