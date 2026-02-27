# Performance Deep Clean Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Comprehensive performance optimization of the portfolio app — images, dependencies, lazy-loading, caching, fonts, dead code, and framer-motion removal.

**Architecture:** Work in phases: dead code first (safe, no visual change), then images, then lazy-loading, then caching, then framer-motion migration (highest risk). Each phase ends with a build check and commit.

**Tech Stack:** Next.js 15, Tailwind CSS, `next/image`, `sharp` CLI, IntersectionObserver, CSS animations, `unstable_cache`

---

## Task 1: Remove Dead Dependencies & Code

**Files:**
- Modify: `portfolio_app/package.json`
- Delete: `portfolio_app/src/app/v4_iostheme/` (entire directory)
- Delete: `portfolio_app/src/components/ui/HexagonBackground.tsx`

**Step 1: Remove unused npm packages**

```bash
cd /home/rishav/soul-old/portfolio_app
npm uninstall puppeteer d3 @types/d3
```

**Step 2: Delete v4_iostheme route**

```bash
rm -rf src/app/v4_iostheme
```

This removes 1000+ lines of dead iOS-theme variant code and 4 framer-motion imports.

**Step 3: Delete HexagonBackground.tsx**

Not imported in any active page (confirmed via grep on `src/app/`).

```bash
rm src/components/ui/HexagonBackground.tsx
```

**Step 4: Fix DataChart.tsx — replace d3 with recharts**

Read `src/components/data-visualization/DataChart.tsx`. It uses `d3` for a bar chart. Since `recharts` (which wraps d3 internally) is already a dependency and used elsewhere, rewrite DataChart to use recharts `<BarChart>` instead of raw d3. This eliminates the direct d3 dependency (880KB).

Minimal recharts replacement:
```tsx
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function DataChart({ data }: { data: Array<{ name: string; value: number }> }) {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="value" fill="#3b82f6" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
```

**Step 5: Build and commit**

```bash
npm run build
git add -A && git commit -m "perf: remove dead deps (puppeteer, d3), v4_iostheme, HexagonBackground"
```

---

## Task 2: Image Optimization

**Files:**
- Modify: all PNGs in `portfolio_app/public/images/`
- Delete: duplicate images in `portfolio_app/public/images/projects/thumbnail/` that also exist in `portfolio_app/public/images/projects/images/`
- Delete: `portfolio_app/public/images/photo_bg.png` (1.1MB, unused since Vanta removal)

**Step 1: Install sharp CLI for batch conversion**

```bash
npm install -D sharp-cli
```

Or use `npx sharp-cli` directly.

**Step 2: Identify and delete duplicate project images**

These files exist in both `/projects/thumbnail/` and `/projects/images/`:
- `rb_databricks_wrangling.png` (2.2MB each)
- `im_aws_migration.png` (2.1MB each)
- `jubilant_prod.png` (2.2MB each)

Keep one copy in `/projects/thumbnail/` (used by ProjectImage component). Delete from `/projects/images/` if no component references that path.

```bash
# Check which path is used in code first
grep -r "projects/images/" src/ --include="*.tsx" --include="*.ts"
grep -r "projects/thumbnail/" src/ --include="*.tsx" --include="*.ts"
```

Delete the unused duplicates.

**Step 3: Convert large PNGs to WebP**

```bash
cd public/images
# Convert profile images
npx sharp-cli -i profile.png -o profile.webp --format webp --quality 85
npx sharp-cli -i photo_bg.png -o photo_bg.webp --format webp --quality 80

# Convert project thumbnails
cd projects/thumbnail
for f in *.png; do
  npx sharp-cli -i "$f" -o "${f%.png}.webp" --format webp --quality 85
done
```

Keep original PNGs as fallback. Update component references to use `.webp` where possible, or let `next/image` handle format negotiation.

**Step 4: Optimize PWA icons**

The 3 icon files (180x180, 192x192, 512x512) are all 691KB each. Resize properly:

```bash
npx sharp-cli -i icon-512x512.png -o icon-512x512.webp --format webp --quality 90
npx sharp-cli -i icon-192x192.png --resize 192 -o icon-192x192.png --format png
npx sharp-cli -i icon-180x180.png --resize 180 -o icon-180x180.png --format png
```

**Step 5: Delete photo_bg.png if unused**

```bash
grep -r "photo_bg" src/ public/ --include="*.tsx" --include="*.ts" --include="*.css" --include="*.html"
```

If no results, delete it (1.1MB savings).

**Step 6: Build and commit**

```bash
npm run build
git add -A && git commit -m "perf: optimize images — WebP conversion, dedup, resize icons"
```

---

## Task 3: ProjectImage — Replace raw img with next/image

