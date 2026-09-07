import { ShieldCheck } from 'lucide-react'

export function MunLinkPreview() {
  return (
    <div className="browser-frame" aria-label="Screenshot preview of the MunLink demo">
      <div className="browser-bar">
        <div className="browser-dots"><i /><i /><i /></div>
        <span>munlink-web-9s3r.onrender.com</span>
        <ShieldCheck size={15} />
      </div>
      <img
        className="munlink-screenshot"
        src="/images/munlink-homepage.jpg"
        alt="MunLink demo homepage showing its Zambales municipal-services interface"
        width="1881"
        height="946"
        loading="lazy"
        decoding="async"
        fetchPriority="low"
      />
      <div className="mockup-note">Project screenshot - public demo homepage</div>
    </div>
  )
}
