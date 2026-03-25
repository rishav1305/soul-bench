#!/usr/bin/env python3
"""
CARS Benchmark — Full 52-Model Comparative Report Generator
Generates publication-ready visualizations for Loki's content series.
"""

import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

OUTPUT_DIR = Path("/home/rishav/soul-roles/shared/briefs/banner-analyses")
DATA_FILE = OUTPUT_DIR / "cars-benchmark-2026-03-24-0620.json"

# Load data
with open(DATA_FILE) as f:
    data = json.load(f)

print(f"Loaded {len(data)} models")

# ─── Color palette by provider ───
PROVIDER_COLORS = {
    'claude': '#D97706',      # amber
    'gpt': '#2563EB',         # blue
    'gemini': '#059669',      # emerald
    'nova': '#7C3AED',        # purple
    'mistral': '#DC2626',     # red
    'mixtral': '#DC2626',     # red (same family)
    'qwen': '#EC4899',        # pink
    'mercury': '#6B7280',     # gray
    'o3': '#2563EB',          # blue (OpenAI)
    'o4': '#2563EB',          # blue (OpenAI)
    'r1': '#F97316',          # orange (DeepSeek)
    'gpt-oss': '#60A5FA',    # light blue (AWS)
}

def get_color(model_name):
    name = model_name.lower()
    for prefix, color in PROVIDER_COLORS.items():
        if name.startswith(prefix):
            return color
    return '#6B7280'

def get_provider(model_name):
    name = model_name.lower()
    if name.startswith('claude'): return 'Anthropic'
    if name.startswith(('gpt', 'o3', 'o4')): return 'OpenAI'
    if name.startswith('gpt-oss'): return 'AWS (OSS)'
    if name.startswith('gemini'): return 'Google'
    if name.startswith('nova'): return 'Amazon'
    if name.startswith(('mistral', 'mixtral')): return 'Mistral'
    if name.startswith('qwen'): return 'Alibaba'
    if name.startswith('mercury'): return 'Mercury'
    if name.startswith('r1'): return 'DeepSeek'
    return 'Other'

# ─── Prepare sorted data ───
ranked_strict = sorted(data, key=lambda x: x['summary']['avg_accuracy'], reverse=True)
ranked_relaxed = sorted(data, key=lambda x: x['summary']['avg_accuracy_relaxed'], reverse=True)
ranked_cars = sorted(data, key=lambda x: x.get('cars_size', 0), reverse=True)

# ═══════════════════════════════════════════════════════════════
# CHART 1: Strict vs Relaxed Accuracy — Top 25 Models (Horizontal Bar)
# ═══════════════════════════════════════════════════════════════
print("Generating Chart 1: Strict vs Relaxed accuracy...")

top25 = ranked_relaxed[:25]
fig, ax = plt.subplots(figsize=(14, 12))

models = [r['model'] for r in top25][::-1]  # reverse for bottom-to-top
strict = [r['summary']['avg_accuracy'] * 100 for r in top25][::-1]
relaxed = [r['summary']['avg_accuracy_relaxed'] * 100 for r in top25][::-1]
colors = [get_color(m) for m in models]

y_pos = np.arange(len(models))
bar_height = 0.35

# Relaxed bars (background, lighter)
bars_relaxed = ax.barh(y_pos + bar_height/2, relaxed, bar_height,
                        color=[c + '40' for c in colors], edgecolor=[c for c in colors], linewidth=1)
# Strict bars (foreground, solid)
bars_strict = ax.barh(y_pos - bar_height/2, strict, bar_height,
                       color=colors, edgecolor='white', linewidth=0.5)

