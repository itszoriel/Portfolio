import { useEffect } from 'react'
import { personName, siteUrl } from '../content'

const siteName = `${personName} Portfolio`

type PageMetadataProps = {
  title: string
  description: string
  path: string
  image?: string
  imageAlt?: string
  imageWidth?: number
  imageHeight?: number
  type?: 'website' | 'article'
  structuredData?: Record<string, unknown>
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
  imageAlt = `Portrait of ${personName}`,
  imageWidth = 960,
  imageHeight = 958,
  type = 'website',
  structuredData,
}: PageMetadataProps) {
  useEffect(() => {
    const canonical = new URL(path, siteUrl)
    canonical.hash = ''
    const canonicalUrl = canonical.href
    const imageUrl = new URL(image, siteUrl).href
    const twitterCard = imageWidth / imageHeight >= 1.5 ? 'summary_large_image' : 'summary'

    document.title = title

    let canonicalLink = document.head.querySelector<HTMLLinkElement>('link[rel="canonical"]')
    if (!canonicalLink) {
      canonicalLink = document.createElement('link')
      canonicalLink.rel = 'canonical'
      document.head.appendChild(canonicalLink)
    }
    canonicalLink.href = canonicalUrl

    setMeta('name', 'description', description)
    setMeta('name', 'author', personName)
    setMeta('name', 'robots', 'index, follow, max-image-preview:large')
    setMeta('name', 'googlebot', 'index, follow, max-image-preview:large')
    setMeta('property', 'og:type', type)
    setMeta('property', 'og:url', canonicalUrl)
    setMeta('property', 'og:site_name', siteName)
    setMeta('property', 'og:locale', 'en_PH')
    setMeta('property', 'og:title', title)
    setMeta('property', 'og:description', description)
    setMeta('property', 'og:image', imageUrl)
    setMeta('property', 'og:image:secure_url', imageUrl)
    setMeta('property', 'og:image:type', 'image/jpeg')
    setMeta('property', 'og:image:width', String(imageWidth))
    setMeta('property', 'og:image:height', String(imageHeight))
    setMeta('property', 'og:image:alt', imageAlt)
    setMeta('name', 'twitter:card', twitterCard)
    setMeta('name', 'twitter:title', title)
    setMeta('name', 'twitter:description', description)
    setMeta('name', 'twitter:image', imageUrl)
    setMeta('name', 'twitter:image:alt', imageAlt)

    let schema = document.head.querySelector<HTMLScriptElement>('script[data-page-schema="true"]')
    if (structuredData) {
      if (!schema) {
        schema = document.createElement('script')
        schema.type = 'application/ld+json'
        schema.dataset.pageSchema = 'true'
        document.head.appendChild(schema)
      }
      schema.textContent = JSON.stringify(structuredData)
    } else {
      schema?.remove()
    }

    return () => schema?.remove()
  }, [description, image, imageAlt, imageHeight, imageWidth, path, structuredData, title, type])

  return null
}