**Files:**
- Modify: `portfolio_app/src/components/ui/ProjectImage.tsx`

**Step 1: Rewrite ProjectImage with next/image**

```tsx
'use client';

import React, { useState } from 'react';
import Image from 'next/image';

interface ProjectImageProps {
  src: string;
  alt: string;
  className?: string;
  fallbackSrc?: string;
}

export default function ProjectImage({
  src,
  alt,
  className = "w-full h-32 object-cover rounded-md",
  fallbackSrc = '/images/projects/thumbnail/aws_logo.png'
}: ProjectImageProps) {
  const [imgSrc, setImgSrc] = useState(src);

  return (
    <div className={`relative ${className}`}>
      <Image
        src={imgSrc}
        alt={alt}
        fill
        sizes="(max-width: 768px) 100vw, 33vw"
        className="object-cover rounded-md"
        onError={() => setImgSrc(fallbackSrc)}
      />
    </div>
  );
}
```

Note: The parent `className` moves to a wrapper div since `next/image` with `fill` needs a positioned parent. Check all call sites to ensure sizing still works.

**Step 2: Build and verify visually**

```bash
npm run build
npm run dev
```

Check `/projects` page to confirm images render correctly.

**Step 3: Commit**

```bash
git add src/components/ui/ProjectImage.tsx
git commit -m "perf: replace raw img with next/image in ProjectImage"
```

---

## Task 4: Update next.config.ts

**Files:**
- Modify: `portfolio_app/next.config.ts`

**Step 1: Replace deprecated `domains` with `remotePatterns`**

```typescript
const nextConfig: NextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'miro.medium.com' },
      { protocol: 'https', hostname: '*.medium.com' },
      { protocol: 'https', hostname: 'cdn.jsdelivr.net' },
      { protocol: 'https', hostname: 'github.com' },
      { protocol: 'https', hostname: 'raw.githubusercontent.com' },
      { protocol: 'https', hostname: 'images.unsplash.com' },
    ],
    formats: ['image/avif', 'image/webp'],
  },
};
```

The `formats` array tells Next.js to serve AVIF (smallest) with WebP fallback automatically.

**Step 2: Build and commit**

```bash
npm run build
git add next.config.ts
git commit -m "perf: update next.config with remotePatterns and AVIF/WebP formats"
```

---

## Task 5: Font Optimization

**Files:**
- Modify: `portfolio_app/src/styles/custom-fonts.css`

**Step 1: Check which custom fonts are actually used**

```bash
grep -r "font-desdemona\|font-bauhaus\|font-blackletter\|font-modern-love\|font-stencil\|font-braggadocio" src/ --include="*.tsx" --include="*.ts"
```

**Step 2: Consolidate Braggadocio**

Remove duplicate imports. Keep only one source (Google Fonts `Bungee Shade` as the most reliable). Remove the cdnfonts and onlinewebfonts imports.

Update `.font-braggadocio` and `.font-braggadocio2` classes to use `'Bungee Shade'` as primary.

**Step 3: Remove any font imports not referenced in components**

If grep from Step 1 shows unused font classes, remove their `@import` and class definitions.

**Step 4: Add `font-display: swap` to custom @font-face**

For any remaining custom `@font-face` declarations, add `font-display: swap;` to prevent blocking.

**Step 5: Build and commit**

```bash
npm run build
git add src/styles/custom-fonts.css
git commit -m "perf: consolidate fonts — remove duplicate imports, add font-display swap"
```

---

## Task 6: Lazy-Load Heavy Components

**Files:**
- Modify: `portfolio_app/src/components/ui/ClientDynamicImports.tsx`
- Modify: `portfolio_app/src/app/page.tsx` (imports)
- Modify: `portfolio_app/src/app/layout.tsx` (ContactSidebar import)

**Step 1: Add dynamic imports to ClientDynamicImports.tsx**

```typescript
'use client';

import dynamic from 'next/dynamic';

export const SkillsRadar = dynamic(() => import('@/components/ui/SkillsRadar'), { ssr: false });
export const AIChatWidget = dynamic(() => import('@/components/ui/AIChatWidget'), { ssr: false });
export const ParticleField = dynamic(() => import('@/components/ui/ParticleField'), { ssr: false });
export const AutoScrollTestimonials = dynamic(() => import('@/components/ui/AutoScrollTestimonials'), { ssr: false });
export const ExperienceTimeline = dynamic(() => import('@/components/ui/ExperienceTimeline'), { ssr: false });
```

**Step 2: Update page.tsx imports**

Replace direct imports with dynamic ones:

