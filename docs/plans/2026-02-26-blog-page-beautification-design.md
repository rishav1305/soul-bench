# Blog Page Beautification Design

**Date:** 2026-02-26
**Status:** Approved
**Scope:** Global font change (Ubuntu) + Blog listing page redesign + Blog detail page improvements

## Context

The current blog page at rishavchatterjee.com/blog is visually basic — plain white background, bordered card layout, no featured post treatment, broken Medium thumbnails, and a stark contrast with the premium dark navy homepage. The goal is to bring the blog page up to the quality level of top tech blogs (Stripe, Vercel, Medium) while maintaining the site's existing brand identity.

## Design Decisions

| Decision | Choice |
|----------|--------|
| Blog theme | Dark navy hero header + white content area |
| Card layout | Magazine two-column (featured 2/3 + sidebar 1/3) then 3-col grid |
| Content organization | Unified feed — local + Medium posts mixed, sorted by date |
| Font change | Ubuntu for body/content text site-wide; Geist Sans stays for headings |
| Card style | Borderless, subtle hover lift + shadow, clean typography |

## 1. Global Font Change — Ubuntu

- Add `Ubuntu` from Google Fonts via `next/font/google` in `layout.tsx`
- Weights: 400 (regular body), 500 (medium for emphasis), 700 (bold for strong)
- Set as CSS variable `--font-ubuntu` on `<body>`
- Update `globals.css` body font-family to use Ubuntu
- Geist Sans remains for headings (h1-h6), navigation, and UI elements
- Decorative fonts (Braggadocio, etc.) remain untouched

**Files to modify:**
- `src/app/layout.tsx` — import Ubuntu font
- `src/app/globals.css` — update body font-family

## 2. Blog Page Hero Header

Dark navy hero section matching the homepage:

- Background: `#0a2540` (or match homepage's exact dark navy)
- Height: ~200-250px
- "Blog" title: large Geist Sans bold, white text
- Subtitle: "Research, articles, and technical deep-dives" in muted blue-gray (`#8b9eb0`)
- Blue accent underline below title (existing brand pattern, `bg-blue-500`)
- Breadcrumb: light/white text on dark background
- Smooth transition to white content area below

## 3. Blog Listing — Magazine Layout

### Featured Post (Hero Card)
- Takes ~65% width on desktop (left side)
- Dark gradient background (navy to blue: `#0a2540` → `#1e3a5f`)
- White text: large title (Geist Sans bold, ~28px), excerpt (Ubuntu, ~16px)
- "Featured" badge (blue pill)
- Category pill, date, reading time
- Arrow link to article
- Medium badge if post is from Medium

### Sidebar (Right, ~35% width)
- 2-3 recent posts stacked vertically
- Compact cards: category pill, title, short excerpt, date
- White background, subtle bottom border separating each
- Hover: slight background tint

### Grid Section (Below Magazine Section)
- 3-column grid on desktop, 2-column on tablet, 1-column on mobile
- All remaining posts (after featured + sidebar)

### Card Design
- White background, no heavy borders
- Subtle `border-gray-100` or borderless
- Generous padding (24px)
- Category pill at top (blue-100 bg, blue-700 text, rounded-full)
- Title: Geist Sans bold, `#1a1a1a`, 18-20px
- Excerpt: Ubuntu, `#6b7280`, 14-15px, 2-line clamp
- Footer: date (left) and reading time (right), muted gray, separated by dot
- Hover: `translateY(-2px)` lift + shadow deepening transition
- Medium posts: small "M" icon badge in top-right corner

### Unified Feed
- All posts (local + Medium) combined into one array
- Sorted by date descending
- First post (or featured post) → hero card
- Posts 2-4 → sidebar
- Posts 5+ → grid

## 4. Blog Detail Page Improvements

### Hero Header
- Same dark navy header as listing page
- Post title (large, white, Geist Sans bold)
- Category pills (blue on dark)
- Date + reading time (muted light text)
- Author line with avatar

### Content Area
- Max-width: 720px centered (optimal reading width)
- Ubuntu font for all body text
- Line-height: 1.8 for paragraphs (improved readability)
- Heading styles: Geist Sans, larger sizes, more vertical breathing room
- Blockquotes: blue left border + light blue background (`bg-blue-50`)
- Code blocks: dark background (`#1a1a2e`), rounded corners, monospace
- Tables: clean styling with alternating row backgrounds
- Images: rounded corners, subtle shadow

### Back Navigation
- Styled "Back to all posts" link at bottom with arrow icon

## 5. Responsive Behavior

| Breakpoint | Layout |
|-----------|--------|
| Desktop (1024px+) | Magazine (featured 2/3 + sidebar 1/3) + 3-col grid |
| Tablet (768-1023px) | Featured full-width + 2-col grid |
| Mobile (<768px) | Single column, all cards stacked |

## 6. Files to Create/Modify

| File | Action |
|------|--------|
| `src/app/layout.tsx` | Add Ubuntu font import |
| `src/app/globals.css` | Update body font-family to Ubuntu |
| `src/app/blog/page.tsx` | Complete rewrite — magazine layout, unified feed, hero header |
| `src/app/blog/[slug]/page.tsx` | Rewrite — dark hero header, improved typography |
| `src/lib/utils/medium-feed.ts` | May need type alignment for unified feed sorting |

## References

Design patterns researched from:
- Stripe blog (systematic restraint, typography-driven, featured treatment)
- Vercel blog (clean list, developer-centric, minimal decoration)
- Medium (reading-optimized typography, clean card design)
- Elementor's blog design research (visual hierarchy, color balance)
