# Performance Deep Clean — Portfolio App

**Date:** 2026-02-27
**Status:** Approved
**Goal:** Comprehensive performance optimization covering images, dependencies, caching, lazy-loading, fonts, dead code, and framer-motion replacement.

## Section 1: Image Optimization (~10-15MB savings)

- Convert all PNGs in `/public/images/` to WebP using `sharp` CLI (60-70% compression)
- Delete duplicate thumbnails in `/images/projects/thumbnail/` that exist in `/images/`
- Replace raw `<img>` in `ProjectImage.tsx` with `next/image`
- Update `next.config.ts`: replace deprecated `domains` with `remotePatterns` for automatic format negotiation

## Section 2: Dependency Cleanup (~55MB node_modules, ~1MB+ client JS)

**Remove entirely:**
- `puppeteer` — never imported (50MB+)
- `d3` — 880KB, only used in `DataChart.tsx` which already uses `recharts`
- `framer-motion` — 5.6MB, replace with CSS animations (Section 7)

**Keep but verify lazy-loaded:**
- `@react-three/fiber` — only in `DataFlow3D`, already dynamic
- `recharts` — already lazy via `ClientDynamicImports`

## Section 3: Lazy-Loading & Code Splitting

Components to move behind `dynamic(() => import(...), { ssr: false })`:
- `ParticleField` — canvas effect, hero only
- `ContactSidebar` — floating sidebar, not needed at first paint
- `AutoScrollTestimonials` — below fold
- `ExperienceTimeline` — below fold, animation-heavy

Add loading skeletons where components are above-fold visible.

## Section 4: Data Fetching & Caching

- Wrap Supabase service functions with `unstable_cache` + revalidation intervals
  - `siteConfig`: revalidate every 1 hour
  - `experience`, `education`, `projects`: revalidate every 24 hours
  - `testimonials`, `caseStudies`, `brands`: revalidate every 24 hours
- Add `export const revalidate = 3600` to blog page for ISR (Medium RSS cached 1 hour)
- Remove duplicate `siteConfig`/`experience` fetch from `page.tsx` — use SiteConfigContext from layout

## Section 5: Font Optimization

- Consolidate `custom-fonts.css`: remove duplicate Braggadocio imports (3 sources -> 1)
- Add `font-display: swap` to all custom `@font-face` declarations
- Remove unused font imports if any fonts aren't referenced in components

## Section 6: Dead Code Removal

- Delete `/src/app/v4_iostheme/` route (unused alternate theme, ~1000+ LOC)
- Delete `HexagonBackground.tsx` if not used in current pages
- Delete `DataCleansingFlow.tsx` if orphaned
- Clean up stale imports and references

## Section 7: framer-motion Replacement

**Strategy:** CSS `@keyframes` + `IntersectionObserver` for scroll-triggered animations.

Replacement patterns:
- Simple fade/slide entrances -> CSS `animation` triggered by IntersectionObserver adding a class
- `AnimatePresence` (mount/unmount) -> CSS transitions with conditional class toggling
- Layout animations -> CSS `transition: all` on position/size changes

**Constraint:** Each component must maintain identical visual behavior. Before/after verification required.

**Components to migrate:**
- `ContactSidebar` — slide-in animation
- `BrandHexagonGrid` / `BrandLogoGrid` — fade-in on scroll
- `AboutStats` — counter animation
- `AutoScrollTestimonials` — carousel motion
- `EducationHighlight` — fade on scroll
- `ExperienceTimeline` — AnimatePresence + stagger
- `Navbar` — mobile menu animation
- `AIChatWidget` — message animations

## Estimated Impact

| Metric | Before | After (est.) |
|--------|--------|-------------|
| Image payload | ~17.9MB | ~4-5MB |
| Client JS (heavy deps) | ~7MB (d3+framer) | ~0.5MB |
| node_modules | ~894MB | ~835MB |
| Supabase queries/page | 10+ (with dupes) | 7 (cached) |
| Medium RSS calls | Every request | Cached 1h (ISR) |
| Font requests | 8 from 4 CDNs | 5-6 from 2 CDNs |
| Lighthouse (est.) | ~60-70 | 90+ |