ax.set_yticks(y_pos)
ax.set_yticklabels(models, fontsize=9, fontfamily='monospace')
ax.set_xlabel('Accuracy (%)', fontsize=12)
ax.set_title('CARS Benchmark: Top 25 Models by Relaxed Accuracy\nStrict (solid) vs Relaxed (outline) — Gap = "Format Tax"',
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlim(0, 100)
ax.axvline(x=80, color='#CBD5E1', linestyle='--', alpha=0.5, label='80% threshold')
ax.axvline(x=90, color='#94A3B8', linestyle='--', alpha=0.5, label='90% threshold')

# Add gap labels
for i, (s, r) in enumerate(zip(strict, relaxed)):
    gap = r - s
    if gap > 0:
        ax.text(r + 0.5, i, f'+{gap:.0f}pp', va='center', fontsize=7, color='#64748B')

# Legend
strict_patch = mpatches.Patch(color='#64748B', label='Strict accuracy')
relaxed_patch = mpatches.Patch(facecolor='#64748B40', edgecolor='#64748B', label='Relaxed accuracy')
ax.legend(handles=[strict_patch, relaxed_patch], loc='lower right', fontsize=10)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'cars-chart1-accuracy-top25.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: cars-chart1-accuracy-top25.png")

# ═══════════════════════════════════════════════════════════════
# CHART 2: CARS Efficiency Score — Top 20 (Size-adjusted)
# ═══════════════════════════════════════════════════════════════
print("Generating Chart 2: CARS efficiency scores...")

# Use relaxed CARS_Size from the report
top20_cars = ranked_cars[:20]
fig, ax = plt.subplots(figsize=(12, 9))

models_c = [r['model'] for r in top20_cars][::-1]
cars_scores = [r.get('cars_size', 0) for r in top20_cars][::-1]
colors_c = [get_color(m) for m in models_c]
sizes_c = [r.get('est_size_gb', 0) for r in top20_cars][::-1]

y_pos = np.arange(len(models_c))
bars = ax.barh(y_pos, cars_scores, color=colors_c, edgecolor='white', linewidth=0.5)

# Add size labels
for i, (score, size) in enumerate(zip(cars_scores, sizes_c)):
    ax.text(score + 0.001, i, f'{size:.0f}B | {score:.4f}', va='center', fontsize=8, color='#475569')

ax.set_yticks(y_pos)
ax.set_yticklabels(models_c, fontsize=9, fontfamily='monospace')
ax.set_xlabel('CARS_Size Score (higher = more cost-efficient)', fontsize=11)
ax.set_title('CARS Efficiency: Top 20 Models\nCARS_Size = Accuracy / (Size_GB × Latency_s)',
             fontsize=14, fontweight='bold', pad=15)

# Provider legend
providers_seen = {}
for m, c in zip(models_c, colors_c):
    p = get_provider(m)
    if p not in providers_seen:
        providers_seen[p] = c
legend_patches = [mpatches.Patch(color=c, label=p) for p, c in providers_seen.items()]
ax.legend(handles=legend_patches, loc='lower right', fontsize=9)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'cars-chart2-efficiency-top20.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: cars-chart2-efficiency-top20.png")

# ═══════════════════════════════════════════════════════════════
# CHART 3: Accuracy vs Latency Scatter (all 52 models)
# ═══════════════════════════════════════════════════════════════
print("Generating Chart 3: Accuracy vs latency scatter...")

fig, ax = plt.subplots(figsize=(14, 10))

for r in data:
    m = r['model']
    strict_acc = r['summary']['avg_accuracy'] * 100
    relaxed_acc = r['summary']['avg_accuracy_relaxed'] * 100
    lat = r['summary']['avg_latency_s']
    size = r.get('est_size_gb', 10)
    color = get_color(m)

    # Size of dot proportional to model size (log scale)
    dot_size = max(20, min(300, np.log2(size + 1) * 30))

    ax.scatter(lat, relaxed_acc, s=dot_size, color=color, alpha=0.7, edgecolors='white', linewidths=0.5)

    # Label top performers and outliers
    if relaxed_acc > 88 or strict_acc > 75 or (relaxed_acc > 80 and lat < 2) or relaxed_acc < 40:
        fontsize = 7
        offset = (5, 5)
        ax.annotate(m, (lat, relaxed_acc), xytext=offset, textcoords='offset points',
                   fontsize=fontsize, color='#334155', alpha=0.9,
                   arrowprops=dict(arrowstyle='-', color='#CBD5E1', lw=0.5))

ax.set_xlabel('Average Latency (seconds)', fontsize=12)
ax.set_ylabel('Relaxed Accuracy (%)', fontsize=12)
ax.set_title('CARS: Accuracy vs Latency — All 52 Models\nDot size ∝ model parameters (log scale)',
             fontsize=14, fontweight='bold', pad=15)

# Quadrant lines
ax.axhline(y=80, color='#E2E8F0', linestyle='--', alpha=0.7)
ax.axvline(x=5, color='#E2E8F0', linestyle='--', alpha=0.7)

# Quadrant labels
ax.text(1.5, 95, 'Fast & Accurate', fontsize=10, color='#16A34A', alpha=0.5, fontweight='bold')
ax.text(8, 95, 'Slow & Accurate', fontsize=10, color='#D97706', alpha=0.5, fontweight='bold')
ax.text(1.5, 38, 'Fast & Inaccurate', fontsize=10, color='#DC2626', alpha=0.3, fontweight='bold')
ax.text(8, 38, 'Slow & Inaccurate', fontsize=10, color='#7F1D1D', alpha=0.3, fontweight='bold')

# Provider legend
providers_in_chart = {}
for r in data:
    p = get_provider(r['model'])
    c = get_color(r['model'])
    if p not in providers_in_chart:
        providers_in_chart[p] = c
legend_patches = [mpatches.Patch(color=c, label=p) for p, c in providers_in_chart.items()]
ax.legend(handles=legend_patches, loc='lower left', fontsize=9)

ax.set_xlim(0, 16)
ax.set_ylim(30, 100)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'cars-chart3-scatter-all.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: cars-chart3-scatter-all.png")

# ═══════════════════════════════════════════════════════════════
# CHART 4: Format Tax — Gap between Strict and Relaxed
# ═══════════════════════════════════════════════════════════════
print("Generating Chart 4: Format tax (strict-relaxed gap)...")

# Sort by gap
gap_data = []
for r in data:
    strict_acc = r['summary']['avg_accuracy'] * 100
    relaxed_acc = r['summary']['avg_accuracy_relaxed'] * 100
    gap = relaxed_acc - strict_acc
    gap_data.append((r['model'], gap, strict_acc, relaxed_acc))

gap_data.sort(key=lambda x: x[1], reverse=True)

fig, ax = plt.subplots(figsize=(14, 12))

models_g = [g[0] for g in gap_data][::-1]
gaps = [g[1] for g in gap_data][::-1]
colors_g = [get_color(m) for m in models_g]

y_pos = np.arange(len(models_g))
bars = ax.barh(y_pos, gaps, color=colors_g, edgecolor='white', linewidth=0.5)

# Color bars by severity
for i, (bar, gap) in enumerate(zip(bars, gaps)):
    if gap >= 20:
        bar.set_color('#DC2626')  # Red: severe tax
    elif gap >= 15:
        bar.set_color('#F59E0B')  # Amber: moderate tax
    elif gap >= 10:
        bar.set_color('#3B82F6')  # Blue: mild tax
    else:
        bar.set_color('#10B981')  # Green: low tax

ax.set_yticks(y_pos)
ax.set_yticklabels(models_g, fontsize=7, fontfamily='monospace')
ax.set_xlabel('Format Tax (Relaxed − Strict, percentage points)', fontsize=11)
ax.set_title('The "Format Tax": How Much Accuracy Models Lose to Formatting\n0pp = perfect format compliance, 27pp = severe formatting issues',
             fontsize=13, fontweight='bold', pad=15)

# Legend
patches = [
    mpatches.Patch(color='#10B981', label='Low (0-9pp)'),
    mpatches.Patch(color='#3B82F6', label='Mild (10-14pp)'),
    mpatches.Patch(color='#F59E0B', label='Moderate (15-19pp)'),
    mpatches.Patch(color='#DC2626', label='Severe (20+pp)'),
]
ax.legend(handles=patches, loc='lower right', fontsize=9)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'cars-chart4-format-tax.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: cars-chart4-format-tax.png")

# ═══════════════════════════════════════════════════════════════
# CHART 5: Provider Comparison — Box Plot by Provider Family
# ═══════════════════════════════════════════════════════════════
print("Generating Chart 5: Provider comparison box plots...")

provider_scores = {}
for r in data:
    provider = get_provider(r['model'])
    relaxed = r['summary']['avg_accuracy_relaxed'] * 100
    if provider not in provider_scores:
        provider_scores[provider] = []
    provider_scores[provider].append(relaxed)

# Sort by median
providers_sorted = sorted(provider_scores.keys(), key=lambda p: np.median(provider_scores[p]), reverse=True)

fig, ax = plt.subplots(figsize=(12, 7))
box_data = [provider_scores[p] for p in providers_sorted]
bp = ax.boxplot(box_data, labels=providers_sorted, patch_artist=True, vert=True,
                medianprops=dict(color='black', linewidth=2),
                whiskerprops=dict(color='#64748B'),
                capprops=dict(color='#64748B'))

provider_color_map = {
    'Anthropic': '#D97706', 'OpenAI': '#2563EB', 'Google': '#059669',
    'Amazon': '#7C3AED', 'Mistral': '#DC2626', 'Alibaba': '#EC4899',
    'Mercury': '#6B7280', 'DeepSeek': '#F97316', 'AWS (OSS)': '#60A5FA'
}
for patch, prov in zip(bp['boxes'], providers_sorted):
    patch.set_facecolor(provider_color_map.get(prov, '#94A3B8') + '60')
    patch.set_edgecolor(provider_color_map.get(prov, '#94A3B8'))

# Add model count
for i, prov in enumerate(providers_sorted):
    count = len(provider_scores[prov])
    median = np.median(provider_scores[prov])
    ax.text(i + 1, median + 2, f'n={count}', ha='center', fontsize=8, color='#64748B')

ax.set_ylabel('Relaxed Accuracy (%)', fontsize=12)
ax.set_title('CARS Accuracy by Provider Family\nBox plots show distribution across all provider models',
             fontsize=14, fontweight='bold', pad=15)
ax.set_ylim(25, 100)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'cars-chart5-provider-boxplot.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: cars-chart5-provider-boxplot.png")

# ═══════════════════════════════════════════════════════════════
# CHART 6: Reasoning Penalty — With vs Without Reasoning
# ═══════════════════════════════════════════════════════════════
print("Generating Chart 6: Reasoning penalty comparison...")

reasoning_pairs = [
    ('gemini-2.5-flash', 'gemini-2.5-flash-no-reasoning', 'Gemini 2.5 Flash'),
    ('gemini-3-flash', 'gemini-3-flash-no-reasoning', 'Gemini 3 Flash'),
]

# Also add o3/o3-mini/o4-mini as "reasoning-only" models
reasoning_models = ['o3', 'o3-mini', 'o4-mini']

model_lookup = {r['model']: r for r in data}

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left: paired comparison
ax = axes[0]
x = np.arange(len(reasoning_pairs))
width = 0.35

with_reasoning = []
without_reasoning = []
labels = []
for with_r, without_r, label in reasoning_pairs:
    wr = model_lookup.get(with_r, {}).get('summary', {})
    wor = model_lookup.get(without_r, {}).get('summary', {})
    with_reasoning.append(wr.get('avg_accuracy', 0) * 100)
    without_reasoning.append(wor.get('avg_accuracy', 0) * 100)
    labels.append(label)

bars1 = ax.bar(x - width/2, with_reasoning, width, label='With Reasoning', color='#DC2626', alpha=0.8)
bars2 = ax.bar(x + width/2, without_reasoning, width, label='Without Reasoning', color='#10B981', alpha=0.8)

ax.set_ylabel('Strict Accuracy (%)', fontsize=11)
ax.set_title('Reasoning Penalty on Structured Tasks', fontsize=13, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=10)
ax.legend(fontsize=10)
ax.set_ylim(0, 100)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=9)