```typescript
// BEFORE
import ParticleField from "@/components/ui/ParticleField";
import AutoScrollTestimonials from "@/components/ui/AutoScrollTestimonials";
import ExperienceTimeline from "@/components/ui/ExperienceTimeline";

// AFTER
import { ParticleField, AutoScrollTestimonials, ExperienceTimeline } from "@/components/ui/ClientDynamicImports";
```

**Step 3: Update layout.tsx for ContactSidebar**

Since layout.tsx is a server component, use `next/dynamic` directly:

```typescript
import dynamic from 'next/dynamic';
const ContactSidebar = dynamic(() => import('@/components/ui/ContactSidebar'), { ssr: false });
```

**Step 4: Build and commit**

```bash
npm run build
git add src/components/ui/ClientDynamicImports.tsx src/app/page.tsx src/app/layout.tsx
git commit -m "perf: lazy-load ParticleField, ContactSidebar, Testimonials, Timeline"
```

---

## Task 7: Data Fetching & Caching

**Files:**
- Modify: all files in `portfolio_app/src/services/`
- Modify: `portfolio_app/src/app/blog/page.tsx`

**Step 1: Wrap service functions with React `cache()`**

React's `cache()` deduplicates calls within a single server render. This fixes the duplicate `siteConfig` + `experience` fetches between layout.tsx and page.tsx.

For each service file, wrap the export:

```typescript
import { cache } from 'react';

export const getSiteConfig = cache(async (): Promise<SiteConfig | null> => {
  // ... existing Supabase query unchanged
});
```

Apply to ALL service files.

**Step 2: Add ISR to blog page**

```typescript
// At the top of src/app/blog/page.tsx
export const revalidate = 3600; // Revalidate every hour
```

**Step 3: Add `unstable_cache` for static content**

For data that rarely changes, use `unstable_cache`:

```typescript
import { unstable_cache } from 'next/cache';

export const getExperience = unstable_cache(
  async (): Promise<WorkExperience[]> => {
    // ... existing Supabase query
  },
  ['experience'],
  { revalidate: 86400 } // 24 hours
);
```

Apply to: experience, education, brands, testimonials, caseStudies, skillRadar.
Keep siteConfig with React `cache()` only (changes more often).

**Step 4: Build and commit**

```bash
npm run build
git add src/services/ src/app/blog/page.tsx
git commit -m "perf: add React cache() dedup + unstable_cache for services + ISR for blog"
```

---

## Task 8: Replace framer-motion — Simple whileInView Components

**Files:**
- Create: `portfolio_app/src/hooks/useInView.ts`
- Modify: `portfolio_app/src/app/globals.css`
- Modify: `portfolio_app/src/components/ui/AboutStats.tsx`
- Modify: `portfolio_app/src/components/ui/EducationHighlight.tsx`
- Modify: `portfolio_app/src/components/ui/BrandLogoGrid.tsx`

**Step 1: Create reusable `useInView` hook**

Create `portfolio_app/src/hooks/useInView.ts`:

```typescript
'use client';

import { useEffect, useRef, useState } from 'react';

export function useInView(options?: IntersectionObserverInit) {
  const ref = useRef<HTMLDivElement>(null);
  const [isInView, setIsInView] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsInView(true);
          observer.unobserve(el);
        }
      },
      { threshold: 0.1, ...options }
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  return { ref, isInView };
}
```

**Step 2: Add CSS animation classes to globals.css**

```css
.animate-fade-in-up {
  animation: fadeInUp 0.5s ease-out forwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(16px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
```

**Step 3: Rewrite AboutStats.tsx, EducationHighlight.tsx, BrandLogoGrid.tsx**

Replace `motion.div` with regular `div` + `useInView` + CSS class toggle. Pattern:

```tsx
const { ref, isInView } = useInView();

<div
  className={`... ${isInView ? 'animate-fade-in-up' : 'opacity-0'}`}
  style={{ animationDelay: `${index * 100}ms` }}
>
```

**Step 4: Build, verify scroll animations, commit**

```bash
npm run build
git add src/hooks/useInView.ts src/app/globals.css src/components/ui/AboutStats.tsx src/components/ui/EducationHighlight.tsx src/components/ui/BrandLogoGrid.tsx
git commit -m "perf: replace framer-motion whileInView with CSS animations + IntersectionObserver"
```

---

## Task 9: Replace framer-motion — BrandHexagonGrid

**Files:**
- Modify: `portfolio_app/src/components/ui/BrandHexagonGrid.tsx`

Uses `whileInView` + `whileHover` with spring physics. Replace:
- `whileInView` -> `useInView` + CSS animation
- `whileHover scale(1.15)` -> Tailwind `hover:scale-[1.15]`
- `whileHover filter drop-shadow` -> Tailwind `hover:drop-shadow-lg`
- Spring physics -> CSS `transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)`

**Step 1: Rewrite, build, verify hover effects, commit**

