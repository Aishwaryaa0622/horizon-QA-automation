"""
recommendations.py
------------------
Lighthouse tells you WHAT is slow. This module explains WHY it matters and
HOW to fix it, in plain English.

`FIXES` maps a Lighthouse audit id (the stable string Google uses, e.g.
"uses-optimized-images") to a short recommendation. Anything we do not have a
custom text for falls back to the audit's own description.
"""

# Audit id -> beginner friendly fix advice.
FIXES = {
    "render-blocking-resources": (
        "Some CSS/JS files load before the page can be drawn. Inline the small "
        "critical CSS and add `defer` or `async` to non-essential scripts."
    ),
    "uses-optimized-images": (
        "Images are heavier than they need to be. Compress them (TinyPNG, "
        "Squoosh) or serve them through an image CDN."
    ),
    "modern-image-formats": (
        "Serve images as WebP or AVIF instead of JPEG/PNG - usually 25-50% smaller."
    ),
    "uses-responsive-images": (
        "Large images are being shrunk by the browser. Ship correctly sized "
        "images using `srcset` / `sizes`."
    ),
    "offscreen-images": (
        "Images below the fold load immediately. Add `loading=\"lazy\"` to them."
    ),
    "unused-css-rules": (
        "A lot of CSS is never used on this page. Remove dead styles or split "
        "CSS per page (PurgeCSS / Tailwind's built-in purge)."
    ),
    "unused-javascript": (
        "Unused JavaScript is downloaded and parsed. Use code splitting and "
        "load heavy libraries only where they are needed."
    ),
    "unminified-css": "Minify CSS during your build step.",
    "unminified-javascript": "Minify JavaScript during your build step.",
    "uses-text-compression": (
        "Enable gzip or Brotli compression on the server for text responses."
    ),
    "uses-long-cache-ttl": (
        "Static files expire too soon. Set long `Cache-Control` max-age values "
        "and use hashed file names."
    ),
    "server-response-time": (
        "The server takes too long for the first byte. Add caching, optimise "
        "database queries, or move to a faster host/CDN."
    ),
    "total-byte-weight": (
        "The page is very heavy overall. Trim images, fonts and third-party scripts."
    ),
    "dom-size": (
        "The page has too many HTML elements. Simplify the markup or paginate "
        "long lists."
    ),
    "font-display": (
        "Text is invisible while fonts load. Add `font-display: swap` to your "
        "@font-face rules."
    ),
    "largest-contentful-paint-element": (
        "Make the main hero image or heading load first: preload it and avoid "
        "lazy-loading it."
    ),
    "layout-shift-elements": (
        "Content jumps around while loading. Set width/height (or aspect-ratio) "
        "on images, ads and embeds."
    ),
    "third-party-summary": (
        "Third-party scripts (analytics, chat, ads) cost a lot of time. Remove "
        "the ones you do not need and load the rest after the page is ready."
    ),
    "redirects": "Remove redirect chains - each hop adds a full round trip.",
    "bootup-time": (
        "JavaScript execution is expensive. Split bundles and defer heavy work."
    ),
    "mainthread-work-breakdown": (
        "The main thread is busy for too long. Reduce script work and long tasks."
    ),
    "image-alt": "Add descriptive `alt` text to every meaningful image.",
    "color-contrast": (
        "Text contrast is too low. Aim for a contrast ratio of at least 4.5:1."
    ),
    "meta-description": "Add a unique meta description tag (under 160 characters).",
    "document-title": "Add a clear, unique <title> to the page.",
    "is-crawlable": "Remove the noindex/robots rules blocking search engines.",
    "uses-https": "Serve the whole site over HTTPS.",
    "errors-in-console": "Fix the JavaScript errors logged in the browser console.",
}


def get_fix(audit_id: str, fallback: str = "") -> str:
    """
    Return the recommended fix for a Lighthouse audit.

    Falls back to Lighthouse's own description when we have no custom text.
    """
    return FIXES.get(audit_id) or fallback or "Review this audit in the Lighthouse docs."
