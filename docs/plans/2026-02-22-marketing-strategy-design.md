# Holistic Marketing Strategy — Content-Led Flywheel with Full-Spectrum Reach

**Date:** 2026-02-22
**Status:** Approved design
**Replaces:** Outreach-only strategy in MASTER_PLAN.md Phase 5

---

## Context

The previous strategy was cold-email-only: build soul-outreach, then email 600 people across 10 campaigns. Problems:

1. Single-channel dependency on a tool that's 5% built
2. No deliverability infrastructure (domain warmup, SPF/DKIM/DMARC)
3. No inbound engine (content, communities, SEO)
4. Job portals and recruiters completely absent
5. Freelance platforms absent
6. Consulting and product outreach limited to cold email

This strategy replaces that with an 11-channel approach serving all 3 tracks simultaneously.

---

## Three Tracks

| Track | Priority | Goal | Timeframe |
|---|---|---|---|
| 1. Job Change | PRIMARY | Land AI engineering role at top-tier company | 3-4 months |
| 2. Consulting + Freelance + Contract | PARALLEL | Steady income pipeline | 2-6 months |
| 3. Product (soul-outreach SaaS) | LONG-TERM | Users, revenue, open-source community | 4-12 months |

All three are real priorities. The strategy is designed so most activities serve 2-3 tracks simultaneously.

---

## Strategy: Content-Led Flywheel

Content creates gravity (people come to you), while direct applications + outreach + recruiters cover the "go to them" side. Every channel feeds the others.

```
                    INBOUND (they find you)
                           |
        Blog/SEO ----+---- LinkedIn posts ----+---- Twitter
        GitHub stars  |    Community presence  |    Open source
                      v                        v
              +-----------------+    +------------------+
              | Portfolio site  |    | GitHub profile    |
              | (credibility)   |    | (proof of work)   |
              +-----------------+    +------------------+
                      |                        |
                      +----------+-------------+
                                 |
                    CONVERSION (they engage)
                    - DMs, comments, inbound emails
                    - Recruiter calls from portals
                    - Referrals from network
                                 |
         +-----------+-----------+-----------+
         |           |           |           |
      Track 1     Track 2     Track 3     Track 1
      Job offer   Consulting  Product     Job offer
      (inbound)   lead        user        (applied)
                                 |
                    OUTBOUND (you reach them)
                           |
        Cold email ---+--- Direct apply ---+--- Recruiters
        LinkedIn DMs  |   Naukri/Indeed    |   Hiring consultancy
        Warm intros   |   Career pages     |   Staffing firms
                      |   Freelance platforms
```

---

## Budget

- **Starting cap:** 10,000-20,000 INR/month (~$120-240 USD)
- **Principle:** Start at 0. Add paid tools only when the free version proves the channel works.
- **ROI-driven:** Every spend must show measurable returns. Kill if not.
- **Gradual ramp:** Phase 0 at 0, Phase 1 at ~2000-3000, Phase 2 at ~5000-8000, Phase 3 at ~8000-15000

**Existing assets:** Custom domain, hosted portfolio (rishavchatterjee.com), domain email, LinkedIn profile updated, GitHub profile done, 6 repos pinned.

---

## Success Metrics

### Track 1: Job Change

| Milestone | Target | Timeframe |
|---|---|---|
| Profiles live on all portals | 5+ platforms | Week 1-2 |
| Registered with recruiters | 3-5 agencies | Week 2-3 |
| Applications submitted | 10-15/week | Ongoing |
| Recruiter-sourced interviews | 2-3/month | Month 2+ |
| Outreach-sourced conversations | 5-8/month | Month 2+ |
| Inbound interest (from content) | 1-2/month | Month 3+ |
| Offers | 1-3 | Month 3-4 |

### Track 2: Consulting + Freelance + Contract

| Milestone | Target | Timeframe |
|---|---|---|
| Freelance platform profiles live | 8-10 platforms | Week 2-4 |
| First freelance platform approval (Toptal/Turing) | 1-2 platforms | Month 1-2 |
| LinkedIn DM conversations with CTOs | 5-10/month | Month 2+ |
| Discovery calls | 2-4/month | Month 2+ |
| First paid engagement | 1 | Month 2-3 |
| Steady pipeline | $10-20K/month | Month 4-6 |

### Track 3: Product (soul-outreach)

