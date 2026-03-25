/**
 * CARS Benchmark Data Layer
 *
 * TypeScript module for loading and transforming CARS benchmark data.
 * Import into Next.js/React dashboard components.
 *
 * Data files:
 *   dashboard.json  — models + metadata (65KB, load at build time)
 *   prompts.json    — per-prompt results (860KB, lazy load for head-to-head view)
 *
 * Usage:
 *   import { loadDashboard, filterModels, getProviderStats } from './cars-data';
 *   const data = loadDashboard();
 *   const filtered = filterModels(data.models, { providers: ['OpenAI'] });
 */

// ─────────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────────

export interface CarsModel {
  id: string;
  model_id: string;
  provider: Provider;
  strict_pct: number;
  relaxed_pct: number;
  format_tax_pp: number;
  latency_s: number;
  tps: number;
  est_size_gb: number;
  cars_size: number;
  cars_size_relaxed: number;
  cars_ram: number;
  cars_vram: number;
  total_prompts: number;
  total_errors: number;
  category_strict: Record<string, number>;
  category_relaxed: Record<string, number>;
}

export interface PromptResult {
  model: string;
  provider: Provider;
  prompt_id: string;
  task: string;
  prompt_preview: string;
  response_preview: string;
  strict: number;     // 0 or 1
  relaxed: number;    // 0 or 1
  latency_s: number;
  tps: number;
}

export interface BenchmarkMetadata {
  benchmark: {
    name: string;
    version: string;
    date: string;
    description: string;
  };
  stats: {
    total_models: number;
    total_providers: number;
    total_prompts: number;
    total_categories: number;
    total_evaluations: number;
    avg_format_tax_pp: number;
  };
  categories: Record<string, string>;
  providers: Record<string, ProviderStats>;
  insights: {
    top_strict: string;
    top_strict_score: number;
    zero_format_tax: string[];
    most_efficient: string;
    generation_regressions: Array<{
      newer: string;
      older: string;
      delta_pp: number;
    }>;
    reasoning_penalties: Array<{
      model: string;
      with_reasoning: number;
      without: number;
      penalty_x: number;
    }>;
  };
  methodology: {
    scoring: string;
    cars_formula: string;
    infrastructure: string;
    prompts: string;
    temperature: number;
  };
  generated_at: string;
}

export interface ProviderStats {
  count: number;
  models: string[];
  median_strict: number;
  median_relaxed: number;
  best_strict: number;
  worst_strict: number;
  spread: number;
}

export interface DashboardData {
  metadata: BenchmarkMetadata;
  models: CarsModel[];
}

export type Provider =
  | "Anthropic"
  | "OpenAI"
  | "Google"
  | "Amazon"
  | "Mistral"
  | "Alibaba"
  | "DeepSeek"
  | "Mercury"
  | "Other";

export type SortField =
  | "strict_pct"
  | "relaxed_pct"
  | "format_tax_pp"
  | "cars_size"
  | "latency_s"
  | "tps"
  | "est_size_gb";

export type Category =
  | "Campaign Planning"
  | "Classification"
  | "Code Generation"
  | "Contact Research"
  | "Email Drafting"
  | "Infra Management"
  | "Knowledge QA"
  | "Reply Classification"
  | "System Health"
  | "Task Planning";

// ─────────────────────────────────────────────────────────
// Constants
// ─────────────────────────────────────────────────────────

export const PROVIDER_COLORS: Record<Provider, string> = {
  Anthropic: "#d4a574",
  OpenAI: "#74b9ff",
  Google: "#55efc4",
  Amazon: "#ff7675",
  Mistral: "#a29bfe",
  Alibaba: "#fd79a8",
  DeepSeek: "#00cec9",
  Mercury: "#ffeaa7",
  Other: "#636e72",
};

export const CATEGORIES: Category[] = [
  "Campaign Planning",
  "Classification",
  "Code Generation",
  "Contact Research",
  "Email Drafting",
  "Infra Management",
  "Knowledge QA",
  "Reply Classification",
  "System Health",
  "Task Planning",
];

/**
 * Model families for generation regression tracking.
 * Each family lists models in chronological order (oldest → newest).
 */
export const MODEL_FAMILIES: Record<string, string[]> = {
  "GPT Main": ["gpt-3.5-turbo-0125", "gpt-4-turbo", "gpt-4o", "gpt-5", "gpt-5.2"],
  "GPT Mini/Nano": ["gpt-4o-mini", "gpt-4.1-mini", "gpt-4.1-nano", "gpt-5-mini", "gpt-5-nano"],
  "Claude Sonnet": [
    "claude-3-sonnet-20240229",
    "claude-3-5-sonnet-20241022",
    "claude-sonnet-4-20250514",
    "claude-sonnet-4-5-20250929",
    "claude-sonnet-4-6",
  ],
  "Claude Opus": ["claude-4.5-opus", "claude-opus-4-5-20251101", "claude-opus-4-6"],
  "Gemini Pro": ["gemini-2.5-pro", "gemini-3-pro", "gemini-3.1-pro"],
  "Gemini Flash": ["gemini-2.0-flash", "gemini-2.5-flash", "gemini-3-flash"],
};

/**
 * Reasoning toggle pairs: [with_reasoning, without_reasoning, display_label]
 */