# Right: reasoning-only models
ax2 = axes[1]
reasoning_data = []
for m in reasoning_models:
    if m in model_lookup:
        r = model_lookup[m]
        reasoning_data.append({
            'model': m,
            'strict': r['summary']['avg_accuracy'] * 100,
            'relaxed': r['summary']['avg_accuracy_relaxed'] * 100,
            'latency': r['summary']['avg_latency_s']
        })

r_models = [d['model'] for d in reasoning_data]
r_strict = [d['strict'] for d in reasoning_data]
r_relaxed = [d['relaxed'] for d in reasoning_data]

x2 = np.arange(len(r_models))
bars3 = ax2.bar(x2 - width/2, r_strict, width, label='Strict', color='#2563EB', alpha=0.8)
bars4 = ax2.bar(x2 + width/2, r_relaxed, width, label='Relaxed', color='#60A5FA', alpha=0.8)

ax2.set_ylabel('Accuracy (%)', fontsize=11)
ax2.set_title('Reasoning-Only Models (OpenAI o-series)', fontsize=13, fontweight='bold')
ax2.set_xticks(x2)
ax2.set_xticklabels(r_models, fontsize=10)
ax2.legend(fontsize=10)
ax2.set_ylim(0, 100)

for bars in [bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=9)

plt.suptitle('The Reasoning Trade-off: Thinking Harder ≠ Better at Structured Tasks',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'cars-chart6-reasoning-penalty.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: cars-chart6-reasoning-penalty.png")

# ═══════════════════════════════════════════════════════════════
# CHART 7: Generation Regression — Newer ≠ Better
# ═══════════════════════════════════════════════════════════════
print("Generating Chart 7: Generation regression...")

# GPT family
gpt_timeline = [
    ('gpt-3.5-turbo-0125', 'GPT-3.5\nTurbo'),
    ('gpt-4-turbo', 'GPT-4\nTurbo'),
    ('gpt-4o', 'GPT-4o'),
    ('gpt-4o-mini', 'GPT-4o\nMini'),
    ('gpt-4.1', 'GPT-4.1'),
    ('gpt-4.1-mini', 'GPT-4.1\nMini'),
    ('gpt-4.1-nano', 'GPT-4.1\nNano'),
    ('gpt-5', 'GPT-5'),
    ('gpt-5-mini', 'GPT-5\nMini'),
    ('gpt-5-nano', 'GPT-5\nNano'),
    ('gpt-5.2', 'GPT-5.2'),
]

# Claude family
claude_timeline = [
    ('claude-3-haiku-20240307', 'Claude 3\nHaiku'),
    ('claude-3-sonnet-20240229', 'Claude 3\nSonnet'),
    ('claude-3-5-haiku-20241022', 'Claude 3.5\nHaiku'),
    ('claude-3-5-sonnet-20241022', 'Claude 3.5\nSonnet v2'),
    ('claude-3-7-sonnet-20250219', 'Claude 3.7\nSonnet'),
    ('claude-haiku-4-5-20251001', 'Claude 4.5\nHaiku'),
    ('claude-sonnet-4-20250514', 'Claude\nSonnet 4'),
    ('claude-sonnet-4-5-20250929', 'Claude\nSonnet 4.5'),
    ('claude-sonnet-4-6', 'Claude\nSonnet 4.6'),
    ('claude-opus-4-5-20251101', 'Claude\nOpus 4.5'),
    ('claude-opus-4-6', 'Claude\nOpus 4.6'),
]

# Gemini family
gemini_timeline = [
    ('gemini-2.0-flash', 'Gemini 2.0\nFlash'),
    ('gemini-2.5-flash-no-reasoning', 'Gemini 2.5\nFlash (no-R)'),
    ('gemini-2.5-flash', 'Gemini 2.5\nFlash'),
    ('gemini-2.5-pro', 'Gemini 2.5\nPro'),
    ('gemini-3-flash-no-reasoning', 'Gemini 3\nFlash (no-R)'),
    ('gemini-3-flash', 'Gemini 3\nFlash'),
    ('gemini-3-pro', 'Gemini 3\nPro'),
    ('gemini-3.1-pro', 'Gemini 3.1\nPro'),
]

fig, axes = plt.subplots(3, 1, figsize=(16, 14))

for ax, timeline, title, color in [
    (axes[0], gpt_timeline, 'OpenAI GPT Family', '#2563EB'),
    (axes[1], claude_timeline, 'Anthropic Claude Family', '#D97706'),
    (axes[2], gemini_timeline, 'Google Gemini Family', '#059669'),
]:
    valid_models = [(m, l) for m, l in timeline if m in model_lookup]
    if not valid_models:
        continue

    labels = [l for _, l in valid_models]
    strict = [model_lookup[m]['summary']['avg_accuracy'] * 100 for m, _ in valid_models]
    relaxed = [model_lookup[m]['summary']['avg_accuracy_relaxed'] * 100 for m, _ in valid_models]

    x = np.arange(len(labels))
    ax.plot(x, strict, 'o-', color=color, linewidth=2, markersize=8, label='Strict', alpha=0.9)
    ax.plot(x, relaxed, 's--', color=color, linewidth=1.5, markersize=6, label='Relaxed', alpha=0.5)

    # Highlight regressions
    for i in range(1, len(strict)):
        if strict[i] < strict[i-1] - 5:  # >5pp drop
            ax.annotate('', xy=(i, strict[i]), xytext=(i-1, strict[i-1]),
                       arrowprops=dict(arrowstyle='->', color='#DC2626', lw=2))

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel('Accuracy (%)', fontsize=10)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_ylim(20, 100)
    ax.legend(loc='lower left', fontsize=9)
    ax.grid(axis='y', alpha=0.3)

plt.suptitle('Generation Regression: Newer Models Don\'t Always Score Higher\nRed arrows = significant accuracy drops (>5pp)',
             fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'cars-chart7-generation-regression.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: cars-chart7-generation-regression.png")

# ═══════════════════════════════════════════════════════════════
# CHART 8: Category Heatmap — Top 15 Models
# ═══════════════════════════════════════════════════════════════
print("Generating Chart 8: Category accuracy heatmap...")

top15 = ranked_relaxed[:15]
categories = list(top15[0].get('category_accuracy_relaxed', {}).keys())

if categories:
    heatmap_data = []
    model_names = []
    for r in top15:
        cat_acc = r.get('category_accuracy_relaxed', {})
        row = [cat_acc.get(cat, 0) * 100 for cat in categories]
        heatmap_data.append(row)
        model_names.append(r['model'])

    heatmap_array = np.array(heatmap_data)

    fig, ax = plt.subplots(figsize=(14, 8))
    im = ax.imshow(heatmap_array, cmap='RdYlGn', aspect='auto', vmin=40, vmax=100)

    ax.set_xticks(np.arange(len(categories)))
    ax.set_yticks(np.arange(len(model_names)))
    ax.set_xticklabels([c.replace('-', '\n') for c in categories], fontsize=9)
    ax.set_yticklabels(model_names, fontsize=9, fontfamily='monospace')

    # Add text values
    for i in range(len(model_names)):
        for j in range(len(categories)):
            val = heatmap_array[i, j]
            text_color = 'white' if val < 60 else 'black'
            ax.text(j, i, f'{val:.0f}', ha='center', va='center', fontsize=7, color=text_color)

    plt.colorbar(im, ax=ax, label='Relaxed Accuracy (%)')
    ax.set_title('Category-Level Accuracy Heatmap (Top 15 Models, Relaxed Scoring)\nGreen = strong, Red = weak',
                 fontsize=13, fontweight='bold', pad=15)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'cars-chart8-category-heatmap.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: cars-chart8-category-heatmap.png")
else:
    print("  SKIP: No category data available")

print("\n✅ All charts generated!")
print(f"\nFiles saved to: {OUTPUT_DIR}/cars-chart*.png")
