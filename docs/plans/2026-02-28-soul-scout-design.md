# soul-scout — Design Document

**Created:** 2026-02-28
**Status:** Approved
**Location:** `~/soul/products/soul-scout/`
**Monorepo:** Part of `~/soul/` Go + TypeScript turborepo

---

## Problem

Rishav has profiles on 7+ platforms (website, LinkedIn, Naukri, Indeed, Wellfound, Instahyre, GitHub) plus upcoming freelance platforms (Toptal, Turing, Andela). Currently:

1. **No content sync** — Profile data drifts between platforms. No way to detect when Supabase (source of truth) differs from what's live.
2. **No opportunity monitoring** — Inbound matches, recruiter messages, and application status changes go unchecked. No structured daily review.
3. **No tailored resume generation** — One static resume for all roles. No way to quickly generate role-variant PDFs from Supabase data.
4. **No application tracking** — No centralized log of what was applied to, when, and what follow-up is needed.

## Solution

**soul-scout**: An automated daily agent that syncs content, monitors opportunities, generates tailored resumes, and tracks applications. Manual trigger (Phase 1) → auto-scheduled via soul-planner (Phase 2).

---

## Architecture

```
                    ┌─────────────────────┐
                    │   /scout (trigger)   │
                    │  Manual now, auto    │
                    │  via soul-planner    │
                    │  later               │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Scout Agent        │
                    │   (orchestrator)     │
                    └──────────┬──────────┘
                               │
          ┌────────────┬───────┴───────┬────────────┐
          ▼            ▼               ▼            ▼
   ┌──────────┐ ┌──────────┐  ┌──────────┐ ┌──────────┐
   │  SYNC    │ │  SWEEP   │  │ GENERATE │ │ TRACKER  │
   │ Supabase │ │ Browser  │  │ Resume   │ │ Log +    │
   │ vs Live  │ │ Monitor  │  │ + Cover  │ │ Report   │
   └──────────┘ └──────────┘  │ (PDF)    │ └──────────┘
                               └──────────┘
```

**Source of truth:** Supabase (portfolio database at rishavchatterjee.com)
**Report output:** `docs/scout-reports/YYYY-MM-DD-*.md`
**PDF output:** `drafts/applications/<company>-<role>-<date>.pdf`
**Tracker:** `docs/scout-tracker.md`

---

## Module 1: SYNC — Content Consistency Checker

### Purpose
Connect to Supabase, read current profile data, compare against what each platform should show. Generate a drift report.

### Data Flow
```
Supabase tables ──► sync module ──► compare against expected fields per platform
                                          │
                                    ┌─────▼──────┐
                                    │ Drift Report │
                                    └─────────────┘
```

### Supabase Tables Used
| Table | Fields Checked |
|-------|---------------|
| site_config | name, title, bio, social links |
| experience | role, company, period, achievements |
| skills | categories, skill names, levels |
| projects | title, description, tech stack |
| stats_dashboard | years experience, project count |

### Checks Per Platform

| Platform | What to Verify | How |
|----------|---------------|-----|
| rishavchatterjee.com | Resume page data matches Supabase | Fetch /resume page, compare rendered text against DB |
| LinkedIn | Headline, About, Experience, Skills | Browser snapshot, compare against Supabase experience/skills |
| GitHub README | Profile README matches current identity | Fetch raw README via GitHub API, compare key sections |
| Naukri | Headline, skills, experience summary | Browser snapshot, compare key fields |
| Indeed | Profile summary, skills | Browser snapshot |
| Wellfound | Bio, skills, experience | Browser snapshot |
| Instahyre | Profile completeness | Browser snapshot |

### Output
`docs/scout-reports/YYYY-MM-DD-sync.md`

```markdown
# Sync Report — 2026-02-28

## Summary
- Platforms checked: 7
- In sync: 5
- Drift detected: 2

## Per-Platform Status

### rishavchatterjee.com ✅ In Sync
All experience, skills, and projects match Supabase.

### LinkedIn ⚠️ Drift Detected
- Headline: "Senior Data Engineer" → should be "AI Engineer | AI Consultant | AI Researcher"
- Missing skill: "Claude Code"
- Experience: IBM-TWC role description outdated

### Naukri ✅ In Sync
...
```

---

## Module 2: SWEEP — Browser-Assisted Opportunity Monitor

### Purpose
Open each job portal in the browser, check for new inbound matches, recruiter messages, application status changes, and relevant postings. Summarize everything.

### Platforms to Sweep

| Platform | What to Check | Login Required |
|----------|--------------|----------------|
| LinkedIn Jobs | New recommendations, saved search results, InMail/messages | Yes (session) |
| Naukri | Recruiter views, new matches, application responses | Yes |
| Instahyre | Inbound company interest, new matches | Yes |
| Wellfound | New startup matches, message responses | Yes |
| Indeed | Application status updates, new recommendations | Yes |

