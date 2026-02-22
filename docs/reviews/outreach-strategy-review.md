# Outreach Strategy Review

**Date:** 2026-02-22
**Reviewed:** MASTER_PLAN.md, campaign-expansion.md, 05-phase5-campaigns.md

## What's Good

1. **Meta-play is genuinely clever** — "this email was sent using my own AI tool" demonstrates skills in the act of reaching out
2. **Three parallel tracks** (job / consulting / product) with clear priority ordering
3. **Campaign expansion** has smart segmentation — pharma angle (Novartis), India-focused, matching soul-* projects to audience pain points
4. **Enrichment + sequence approach** — personalized research per contact, multi-step followups

## What's Problematic

### 1. Not executable yet
soul-outreach has 2 files built (config.py + agents/client.py). Campaigns start "Month 2" but the tool is at ~5%.

### 2. Volume unrealistic for cold email
- 460-640 contacts across 10 campaigns
- Rate limit 20/day = 30 days for initial sends, 90 days with 3-step sequences
- Single sender domain at 20 cold emails/day = flagged within 2-3 weeks without domain warmup

### 3. Missing deliverability infrastructure
- No domain warmup plan
- No SPF/DKIM/DMARC setup
- No separate sending domain (never cold-email from primary domain)
- No inbox warmup tools (Warmbox, Instantly)
- No bounce rate monitoring (>5% kills sender reputation)
- No email verification (ZeroBounce, NeverBounce)

### 4. Subject lines are self-focused, not recipient-focused
"Built a 6,700-line AI OS" is impressive but reads as spam to hiring managers. Cold email subjects should be about THEIR needs, not YOUR achievements.

### 5. No warming/credibility layer before cold outreach
- No warm intro strategy
- No LinkedIn engagement before emailing
- No conference/meetup networking
- No contributions to target companies' open source repos

### 6. Consulting offer is generic
"Free 30-min architecture review" — every consultant offers this. Packages named but no case studies, outcomes, or pricing anchors.

### 7. No tracking/attribution plan
- No open rate tracking methodology
- No reply rate targets per campaign
- No A/B testing plan
- No kill criteria for underperforming campaigns

## Recommendations

### Priority 1: Make it executable
Get campaigns 1-2 working end-to-end with 20-30 contacts each before automating.

### Priority 2: Deliverability stack (Phase 0)
Separate sending domain, SPF/DKIM/DMARC, 2-3 week warmup, email verification.

### Priority 3: Recipient-centric subject lines
| Current | Better |
|---|---|
| "Built a 6,700-line AI OS" | "Question about {{team_name}}'s agent architecture" |

### Priority 4: Warm-up layer before cold outreach
LinkedIn engagement (2 weeks) -> blog posts (reference material) -> cold outreach to warmed contacts.

### Priority 5: Shrink and focus
Start with 60 contacts (30 AI labs + 30 Indian AI companies), nail those before scaling.

### Priority 6: Define success metrics
| Metric | Target |
|---|---|
| Email deliverability | >95% |
| Open rate | >40% |
| Reply rate | >8% |
| Positive reply rate | >3% |
| Interview conversion | >25% of positives |