| Milestone | Target | Timeframe |
|---|---|---|
| Product usable (Phase 1 complete) | Working CLI + web UI | Month 1-2 |
| GitHub repo public with README | Stars: 50+ | Month 2 |
| Product Hunt launch | 200+ upvotes | Month 3 |
| Show HN post | Front page | Month 3 |
| First external users | 10-20 | Month 3-4 |
| First paying users | 5-10 | Month 4-6 |

### ROI Decision Framework

| Spend | Keep if | Kill if |
|---|---|---|
| LinkedIn Premium | >5 meaningful conversations/month from InMail/insights | <2 conversations after 2 months |
| Naukri paid | >3 recruiter contacts/month | <1 contact after 1 month |
| Email infra (~2000 INR/mo) | >5% reply rate on cold campaigns | <2% reply rate after 50 sends |
| LinkedIn Ads | Cost per lead < 500 INR | Cost per lead > 2000 INR |
| Hiring consultancy | Gets interviews you can't get yourself | Zero interviews after 1 month |

---

## 11 Channels

### Channel 1: LinkedIn — Posts + Engagement + DMs (5h/week)

**Serves:** All 3 tracks
**Type:** Inbound + Outbound
**Cost:** Free -> Premium (when organic proves the channel)

**Weekly cadence:**

| Day | Activity | Time |
|---|---|---|
| Mon | Publish 1 post (technical insight or project update) | 45min |
| Tue | Engage: comment on 10 posts from target people | 30min |
| Wed | Send 5-10 targeted DMs (warm contacts) | 30min |
| Thu | Publish 1 post (career narrative, case study, or opinion) | 45min |
| Fri | Engage: comment on 10 posts + respond to all comments | 30min |
| Sat | Send 5-10 targeted DMs + review weekly analytics | 30min |
| Sun | Batch-write next week's 2 posts | 30min |

**Content pillars (rotating):**

1. **Building in public** — soul ecosystem progress, technical decisions, what worked/failed
2. **AI engineering lessons** — insights from 6 years of data eng + AI tools
3. **Data/numbers posts** — concrete metrics from past work (88% query resolution, 60% time reduction, 99.5% accuracy)
4. **Opinion/contrarian takes** — hot takes on AI engineering, tools, agent frameworks

**DM strategy:**
- Only DM people you've interacted with (commented on their posts, they liked yours) or who viewed your profile
- Template: reference their content + connect to your work + soft ask
- Never cold-spam DMs

**Upgrade trigger:** Move to LinkedIn Premium when consistently getting 1000+ impressions per post and need InMail + advanced search. Likely Month 2.

---

### Channel 2: Blog — Technical Long-Form (3h/week)

**Serves:** All 3 tracks
**Type:** Inbound (SEO + reference material)
**Cost:** Free

**Where:** rishavchatterjee.com/blog. Cross-post to dev.to and Hashnode for SEO reach.

**Cadence:** 1 post every 2 weeks (alternating: write week vs. publish+promote week)

**First 6 posts:**

| # | Title | Serves | Why This First |
|---|---|---|---|
| 1 | "How I Architect 31 Projects as a Solo Engineer with AI Tools" | Job, Consulting | Strongest differentiator story |
| 2 | "Building a Self-Healing AI System: Hysteresis + Remediation" | Job | Technical depth for AI lab interviews |
| 3 | "I Built an AI Outreach Tool That Sends Its Own Emails" | Product, Job | soul-outreach launch content |
| 4 | "Hub Election in Distributed Mesh Networks" | Job | Distributed systems cred |
| 5 | "CARS: A Practical Metric for Local AI Model Evaluation" | Job (research) | Original research angle |
| 6 | "What Enterprise AI Gets Wrong (And How to Fix It)" | Consulting | Consulting lead magnet |

**Content repurposing flow:**
```
Blog post (long)
  -> LinkedIn post (medium) x 2-3
    -> Twitter thread (short)
      -> 3-5 standalone tweets (atomic)
```

One piece of deep work feeds all three platforms.

---

### Channel 3: Twitter/X (2h/week)

**Serves:** Tracks 1, 2, 3
**Type:** Inbound + Outbound
**Cost:** Free

**Cadence:**

| Frequency | Activity |
|---|---|
| Daily (15min) | 3-5 replies to AI engineering discussions (add value, not "great post!") |
| 3x/week | 1 original tweet: project update, technical insight, or hot take |
| 1x/week | 1 thread: deeper dive (repurposed from blog or LinkedIn) |
| Ongoing | Follow + engage with: AI engineers at target companies, indie hackers, dev tool builders |

