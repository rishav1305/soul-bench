# CARS Benchmark Dashboard — UI Spec for Shuri/Happy

**Author:** Banner | **Date:** 2026-03-26
**Target:** Next.js static export → rishavchatterjee.com/cars (or /soul-bench)
**Data source:** `dashboard/data/dashboard.json` (65KB, build-time import)
**Lazy data:** `dashboard/data/prompts.json` (860KB, client-side fetch for Head-to-Head view)

---

## Architecture

```
soul-bench/
  dashboard/
    data/
      dashboard.json    # 65KB — models + metadata (import at build time)
      models.json       # 55KB — models only (alternate import)
      prompts.json      # 860KB — per-prompt results (lazy load)
      metadata.json     # 5KB — benchmark info + insights
    cars-data.ts        # Data transformation module (types, filters, sorts, derived computations)
    DASHBOARD_SPEC.md   # This file
    build_dashboard_data.py  # Regenerate data/ from raw results
```

### Tech Stack
- Next.js 14+ static export (`output: 'export'`)
- Recharts or Plotly.js for interactive charts
- Tailwind CSS, dark theme (zinc palette to match rishavchatterjee.com)
- TypeScript — all types in `cars-data.ts`

### Data Loading
```tsx
// At build time (getStaticProps or direct import)
import dashboardData from '../dashboard/data/dashboard.json';
import type { DashboardData } from '../dashboard/cars-data';
const data: DashboardData = dashboardData;

// Lazy load prompts for Head-to-Head view
const loadPrompts = () => fetch('/data/prompts.json').then(r => r.json());
```

---

## 5 Views

### View 1: Leaderboard (default view)

**Purpose:** Sortable table showing all 52 models with key metrics.

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ CARS Benchmark Leaderboard               [Sort: ▼]     │
│ 52 models • 7 providers • 30 prompts                   │
├─────────────────────────────────────────────────────────┤
│ [Search: ___________] [Providers: □□□□□□□] [Size: ──●──]│
├────┬──────────────────┬──────┬──────┬─────┬─────┬──────┤
│ #  │ Model            │Strict│Relax │ Tax │Lat  │CARS  │
│    │                  │  %   │  %   │(pp) │ (s) │Size  │
├────┼──────────────────┼──────┼──────┼─────┼─────┼──────┤
│ 1  │ 🟢 o3            │ 85.0 │ 85.0 │ 0.0 │4.72 │.0009 │
│ 2  │ 🟢 gpt-oss-20b   │ 79.4 │ 82.7 │ 3.3 │1.61 │.0257 │
│ ...│                  │      │      │     │     │      │
├────┴──────────────────┴──────┴──────┴─────┴─────┴──────┤
│ Click any row to expand → per-prompt results           │
└─────────────────────────────────────────────────────────┘
```

**Components:**
1. **FilterBar** — Search input, provider multiselect (color chips), size range slider
2. **SortableTable** — Columns: Rank, Model (with provider color dot), Strict %, Relaxed %, Format Tax, Latency, TPS, Size (GB), CARS_Size. Click column header to sort.
3. **ModelExpander** — On row click, expand to show:
   - 3 metric cards: Strict correct (N/30), Relaxed correct (N/30), Format Tax (N prompts)
   - 30 prompt results as collapsible list with ✅/🟡/❌ icons
   - Each prompt: task name, response preview, latency, score

**Data binding:**
- `filterModels()` from `cars-data.ts`
- `sortModels()` from `cars-data.ts`
- Prompts: lazy-load `prompts.json` only when a row is expanded

**Interactions:**
- Column header click → sort (toggle asc/desc)
- Provider chip click → toggle filter
- Size slider → filter range
- Row click → expand/collapse drill-down

---

### View 2: Efficiency Map

**Purpose:** Scatter plot showing accuracy vs latency vs model size.

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ CARS Efficiency Map              [Metric: Strict ○ Relax]│
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Accuracy (%)                                           │
│  90 ┤     ● gpt-5.2                                    │
│  80 ┤  ● gpt-oss-20b    ● o3                          │
│  70 ┤  ● gpt-4o              ● claude-sonnet-4        │
│  60 ┤      ● nova-micro                               │
│  50 ┤                        ● gemini-3-flash          │
│  40 ┤               ● gpt-5                            │
│  30 ┤                                                  │
│     └──┬──────┬──────┬──────┬──────┬──────┬──────       │
│        1s     2s     3s     4s     5s     6s  Latency   │
│                                                         │
│  ---- Pareto Frontier (dashed line)                    │
│  Bubble size = model parameters                         │
├─────────────────────────────────────────────────────────┤
│ Top 15 by CARS Efficiency                              │
│ ┌────┬──────────────┬────────┬───────┬───────┬────────┐│
│ │ #  │ Model        │ CARS   │Strict │ Lat   │ Size   ││
│ │ 1  │ nova-micro   │ 0.1856 │ 62.3% │ 1.42s │ 3GB   ││
│ └────┴──────────────┴────────┴───────┴───────┴────────┘│
└─────────────────────────────────────────────────────────┘
```