### Sweep Process
For each platform:
1. Navigate to platform (use existing browser session)
2. Check notifications/messages section
3. Check job recommendations / inbound matches
4. Check application status updates
5. Extract key data points (company, role, match score if available)
6. Screenshot any high-priority items

### Output
`docs/scout-reports/YYYY-MM-DD-sweep.md`

```markdown
# Sweep Report — 2026-02-28

## Summary
- Platforms swept: 5
- New opportunities: 8
- Messages requiring response: 2
- Application status changes: 1

## LinkedIn Jobs
### New Recommendations (3)
1. **AI Platform Engineer** — Acme Corp (Bangalore, Remote) — 95% match
2. **Senior GenAI Engineer** — DataFlow Inc (Remote) — 88% match
3. **ML Engineer** — StartupX (Delhi) — 72% match

### Messages (1)
- Recruiter from TechCo: "Interested in discussing AI Lead role" — **ACTION: Respond**

## Naukri
### Recruiter Views (12 this week)
### New Matches (2)
1. **Data Engineer - AI** — MegaCorp (Gurugram)
2. **AI Consultant** — ConsultFirm (Remote)

## Instahyre
### Inbound Interest (1)
- **GenAI Startup** wants to connect — AI Engineer role — **ACTION: Review**

## Recommended Actions
1. 🔴 Respond to TechCo recruiter on LinkedIn (within 24h)
2. 🟡 Review GenAI Startup on Instahyre
3. 🟢 Apply to Acme Corp AI Platform Engineer (Variant A)
4. 🟢 Apply to DataFlow GenAI Engineer (Variant B)
```

---

## Module 3: GENERATE — Tailored Resume + Cover Note (PDF)

### Purpose
Pull profile data from Supabase, apply a role variant (A-G), generate a styled PDF resume and cover note tailored to a specific company/role.

### Role Variants (from resume-variants.md)

| Variant | Target Role |
|---------|-------------|
| A | AI Platform Architect / Solutions Architect |
| B | GenAI Engineer / LLM Engineer |
| C | Senior AI Engineer |
| D | AI Manager / AI Lead |
| E | AI Consultant / Freelance |
| F | AI Researcher |
| G | Senior Data Engineer (AI-focused) |

### Data Source
All data pulled from Supabase at generation time:
- `experience` table → work history with achievements
- `skills` table → skill categories and levels
- `projects` table → portfolio projects
- `site_config` table → personal info, bio, contact