---

### Channel 4: GitHub + Open Source (Dev time, no separate allocation)

**Serves:** Tracks 1, 3
**Type:** Inbound
**Cost:** Free

**Actions:**
- Every soul-* extraction gets a clean README with architecture diagrams
- Pin the 6 most impressive repos (rotate as new ones ship)
- Contribute 1-2 PRs to popular AI repos (LangChain, CrewAI, or similar)
- Star and engage with repos from target companies
- Profile README links to portfolio, blog, LinkedIn
- Keep contribution graph green (daily commits from soul-* work)

---

### Channel 5: Job Portals (2h/week)

**Serves:** Track 1
**Type:** Outbound
**Cost:** Free -> Naukri paid (~1000-2000 INR/month when justified)

**Platforms:**

| Platform | Why | Ongoing |
|---|---|---|
| LinkedIn Jobs | Largest professional network, "Easy Apply" | 3-5 apps/week |
| Naukri | #1 in India hiring, recruiters search actively | 3-5 apps/week, refresh profile weekly |
| Indeed | Contract + MNC postings in India | 2-3 apps/week |
| Instahyre | Curated AI/tech jobs, companies apply to YOU | Review inbound matches |
| Wellfound (AngelList) | Startups, AI-first companies, often remote | 2-3 apps/week |
| Monster India | Some exclusive MNC postings | 1-2 apps/week |

**Weekly routine:**

| Day | Activity | Time |
|---|---|---|
| Mon | Scan LinkedIn Jobs + Naukri, apply to 3-5 best matches | 45min |
| Thu | Scan Indeed + Instahyre + Wellfound, apply to 3-5 matches | 45min |
| Sun | Refresh Naukri profile (triggers "recently active" boost), review Instahyre inbound | 30min |

**Application quality > quantity.** Every application gets:
- Tailored resume headline for the role
- 2-3 line cover note connecting experience to their specific needs
- Portfolio link

**Upgrade trigger:** Naukri paid when recruiter views > 10/week but contacts < 2.

---

### Channel 6: Freelance Platforms (1h/week steady-state, heavy setup)

**Serves:** Track 2 (freelance + contract)
**Type:** Outbound
**Cost:** Free

**Apply to ALL — each has different client pools:**

| Tier | Platform | Vetting | Best For |
|---|---|---|---|
| Premium | Toptal | Hard (screening + timed test + live project) | High-rate clients ($80-150/hr) |
| Premium | Turing | Automated coding tests + profile review | US companies, steady work |
| Premium | Andela | Interview-based vetting | Long-term placements |
| Mid-tier | Uplers | Profile review + skill test | India-focused data/AI roles |
| Mid-tier | Arc.dev | Async coding challenge + interview | Remote-first companies |
| Mid-tier | Gun.io | Invite-based | Senior roles, curated |
| Mid-tier | Lemon.io | Coding challenge + interview | European/US startups |
| Open | Upwork | No vetting, reputation-based | Quick gigs, volume |
| Open | Fiverr Pro | Portfolio review | Productized services |
| Open | Contra | Portfolio-based | Independent professionals |
| Niche | Braintrust | Token-based | AI/ML specific |
| Niche | Catalant | Enterprise consulting marketplace | Higher-ticket consulting |

**Setup phase (Week 2-4):** Apply to all 12. 8-10 hours total across 2 weeks.

**Steady state (1h/week):**
- Scan Upwork for AI/data projects, send 2-3 proposals/week
- Respond to inbound matches from vetted platforms
- Update profiles monthly

**Positioning across all platforms:**
- Headline: "AI Engineer | Production AI Systems | 6 Years Data Engineering"
- Lead with: GOAT platform (5000 users), Novartis (99.5% accuracy), soul-os (31 projects)
- Rate: Start at $80-100/hr on premium, $50-70 on open platforms

---

### Channel 7: Recruitment Agencies + Hiring Consultancies (1h/week)

**Serves:** Tracks 1, 2
**Type:** Outbound
**Cost:** Some paid (hiring consultancy, success-based)

**Type A: Tech recruitment agencies (register with 3-5)**

| Agency | Specialization |
|---|---|
| Michael Page India | Mid-senior tech, AI/data roles |
| Hays India | Contract + perm tech roles |
| TeamLease Digital | AI/ML placements in India |
| Xpheno | Niche tech, startup-focused |
| ABC Consultants | Senior/leadership tech roles |

