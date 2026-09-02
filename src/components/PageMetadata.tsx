import { useEffect } from 'react'

const siteUrl = 'https://paul-antigo.vercel.app'

type PageMetadataProps = {
  title: string
  description: string
  path: string
  image?: string
  imageAlt?: string
  imageWidth?: number
  imageHeight?: number
  type?: 'website' | 'article'
}

function setMeta(attribute: 'name' | 'property', key: string, content: string) {
  let element = document.head.querySelector<HTMLMetaElement>(`meta[${attribute}="${key}"]`)

  if (!element) {
    element = document.createElement('meta')
    element.setAttribute(attribute, key)
    document.head.appendChild(element)
  }

  element.content = content
}

export function PageMetadata({
  title,
  description,
  path,
  image = '/images/paul-john-antigo.jpg',
  imageAlt = 'Portrait of Paul John Antigo',
  imageWidth = 960,
  imageHeight = 960,
  type = 'website',
}: PageMetadataProps) {
  useEffect(() => {
    const canonicalUrl = new URL(path, siteUrl).href
    const imageUrl = new URL(image, siteUrl).href
    const twitterCard = imageWidth / imageHeight >= 1.5 ? 'summary_large_image' : 'summary'

    document.title = title

    let canonical = document.head.querySelector<HTMLLinkElement>('link[rel="canonical"]')
    if (!canonical) {
      canonical = document.createElement('link')
      canonical.rel = 'canonical'
      document.head.appendChild(canonical)
    }
    canonical.href = canonicalUrl

    setMeta('name', 'description', description)
    setMeta('name', 'robots', 'index, follow, max-image-preview:large')
    setMeta('name', 'googlebot', 'index, follow, max-image-preview:large')
    setMeta('property', 'og:type', type)
    setMeta('property', 'og:url', canonicalUrl)
    setMeta('property', 'og:title', title)
    setMeta('property', 'og:description', description)
    setMeta('property', 'og:image', imageUrl)
    setMeta('property', 'og:image:secure_url', imageUrl)
    setMeta('property', 'og:image:width', String(imageWidth))
    setMeta('property', 'og:image:height', String(imageHeight))
    setMeta('property', 'og:image:alt', imageAlt)
    setMeta('name', 'twitter:card', twitterCard)
    setMeta('name', 'twitter:title', title)
    setMeta('name', 'twitter:description', description)
    setMeta('name', 'twitter:image', imageUrl)
    setMeta('name', 'twitter:image:alt', imageAlt)
  }, [description, image, imageAlt, imageHeight, imageWidth, path, title, type])

  return null
}