**Components:**
1. **ScatterChart** — X: latency, Y: accuracy, bubble size: est_size_gb, color: provider
2. **ParetoLine** — Dashed overlay using `paretoFrontier()` from `cars-data.ts`
3. **EfficiencyTable** — Top 15 by CARS_Size, ranked

**Interactions:**
- Hover bubble → tooltip with model name, CARS score, TPS
- Click bubble → highlight + show details
- Toggle: Strict vs Relaxed metric
- Zoom/pan on chart

---

### View 3: Format Tax

**Purpose:** Visualize the gap between strict and relaxed accuracy per model.

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ The Format Tax                                          │
│ Average across 52 models: 14pp                          │
├─────────────────────────────────────────────────────────┤
│ Horizontal stacked bar chart:                          │
│                                                         │
│ claude-opus-4-5     ▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░ 27pp gap    │
│ gemini-3-pro        ▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░ 27pp gap    │
│ claude-4.5-opus     ▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░ 27pp gap    │
│ ...                                                     │
│ o3                  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 0pp gap     │
│ gpt-3.5-turbo       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 0pp gap     │
│                                                         │
│ ▓ = Strict accuracy   ░ = Format tax (gap to relaxed)  │
├─────────────────────────────────────────────────────────┤
│ Category Breakdown for: [Select model ▼]               │
│                                                         │
│ Grouped bar chart: strict vs relaxed per category      │
│ (10 categories, two bars each)                          │
└─────────────────────────────────────────────────────────┘
```

**Components:**
1. **FormatTaxBar** — Horizontal stacked bars: blue = strict %, red = gap
2. **CategoryComparison** — Grouped bars per category for selected model
3. **ModelSelector** — Dropdown to pick model for category view

**Key insight callout:** Highlight that models with high format tax "know the answer" but can't follow instructions. This is the production deployment cost.

---

### View 4: Head-to-Head

**Purpose:** Compare 2-3 models on every prompt with actual responses visible.

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ Head-to-Head Comparison                                 │
│ [Model A ▼] vs [Model B ▼] vs [Model C ▼ (optional)]  │
├─────────────────────────────────────────────────────────┤
│ Summary comparison table (3 columns)                   │
├─────────────────────────────────────────────────────────┤
│ Category Radar Chart                                    │
│ (10-axis spider chart, one line per model)              │
├─────────────────────────────────────────────────────────┤
│ Prompt-by-Prompt (30 items, collapsible)               │
│                                                         │
│ ⚡ sh-001 — Diagnose API latency from JSON metrics     │
│ ┌──────────────────┬──────────────────┬────────────────┐│
│ │ Model A ✅        │ Model B 🟡       │ Model C ❌     ││
│ │ Latency: 2.3s    │ Latency: 4.1s    │ Latency: 6.2s ││
│ │ "{"diagnosis":   │ "The diagnosis   │ "Based on the  ││
│ │  "high_cpu"..."  │  is high CPU..." │  metrics..."   ││
│ └──────────────────┴──────────────────┴────────────────┘│
│                                                         │
│ ✅ = Both strict pass, ⚡ = Disagreement, ❌ = Both fail│
│ Disagreements expanded by default                      │
└─────────────────────────────────────────────────────────┘
```