**Type B: AI-specialized recruiters**
- Search LinkedIn for "AI recruiter India" or "ML recruitment"
- Connect with 10-15 individual recruiters
- Brief intro message about skills + availability

**Type C: Hiring consultancy (paid, for high-priority targets)**
- For roles at Anthropic/Google/DeepMind where consultancy has relationships
- Research firms with US tech company access
- Budget: 5000-10000 INR one-time or success-based
- Only activate if self-applied + outreach hasn't generated Tier 1 interviews by Month 2

**Weekly routine:**
- Week 1-2: Register with 5 agencies, connect with 10 recruiters on LinkedIn
- Ongoing: Respond to recruiter messages within 24h. Send monthly project updates. 30-60 min/week.

---

### Channel 8: Cold Outreach — Email + LinkedIn DMs (2h/week)

**Serves:** Tracks 1, 2
**Type:** Outbound
**Cost:** ~2000 INR/month (email infrastructure)

**Split:**

| Method | For | Volume | Why |
|---|---|---|---|
| LinkedIn DMs | Hiring managers, CTOs, AI leads | 10-15/week | ~50% open rate, no deliverability issues |
| Cold email | Bulk consulting outreach | 10-15/week | Scalable, automated sequences |

**LinkedIn DM approach (primary for Track 1):**
- Only DM after engaging with their content for at least 1 week
- 3-4 lines max. Reference something specific they posted. Connect to your work. Ask a question.
- Follow-up: If no response in 5 days, one follow-up referencing a new blog post

**Cold email approach (primary for Track 2):**
- Requires deliverability setup first (Phase 0)
- Start with 5 emails/day during warmup, ramp to 15-20/day
- 3-step sequence over 14 days
- Recipient-centric subject lines (about THEIR needs, not your achievements)

**Deliverability infrastructure (one-time setup):**

| Item | Cost | Notes |
|---|---|---|
| Separate sending domain | ~800 INR/year | Never cold email from primary domain |
| SPF + DKIM + DMARC | Free | DNS records on sending domain |
| Email warmup tool (Warmbox or similar) | ~1200 INR/month | 2-3 weeks before first campaign |
| Email verification (ZeroBounce) | ~1600 INR for 1000 emails | Verify before importing contacts |

---

### Channel 9: Communities (1h/week)

**Serves:** Tracks 2, 3
**Type:** Inbound
**Cost:** Free

**Pick 3-4 communities max:**

| Community | Platform | Why |
|---|---|---|
| r/selfhosted | Reddit | Perfect audience for soul-outreach |
| r/MachineLearning or r/artificial | Reddit | AI engineers, hiring managers lurk |
| MLOps Community | Slack | 15,000+ ML engineers, consulting leads + job referrals |
| Latent Space Discord | Discord | AI engineering focused, founders + engineers |

**Weekly cadence:**
- 3-4 thoughtful comments/answers across communities (15min each)
- 1 post per month sharing own work (only after 2+ weeks of contributing value)

**The rule:** 80% giving value, 20% mentioning your work (only when relevant).

---

### Channel 10: Paid Promotion (1h/week, budget-gated)

**Serves:** Tracks 2, 3
**Type:** Outbound
**Cost:** 0 -> 2000-5000 INR/month (when organic proves the channel)

**Stage 1: Free validation (Month 1-2)**
- Post organically. See what resonates.
- Track which topics get 5000+ impressions and 10+ comments.

**Stage 2: Amplify what works (Month 2-3)**

| Tactic | Budget | Expected Result | Kill Criteria |
|---|---|---|---|
| LinkedIn Ads: boost top posts | 2000-3000 INR/mo | 5000-15000 targeted impressions | Cost per engagement > 50 INR |
| LinkedIn Ads: lead magnet | 2000-3000 INR/mo | 10-30 leads/month | Cost per lead > 500 INR |

**Stage 3: Webinars (Month 3+)**

| Format | Topic | Lead Gen |
|---|---|---|
| LinkedIn Live (free) | "AI Agent Architecture for Production" | Attendees are warm consulting leads |
| YouTube webinar (free) | "31 AI Projects as a Solo Engineer" | Evergreen content + SEO |
| Paid workshop (test) | "Build Your First AI Agent" (2h, 500-1000 INR) | Revenue + lead qualification |

---

### Channel 11: Product Launches (Event-based)

**Serves:** Track 3
**Type:** Outbound
**Cost:** ~800 INR (landing page domain)

