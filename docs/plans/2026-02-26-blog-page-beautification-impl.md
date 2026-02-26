# Blog Page Beautification Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Beautify the blog listing and detail pages with a premium magazine-style layout, add Ubuntu as the site-wide content font, and unify local + Medium posts into a single feed.

**Architecture:** Server component blog page with dark hero header, magazine two-column layout (featured + sidebar), then 3-column grid. All posts (local markdown + Medium RSS) merged and sorted by date. Ubuntu font added globally for body text while Geist Sans remains for headings.

**Tech Stack:** Next.js 15, Tailwind CSS v4, next/font/google (Ubuntu), date-fns, existing rss-parser + gray-matter

---

### Task 1: Add Ubuntu Font Globally

**Files:**
- Modify: `portfolio_app/src/app/layout.tsx:19-27` (font imports)
- Modify: `portfolio_app/src/app/layout.tsx:166` (body className)
- Modify: `portfolio_app/src/app/globals.css:24-28` (body font-family)

**Step 1: Add Ubuntu import to layout.tsx**

Add Ubuntu to the existing font imports and create the font instance.

**Step 2: Add Ubuntu CSS variable to body className**

Add `${ubuntu.variable}` to the body element's className.

**Step 3: Update globals.css body font-family**

Change body font-family to `var(--font-ubuntu), Arial, Helvetica, sans-serif`.

**Step 4: Verify locally**

Run: `cd portfolio_app && npm run dev`
Check: All body text renders in Ubuntu. Headings still use Geist Sans.

**Step 5: Commit**

```bash
git add portfolio_app/src/app/layout.tsx portfolio_app/src/app/globals.css
git commit -m "feat(portfolio): add Ubuntu as global body font"
```

---

### Task 2: Rewrite Blog Listing Page

**Files:**
- Modify: `portfolio_app/src/app/blog/page.tsx` (full rewrite)

**Key changes:**
1. Dark hero header section (`bg-gray-900`) matching homepage
2. Unified feed: merge local + Medium posts sorted by date
3. Magazine layout: featured hero card (3/5 width) + sidebar (2/5 width)
4. 3-column grid for remaining posts below
5. Borderless cards with hover lift animations
6. Category pills, reading time, Medium badges
7. Responsive: mobile stacks to single column

**Step 1: Rewrite page.tsx with new layout**

Full server component rewrite with unified post array, magazine grid, dark hero.

**Step 2: Verify locally**

Run: `cd portfolio_app && npm run dev`
Check: Dark hero, magazine layout, unified feed, hover effects, responsive.

**Step 3: Commit**

```bash
git add portfolio_app/src/app/blog/page.tsx
git commit -m "feat(portfolio): redesign blog listing with magazine layout and dark hero"
```

---

### Task 3: Rewrite Blog Detail Page

**Files:**
- Modify: `portfolio_app/src/app/blog/[slug]/page.tsx` (full rewrite)

**Key changes:**
1. Dark hero header with post title, categories, author, date
2. Content area: max-width 720px (optimal reading width)
3. Improved typography: line-height 1.8, better heading spacing
4. Better blockquotes: blue left border + light blue background
5. Better code blocks: dark rounded background with border
6. Animated "Back to all posts" link

Note: Uses existing `dangerouslySetInnerHTML` pattern which is safe because content comes exclusively from local markdown files in `content/blog/`, not from user input or external sources.

**Step 1: Rewrite page.tsx with new layout**

Full rewrite with dark hero header and improved article typography.

**Step 2: Verify locally**

Run: `cd portfolio_app && npm run dev`
Check: Dark hero, improved typography, blockquotes, code blocks.

**Step 3: Commit**

```bash
git add portfolio_app/src/app/blog/[slug]/page.tsx
git commit -m "feat(portfolio): redesign blog detail page with dark hero and improved typography"
```

---

### Task 4: Build Verification

**Step 1: Run production build**

Run: `cd portfolio_app && npm run build`
Expected: Build succeeds with no errors.

**Step 2: Fix any build errors**

Common issues: type mismatches in unified post array, missing imports, Tailwind v4 class issues.

**Step 3: Visual verification**

Check all pages:
1. Homepage — Ubuntu font in body text
2. `/blog` — Magazine layout with dark hero
3. `/blog/[slug]` — Dark hero, improved typography

**Step 4: Commit fixes if needed**

```bash
git add -A
git commit -m "fix(portfolio): resolve build errors from blog redesign"
```