**Components:**
1. **ModelPicker** — 2-3 multiselect dropdowns with autocomplete
2. **ComparisonTable** — Side-by-side summary stats
3. **RadarChart** — 10-category spider chart with opacity fill
4. **PromptList** — 30 collapsible items, each showing parallel responses
   - ⚡ Disagreements expanded by default (this is what's interesting)
   - ✅ Agreements collapsed
   - Actual response text shown (first 300 chars)

**Data loading:** Lazy-load `prompts.json` when user enters this view.

---

### View 5: Insights (The Uncomfortable Charts)

**Purpose:** 4 tabbed charts showing counter-intuitive findings.

**Tabs:**

#### Tab 5a: Generation Regression
- **Chart:** Line chart with 6 model families (GPT Main, GPT Mini/Nano, Claude Sonnet, Claude Opus, Gemini Pro, Gemini Flash)
- **X-axis:** Models in chronological order within each family
- **Y-axis:** Strict accuracy (%)
- **Key callouts:** GPT-5 vs GPT-3.5 (-19pp), Gemini 2.5 Pro vs 2.0 Flash (-32pp), Claude 3.7 vs 3.5 (-37pp)
- **Data:** Use `MODEL_FAMILIES` and `getGenerationRegression()` from `cars-data.ts`

#### Tab 5b: Reasoning Penalty
- **Chart:** Grouped bar (With Reasoning vs Without Reasoning)
- **Data:** Use `REASONING_PAIRS` and `getReasoningPenalties()` from `cars-data.ts`
- **Callout:** "Gemini 2.5 Flash: 2x worse WITH reasoning enabled"
- **Exception section:** O-series models that make reasoning work (o3 at 85% strict, 0pp tax)

#### Tab 5c: Provider Report Card
- **Chart:** Box plot per provider (relaxed accuracy distribution)
- **Table:** Provider summary (count, median, best, worst, spread)
- **Insight:** "Google has the highest ceiling AND lowest floor"

#### Tab 5d: Category Heatmap
- **Chart:** Heatmap grid (models × categories), RdYlGn color scale
- **Slider:** Top N models (10-52)
- **Insight:** Which categories are hard for everyone vs model-specific weaknesses

---

## Global Components

### Sidebar / Navigation
```
┌──────────────┐
│ 🏎️ CARS     │
│ soul-bench   │
├──────────────┤
│ ○ Leaderboard│ ← default
│ ○ Efficiency │
│ ○ Format Tax │
│ ○ Head-to-Head│
│ ○ Insights   │
├──────────────┤
│ Filters:     │
│ [Providers]  │
│ [Size range] │
├──────────────┤
│ 52 models    │
│ 7 providers  │
│ 30 prompts   │
│ 10 categories│
├──────────────┤
│ GitHub ↗     │
│ Methodology ↗│
└──────────────┘
```

### Methodology Section
Expandable section at the bottom of every view explaining:
- CARS formula and variants
- Dual scoring (strict vs relaxed)
- 10 task categories with descriptions
- Temperature 0.0, LiteLLM infrastructure
- Open source: link to GitHub repo

### Dark Theme
- Background: `zinc-950` (#09090b) or similar
- Cards: `zinc-900` (#18181b)
- Text: `zinc-100` (#f4f4f5)
- Provider colors: see `PROVIDER_COLORS` in `cars-data.ts`
- Charts: plotly_dark template or equivalent Recharts dark theme

---

## SEO / Meta

```html
<title>CARS Benchmark — 52 LLMs Ranked by Cost-Adjusted Accuracy | soul-bench</title>
<meta name="description" content="Which AI model gives the best bang for your buck? We benchmarked 52 LLMs from 7 providers on 30 real-world structured tasks. The results challenge everything you assumed." />
<meta property="og:image" content="/cars-og.png" />
```

Generate an OG image (1200x630) showing the top 5 models with CARS scores.

---

## File Deliverables from Banner

| File | Size | Purpose |
|------|------|---------|
| `dashboard/data/dashboard.json` | 65KB | All model data + metadata (build-time import) |
| `dashboard/data/models.json` | 55KB | Models only (alternative import) |
| `dashboard/data/prompts.json` | 860KB | Per-prompt results (lazy load) |
| `dashboard/data/metadata.json` | 5KB | Benchmark info + pre-computed insights |
| `dashboard/cars-data.ts` | 8KB | TypeScript types + filter/sort/computation functions |
| `dashboard/DASHBOARD_SPEC.md` | This file | UI spec with wireframes |

All data is pre-computed. Zero runtime API calls needed. Pure static site.

---

*Banner out. The data layer is ready. Ship something that makes people share it.*