**Launch sequence (when soul-outreach Phase 1-2 complete):**

| Timing | Platform | Expected Impact |
|---|---|---|
| Pre-launch (2 weeks before) | Twitter + LinkedIn teasers | Build anticipation, collect early access emails |
| Launch Day | Product Hunt | 200-500 upvotes, 500-2000 visitors |
| Launch Day +1 | Hacker News "Show HN" | Front page = 5000-10000 visitors |
| Launch Week | Reddit (r/selfhosted, r/SideProject, r/SaaS) | 500-1000 visitors |
| Launch Week | Dev.to / Hashnode technical post | SEO + developer audience |
| Post-launch | AI tool directories (alternatives.to, futuretools.io, theresanaiforthat.com, awesome-selfhosted) | Passive discovery |
| Ongoing | Indie Hackers monthly updates | Community + accountability |

**Launch prep checklist (start 4 weeks before):**
- Demo video (2 min, screen recording + voiceover)
- Screenshots (5-6, polished, dark theme)
- Landing page on separate domain (e.g., souloutreach.dev)
- README with quick-start, architecture diagram, badges
- 10-15 beta testers who can support launch day
- LinkedIn + Twitter posts coordinated for launch day

---

## Phasing Timeline

### Phase 0: Foundation (Week 1-2) — Cost: 0 INR

**Goal:** Profiles live everywhere, content engine started.

| Action | Channel | Time |
|---|---|---|
| Optimize LinkedIn profile | 1 | Done |
| Set up Naukri profile, upload resume | 5 | 2h |
| Set up Indeed, Instahyre, Wellfound profiles | 5 | 3h |
| Apply to 5 freelance platforms (Toptal, Turing, Andela, Uplers, Arc.dev) | 6 | 6h |
| Connect with 10 recruiters on LinkedIn, register with 3 agencies | 7 | 3h |
| Publish first LinkedIn post | 1 | 1h |
| Set up Twitter profile for tech content | 3 | 30min |
| Join 3 communities (Reddit, Slack, Discord) | 9 | 1h |
| Start applying to 8-10 jobs/week on portals | 5 | 2h/week |
| Outline first blog post | 2 | 1h |

**By end of Week 2:** 6+ job portals, 5+ freelance platforms, 3+ recruiter relationships, first content published, communities joined.

### Phase 1: Build Momentum (Week 3-6) — Cost: ~2000-3000 INR/month

**Goal:** Consistent content cadence, first outreach conversations, first recruiter-sourced interviews.

| Action | Channel | Cadence |
|---|---|---|
| 2 LinkedIn posts/week | 1 | Ongoing |
| 10 LinkedIn comments/week on target people's content | 1 | Ongoing |
| 5-10 LinkedIn DMs/week (warmed contacts) | 1, 8 | Ongoing |
| 10-15 job applications/week across portals | 5 | Ongoing |
| Apply to remaining freelance platforms (7 more) | 6 | One-time |
| Publish blog post #1, cross-post to dev.to | 2 | Week 3-4 |
| 3-5 tweets/week + daily engagement | 3 | Ongoing |
| 3-4 community comments/week | 9 | Ongoing |
| Set up cold email infra (domain, warmup) | 8 | One-time |
| First 20-30 cold emails | 8 | Week 5-6 |
| Evaluate LinkedIn Premium | 1 | Week 6 |

**By end of Week 6:** Content cadence established, 50+ applications submitted, 3-5 recruiter conversations, first cold outreach sent, freelance platforms processing.

### Phase 2: Scale What Works (Week 7-12) — Cost: ~5000-8000 INR/month

**Goal:** Double down on producing channels. Cut underperformers.

| Action | Channel | Trigger |
|---|---|---|
| Boost top LinkedIn posts with ads | 10 | Organic posts consistently 2000+ impressions |
| Naukri paid upgrade | 5 | Recruiter views > 10/week but contacts < 2 |
| Hiring consultancy for Tier 1 targets | 7 | Self-applied + outreach hasn't generated Tier 1 interviews |
| Scale cold email to 15-20/day | 8 | Warmup complete + reply rate > 5% |
| Publish blog posts #2 and #3 | 2 | Every 2 weeks |
| First LinkedIn Live or webinar | 10 | Follower count hits 1000+ |
| Prepare soul-outreach for Product Hunt launch | 11 | Product Phase 1-2 complete |