### Variant Application
Each variant adjusts:
- **Headline** — role-specific title
- **Summary** — rewritten emphasis (same facts, different framing)
- **Bullet ordering** — which experience bullets lead (reorder, don't add/remove)
- **Project highlights** — which Soul projects to feature
- **Skills emphasis** — top skills for that role type
- **Cover note** — role-specific hook with `[COMPANY]` and `[SPECIFIC THING]` placeholders filled in

### PDF Generation Pipeline

```
Input: variant (A-G), company name, optional job posting URL
    │
    ▼
Supabase ──► Pull experience, skills, projects, site_config
    │
    ▼
Variant template ──► Apply headline, summary, bullet order, skills emphasis
    │
    ▼
HTML template ──► Render styled resume + cover note
    │
    ▼
Puppeteer/headless Chrome ──► Capture as PDF
    │
    ▼
Output: drafts/applications/<company>-<variant>-<date>.pdf
        drafts/applications/<company>-cover-<date>.pdf
```

### PDF Styling
- Clean, ATS-friendly layout (no columns, no graphics that break parsers)
- Consistent with rishavchatterjee.com/resume styling
- Print-optimized (A4, proper margins)
- Company name and date in filename for easy tracking

### Cover Note Generation
Separate from resume. Uses the cover note templates from `resume-variants.md` with:
- `[COMPANY]` → filled from input
- `[SPECIFIC THING]` → extracted from job posting URL if provided, or left as placeholder for manual fill
- `[ROLE]` → filled from input

---

## Module 4: TRACKER — Application Log + Daily Report

### Purpose
Maintain a structured log of all applications, their status, and follow-up dates. Generate combined daily reports.

### Tracker Format
`docs/scout-tracker.md`

```markdown
# Scout Tracker

## Active Applications

| Date | Company | Role | Platform | Variant | Status | Follow-up | Notes |
|------|---------|------|----------|---------|--------|-----------|-------|
| 2026-02-28 | Acme Corp | AI Platform Engineer | LinkedIn | A | Applied | 2026-03-05 | Custom cover note sent |
| 2026-02-28 | DataFlow | GenAI Engineer | LinkedIn | B | Applied | 2026-03-05 | Easy Apply |
| 2026-02-27 | TechCo | AI Lead | Recruiter | D | Interview Scheduled | 2026-03-03 | Phone screen |

## Status Legend
- **Applied** — Application submitted, waiting for response
- **Viewed** — Application viewed by recruiter/hiring manager
- **Interview Scheduled** — Interview booked
- **Interview Done** — Completed interview, awaiting feedback
- **Offer** — Received offer
- **Rejected** — Application rejected
- **Withdrawn** — Withdrawn by candidate
- **Follow-up Sent** — Follow-up message sent after no response

## Weekly Metrics

| Week | Applied | Responses | Interviews | Offers |
|------|---------|-----------|------------|--------|
| Feb 24-28 | 0 | 0 | 0 | 0 |
```

### Daily Report
`docs/scout-reports/YYYY-MM-DD-daily.md`

Combines output from all modules:

```markdown
# Scout Daily Report — 2026-02-28

## Content Sync
- Platforms checked: 7 | In sync: 5 | Drift: 2
- Action needed: Update LinkedIn headline, add Claude Code skill

## Opportunity Sweep
- New opportunities: 8 | Messages to respond: 2 | Status changes: 1
- Priority actions: [listed]

## Applications Today
- Applied: 3 | Followed up: 1
- Resumes generated: 2 (Variant A, Variant B)

## Follow-ups Due
- TechCo AI Lead — phone screen on March 3
- Acme Corp — follow up if no response by March 5

## Week-to-Date
- Total applied: 3/15 target | Responses: 0 | Interviews: 0
```

---

## Trigger + Scheduling

### Phase 1: Manual Trigger (Now)

Claude Code skills:
- `/scout` — Full daily routine: sync → sweep → report
- `/scout-resume <variant> <company>` — Generate tailored PDF resume
- `/scout-cover <variant> <company>` — Generate tailored cover note
- `/scout-apply <company> <role> <platform> <variant>` — Log application to tracker
- `/scout-report` — View today's report or generate if missing

### Phase 2: Auto-Scheduled (When soul-planner works)

- Agent auto-runs at 9pm IST daily
- Runs sync + sweep automatically
- Generates daily report
- Queues resume generation tasks for user-approved opportunities
- Sends summary to daily report

---

## Tech Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| Agent orchestrator | Go | Monorepo is Go-based, follows existing patterns |
| Supabase client | Go (supabase-go) or REST API | Source of truth access |
| Browser automation | Playwright MCP / Claude browser tools | Already available in Claude Code |
| PDF generation | Puppeteer (headless Chrome) | Renders HTML templates to styled PDF |
| HTML templates | Go templates or TypeScript | Resume + cover note layouts |
| Report generation | Markdown | Simple, readable, version-controlled |
| Tracker | Markdown table | Low overhead, git-tracked |

---

## File Structure

```
~/soul/products/soul-scout/
├── cmd/
│   └── scout/
│       └── main.go              # CLI entry point
├── internal/
│   ├── sync/
│   │   ├── checker.go           # Supabase vs platform comparison
│   │   └── platforms.go         # Per-platform check definitions
│   ├── sweep/
│   │   ├── monitor.go           # Browser sweep orchestrator
│   │   └── platforms.go         # Per-platform sweep logic
│   ├── generate/
│   │   ├── resume.go            # Resume generator
│   │   ├── cover.go             # Cover note generator
│   │   ├── variants.go          # Role variant definitions (A-G)
│   │   ├── pdf.go               # Puppeteer PDF capture
│   │   └── templates/
│   │       ├── resume.html      # Resume HTML template
│   │       └── cover.html       # Cover note HTML template
│   ├── tracker/
│   │   ├── log.go               # Application logger
│   │   └── report.go            # Daily report generator
│   └── supabase/
│       └── client.go            # Supabase REST client
├── templates/
│   ├── resume-a.html            # Variant A template
│   ├── resume-b.html            # ...
│   └── cover-generic.html
├── docs/
│   └── scout-reports/           # Generated reports
├── drafts/
│   └── applications/            # Generated PDFs
├── go.mod
├── go.sum
├── CLAUDE.md
├── README.md
└── Makefile
```

---

## Dependencies

| Dependency | Purpose |
|-----------|---------|
| Supabase REST API | Read profile data (experience, skills, projects) |
| Playwright MCP / Claude browser tools | Browser automation for sweep + sync |
| Puppeteer or chromedp | PDF generation from HTML |
| soul-planner (Phase 2) | Auto-scheduling daily runs |

---

## Success Criteria

1. `/scout` produces a daily report covering sync status + opportunities within 15 minutes
2. All 7 platforms checked for content consistency
3. Tailored PDF resume generated in < 30 seconds per variant
4. Application tracker shows all applications with status and follow-up dates
5. Week-to-date metrics visible at a glance
6. Zero manual data entry for profile sync (Supabase is the only place to update)

---

## What This Does NOT Do

- Does not auto-apply to jobs (requires user approval for every application)
- Does not send messages on behalf of the user (only drafts)
- Does not modify Supabase data (read-only from Supabase)
- Does not store credentials for job portals (relies on browser sessions)
- Does not replace soul-outreach (soul-outreach is for marketing/cold outreach, soul-scout is for job applications)