export const REASONING_PAIRS: [string, string, string][] = [
  ["gemini-2.5-flash", "gemini-2.5-flash-no-reasoning", "Gemini 2.5 Flash"],
  ["gemini-3-flash", "gemini-3-flash-no-reasoning", "Gemini 3 Flash"],
];

// ─────────────────────────────────────────────────────────
// Filter & Sort
// ─────────────────────────────────────────────────────────

export interface FilterOptions {
  providers?: Provider[];
  minSize?: number;
  maxSize?: number;
  minStrict?: number;
  maxLatency?: number;
  searchQuery?: string;
}

export function filterModels(
  models: CarsModel[],
  filters: FilterOptions
): CarsModel[] {
  return models.filter((m) => {
    if (filters.providers?.length && !filters.providers.includes(m.provider))
      return false;
    if (filters.minSize != null && m.est_size_gb < filters.minSize)
      return false;
    if (filters.maxSize != null && m.est_size_gb > filters.maxSize)
      return false;
    if (filters.minStrict != null && m.strict_pct < filters.minStrict)
      return false;
    if (filters.maxLatency != null && m.latency_s > filters.maxLatency)
      return false;
    if (
      filters.searchQuery &&
      !m.id.toLowerCase().includes(filters.searchQuery.toLowerCase()) &&
      !m.provider.toLowerCase().includes(filters.searchQuery.toLowerCase())
    )
      return false;
    return true;
  });
}

export function sortModels(
  models: CarsModel[],
  field: SortField,
  ascending = false
): CarsModel[] {
  const sorted = [...models].sort((a, b) => {
    const aVal = a[field];
    const bVal = b[field];
    return ascending ? aVal - bVal : bVal - aVal;
  });
  return sorted;
}

// ─────────────────────────────────────────────────────────
// Derived Computations
// ─────────────────────────────────────────────────────────

/**
 * Compute Pareto frontier: models where no other model is
 * both more accurate AND faster.
 */
export function paretoFrontier(
  models: CarsModel[],
  accuracyField: "strict_pct" | "relaxed_pct" = "strict_pct"
): CarsModel[] {
  const sorted = [...models].sort((a, b) => b[accuracyField] - a[accuracyField]);
  const frontier: CarsModel[] = [];
  let minLatency = Infinity;

  for (const m of sorted) {
    if (m.latency_s < minLatency) {
      frontier.push(m);
      minLatency = m.latency_s;
    }
  }

  return frontier.sort((a, b) => a.latency_s - b.latency_s);
}

/**
 * Get per-provider aggregate stats from filtered models.
 */
export function getProviderStats(
  models: CarsModel[]
): Record<string, ProviderStats> {
  const groups: Record<string, CarsModel[]> = {};
  for (const m of models) {
    if (!groups[m.provider]) groups[m.provider] = [];
    groups[m.provider].push(m);
  }

  const stats: Record<string, ProviderStats> = {};
  for (const [provider, pModels] of Object.entries(groups)) {
    const strict = pModels.map((m) => m.strict_pct).sort((a, b) => a - b);
    const relaxed = pModels.map((m) => m.relaxed_pct).sort((a, b) => a - b);
    stats[provider] = {
      count: pModels.length,
      models: pModels.map((m) => m.id),
      median_strict: strict[Math.floor(strict.length / 2)],
      median_relaxed: relaxed[Math.floor(relaxed.length / 2)],
      best_strict: strict[strict.length - 1],
      worst_strict: strict[0],
      spread: Math.round((strict[strict.length - 1] - strict[0]) * 10) / 10,
    };
  }

  return stats;
}

/**
 * Build generation regression data for a model family.
 */
export function getGenerationRegression(
  models: CarsModel[],
  family: string[]
): Array<{ model: string; strict_pct: number; order: number }> {
  return family
    .map((name, idx) => {
      const m = models.find((x) => x.id === name);
      return m ? { model: m.id, strict_pct: m.strict_pct, order: idx } : null;
    })
    .filter((x): x is NonNullable<typeof x> => x !== null);
}

/**
 * Build reasoning penalty comparison data.
 */
export function getReasoningPenalties(
  models: CarsModel[]
): Array<{
  label: string;
  with_reasoning: number;
  without_reasoning: number;
  penalty_pp: number;
  improvement_x: number;
}> {
  return REASONING_PAIRS.map(([withR, withoutR, label]) => {
    const on = models.find((m) => m.id === withR);
    const off = models.find((m) => m.id === withoutR);
    if (!on || !off) return null;
    return {
      label,
      with_reasoning: on.strict_pct,
      without_reasoning: off.strict_pct,
      penalty_pp: Math.round((off.strict_pct - on.strict_pct) * 10) / 10,
      improvement_x:
        Math.round((off.strict_pct / Math.max(on.strict_pct, 0.1)) * 10) / 10,
    };
  }).filter((x): x is NonNullable<typeof x> => x !== null);
}

/**
 * Get category heatmap data for top N models.
 */
export function getCategoryHeatmap(
  models: CarsModel[],
  n: number = 20,
  metric: "strict" | "relaxed" = "strict"
): {
  models: string[];
  categories: string[];
  data: number[][];  // models x categories
} {
  const topModels = sortModels(models, "strict_pct").slice(0, n);
  const field = metric === "strict" ? "category_strict" : "category_relaxed";

  return {
    models: topModels.map((m) => m.id),
    categories: CATEGORIES,
    data: topModels.map((m) =>
      CATEGORIES.map((cat) => m[field][cat] ?? 0)
    ),
  };
}