**Evaluate + kill:**
- Portal with zero recruiter contacts after 6 weeks: deprioritize
- Freelance platform with zero matches after 6 weeks: archive
- Community with zero engagement: leave

### Phase 3: Leverage + Launch (Week 13-20) — Cost: ~8000-15000 INR/month

**Goal:** Product launch, consulting pipeline steady, job offers in hand.

| Action | Channel |
|---|---|
| Product Hunt + HN launch for soul-outreach | 11 |
| Paid workshop (test pricing) | 10 |
| Referral asks to connections | 7, 8 |
| Conference attendance (1-2 relevant) | New |
| Decision point: accept job / scale consulting / go all-in product | All |

---

## Weekly Schedule Template

**Total: 15-17h/week**

```
MONDAY (2.5h)
  - Scan job portals, apply to 3-5 roles (45min)
  - Publish LinkedIn post #1 of the week (30min)
  - Engage: 5 LinkedIn comments on target people's posts (15min)
  - 3-5 cold outreach messages (LinkedIn DMs or email) (30min)
  - Community: 1 thoughtful comment on Reddit/Slack (15min)

TUESDAY (2h)
  - Blog writing session (deep work, 1h)
  - Twitter: 1 original tweet + 3-5 replies (20min)
  - Respond to recruiter/inbound messages (20min)
  - Engage: 5 LinkedIn comments (15min)

WEDNESDAY (2h)
  - Send 5-10 LinkedIn DMs (warmed contacts) (30min)
  - Cold email batch (30min)
  - Twitter: 1 tweet + engagement (15min)
  - Freelance platform: check matches, send 1-2 proposals (30min)
  - Community: 1 comment (15min)

THURSDAY (2.5h)
  - Scan job portals, apply to 3-5 roles (45min)
  - Publish LinkedIn post #2 of the week (30min)
  - Engage: 5 LinkedIn comments (15min)
  - Blog writing session continued (45min)
  - Twitter: 1 tweet + engagement (15min)

FRIDAY (2h)
  - Respond to all LinkedIn comments from the week (20min)
  - Cold outreach: 3-5 messages (30min)
  - Recruiter follow-ups (15min)
  - Community: 1-2 comments (15min)
  - Review weekly analytics (30min)

SATURDAY (2.5h)
  - Batch-write next week's 2 LinkedIn posts (45min)
  - Blog: edit + finalize if publish week (45min)
  - Twitter thread (repurpose from blog/LinkedIn) (30min)
  - Freelance platform: update profiles, check new platforms (30min)

SUNDAY (1.5h)
  - Refresh Naukri profile (10min)
  - Review Instahyre/Wellfound inbound matches (20min)
  - Plan next week's content topics (20min)
  - Respond to weekend inbound messages (20min)
  - Month-to-date metrics review + budget decisions (20min)
```

---

## Contract Positioning

Contracts are not a separate channel. "Open to contract roles" is visible across:
- LinkedIn headline/about
- Naukri profile
- Freelance platform profiles
- Recruiter conversations
- Cold outreach messaging

---

## Content Repurposing Flow

```
Blog post (2000 words, biweekly)
  -> 2-3 LinkedIn posts (excerpts, key insights)
    -> 1 Twitter thread
      -> 3-5 standalone tweets
        -> 1-2 community posts (when relevant)
          -> Cold outreach attachment ("wrote about X")
```

One deep writing session produces content for all channels for 2 weeks.

---

## Key Design Decisions

1. **Content-led, not outreach-led.** Cold outreach is 1 of 11 channels, not the entire strategy. Content compounds; cold email doesn't.
2. **All 3 tracks served simultaneously.** Most channels serve 2-3 tracks. LinkedIn posts attract employers AND consulting leads AND product users.
3. **ROI-gated spending.** Every paid tool starts at $0. Upgrade only when free version proves the channel works. Kill criteria defined for every spend.
4. **Gradual ramp.** Phase 0 at 0 INR, Phase 3 at 8000-15000 INR/month. No big upfront spend.
5. **Job portals + recruiters added.** These fill 60-70% of positions and were completely absent from the previous strategy.
6. **Freelance platforms as a distinct channel.** 12 platforms, heavy setup, low maintenance. Fastest path to paid work.
7. **Cold outreach right-sized.** LinkedIn DMs primary (higher open rate), cold email secondary. Volume reduced from 600 contacts to focused micro-campaigns.
8. **Product launch is a coordinated event, not a drip.** PH + HN + Reddit + directories in one week for maximum impact.