```bash
git add src/components/ui/BrandHexagonGrid.tsx
git commit -m "perf: replace framer-motion in BrandHexagonGrid with CSS animations"
```

---

## Task 10: Replace framer-motion — ContactSidebar (AnimatePresence)

**Files:**
- Modify: `portfolio_app/src/components/ui/ContactSidebar.tsx`

Uses nested `AnimatePresence` for enter/exit. Replace with CSS transitions:
- Keep element in DOM, toggle with CSS opacity/transform
- `pointer-events-none` when hidden

```tsx
<div className={`fixed right-0 top-1/3 z-50 flex items-start transition-all duration-500 ease-out
  ${isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-12 pointer-events-none'}`}>
  ...
  <div className={`mr-2 transition-all duration-300 ease-out origin-right
    ${isExpanded ? 'opacity-100 translate-x-0 scale-100' : 'opacity-0 translate-x-5 scale-95 pointer-events-none'}`}>
    ...
  </div>
</div>
```

**Step 1: Rewrite, build, verify sidebar appears/collapses, commit**

```bash
git add src/components/ui/ContactSidebar.tsx
git commit -m "perf: replace framer-motion AnimatePresence in ContactSidebar with CSS transitions"
```

---

## Task 11: Replace framer-motion — AutoScrollTestimonials

**Files:**
- Modify: `portfolio_app/src/components/ui/AutoScrollTestimonials.tsx`

Read file first. Replace motion carousel with CSS `transform: translateX()` transitions.

**Step 1: Read, rewrite, build, verify auto-scroll, commit**

```bash
git add src/components/ui/AutoScrollTestimonials.tsx
git commit -m "perf: replace framer-motion in AutoScrollTestimonials with CSS transitions"
```

---

## Task 12: Replace framer-motion — ExperienceTimeline

**Files:**
- Modify: `portfolio_app/src/components/ui/ExperienceTimeline.tsx`

Uses `AnimatePresence` for expand/collapse. Replace:
- Entry animations -> `useInView` + CSS
- Expand/collapse -> CSS `max-height` transition + `overflow: hidden`

**Step 1: Read, rewrite, build, verify expand/collapse, commit**

```bash
git add src/components/ui/ExperienceTimeline.tsx
git commit -m "perf: replace framer-motion in ExperienceTimeline with CSS transitions"
```

---

## Task 13: Replace framer-motion — AIChatWidget

**Files:**
- Modify: `portfolio_app/src/components/ui/AIChatWidget.tsx`

Uses `AnimatePresence` for chat bubble + messages. Replace:
- Open/close -> CSS opacity + scale transition
- Message entry -> CSS animation with stagger

**Step 1: Read, rewrite, build, verify chat widget, commit**

```bash
git add src/components/ui/AIChatWidget.tsx
git commit -m "perf: replace framer-motion in AIChatWidget with CSS transitions"
```

---

## Task 14: Remove framer-motion Dependency

**Step 1: Verify no remaining imports**

```bash
grep -r "framer-motion" src/ --include="*.tsx" --include="*.ts"
```

Should return zero results.

**Step 2: Uninstall**

```bash
npm uninstall framer-motion
```

**Step 3: Build and commit**

```bash
npm run build
git add package.json package-lock.json
git commit -m "perf: remove framer-motion dependency entirely"
```

---

## Task 15: Move Inline CSS to globals.css

**Files:**
- Modify: `portfolio_app/src/app/layout.tsx`
- Modify: `portfolio_app/src/app/globals.css`

**Step 1: Move force-light-mode styles to globals.css**

The `forceLightModeStyles` string is injected inline via a style tag on every page. Move it to globals.css instead.

Add to globals.css:
```css
/* Force light mode */
:root {
  --background: #ffffff !important;
  --foreground: #171717 !important;
  color-scheme: light !important;
}
```

Remove the `forceLightModeStyles` const and the inline style tag from layout.tsx.

**Step 2: Build and commit**

```bash
npm run build
git add src/app/layout.tsx src/app/globals.css
git commit -m "perf: move force-light-mode CSS from inline to globals.css"
```

---

## Task 16: Final Build, Verification & Push

**Step 1: Full production build**

```bash
npm run build
```

Verify zero errors.

**Step 2: Run dev server and check all pages**

```bash
npm run dev
```

Visit: `/`, `/blog`, `/projects`, `/contact`, `/testimonials`, `/experience`
Verify: images load, animations work, blog posts appear, no console errors.

**Step 3: Push to production**

```bash
git push origin main
```

Vercel auto-deploys. Check live site.

**Step 4: Run Lighthouse on production**

Use Chrome DevTools Lighthouse on the live site:
- Performance target: 90+
- Check LCP, FID, CLS metrics
