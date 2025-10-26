"""
Create comprehensive visualizations for economic efficiency analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (18, 14)
plt.rcParams['font.size'] = 10

print("="*80)
print("CREATING ECONOMIC EFFICIENCY VISUALIZATIONS")
print("="*80)

# Load data
df = pd.read_csv('data/processed/transfer_efficiency_metrics.csv')
print(f"\nLoaded {len(df)} transfers")

# Create output directory
Path('results/figures').mkdir(parents=True, exist_ok=True)

# ============================================================================
# FIGURE 1: COMPREHENSIVE EFFICIENCY DASHBOARD
# ============================================================================
fig = plt.figure(figsize=(20, 14))

# 1. Efficiency by Fee Bracket
ax1 = plt.subplot(3, 3, 1)
df['fee_bracket'] = pd.cut(
    df['fee_millions'],
    bins=[0, 1, 5, 10, 20, 50, 200],
    labels=['<€1M', '€1-5M', '€5-10M', '€10-20M', '€20-50M', '>€50M']
)
fee_stats = df.groupby('fee_bracket', observed=True)['efficiency_score'].agg(['mean', 'count'])
bars = ax1.bar(range(len(fee_stats)), fee_stats['mean'], color='#3498db', alpha=0.8, edgecolor='black')
ax1.set_xticks(range(len(fee_stats)))
ax1.set_xticklabels(fee_stats.index, rotation=45, ha='right')
ax1.set_ylabel('Avg Efficiency Score', fontweight='bold')
ax1.set_title('Efficiency by Fee Bracket', fontweight='bold', fontsize=12)
ax1.grid(axis='y', alpha=0.3)
ax1.axhline(y=50, color='red', linestyle='--', alpha=0.5, label='Average')

for i, (bar, count) in enumerate(zip(bars, fee_stats['count'])):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
            f'{height:.1f}\n(n={count})', ha='center', va='bottom', fontsize=9)

# 2. Efficiency by League
ax2 = plt.subplot(3, 3, 2)
league_stats = df.groupby('league')['efficiency_score'].agg(['mean', 'count']).sort_values('mean', ascending=False)
colors = ['#2ecc71' if x > 50 else '#e74c3c' for x in league_stats['mean']]
bars = ax2.barh(range(len(league_stats)), league_stats['mean'], color=colors, alpha=0.8, edgecolor='black')
ax2.set_yticks(range(len(league_stats)))
ax2.set_yticklabels(league_stats.index)
ax2.set_xlabel('Avg Efficiency Score', fontweight='bold')
ax2.set_title('Efficiency by League', fontweight='bold', fontsize=12)
ax2.axvline(x=50, color='red', linestyle='--', alpha=0.5)
ax2.grid(axis='x', alpha=0.3)

for i, (bar, count) in enumerate(zip(bars, league_stats['count'])):
    width = bar.get_width()
    ax2.text(width + 1, i, f'{width:.1f} (n={count})', va='center', fontsize=9)

# 3. Efficiency by Position
ax3 = plt.subplot(3, 3, 3)
position_stats = df.groupby('position')['efficiency_score'].agg(['mean', 'count']).sort_values('mean', ascending=False)
colors_pos = ['#3498db', '#9b59b6', '#e67e22', '#95a5a6']
bars = ax3.bar(range(len(position_stats)), position_stats['mean'], color=colors_pos, alpha=0.8, edgecolor='black')
ax3.set_xticks(range(len(position_stats)))
ax3.set_xticklabels(position_stats.index, rotation=45, ha='right')
ax3.set_ylabel('Avg Efficiency Score', fontweight='bold')
ax3.set_title('Efficiency by Position', fontweight='bold', fontsize=12)
ax3.grid(axis='y', alpha=0.3)
ax3.axhline(y=50, color='red', linestyle='--', alpha=0.5)

for i, (bar, count) in enumerate(zip(bars, position_stats['count'])):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height + 1,
            f'{height:.1f}\n(n={count})', ha='center', va='bottom', fontsize=9)

# 4. Cost-per-Goal by Fee Bracket
ax4 = plt.subplot(3, 3, 4)
cpg_stats = df[df['cost_per_goal'].notna()].groupby('fee_bracket', observed=True)['cost_per_goal'].mean()
bars = ax4.bar(range(len(cpg_stats)), cpg_stats, color='#e74c3c', alpha=0.8, edgecolor='black')
ax4.set_xticks(range(len(cpg_stats)))
ax4.set_xticklabels(cpg_stats.index, rotation=45, ha='right')
ax4.set_ylabel('Cost per Goal (€M)', fontweight='bold')
ax4.set_title('Cost-per-Goal by Fee Bracket', fontweight='bold', fontsize=12)
ax4.grid(axis='y', alpha=0.3)

for bar in bars:
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height + 0.2,
            f'€{height:.1f}M', ha='center', va='bottom', fontsize=9)

# 5. VfM Score Distribution
ax5 = plt.subplot(3, 3, 5)
ax5.hist(df['vfm_score'], bins=30, color='#2ecc71', alpha=0.7, edgecolor='black')
ax5.axvline(df['vfm_score'].median(), color='red', linestyle='--', linewidth=2, label=f'Median: {df["vfm_score"].median():.2f}')
ax5.set_xlabel('VfM Score', fontweight='bold')
ax5.set_ylabel('Frequency', fontweight='bold')
ax5.set_title('Value-for-Money Score Distribution', fontweight='bold', fontsize=12)
ax5.legend()
ax5.grid(axis='y', alpha=0.3)

# 6. Efficiency Category Distribution
ax6 = plt.subplot(3, 3, 6)
category_counts = df['efficiency_category'].value_counts()
colors_cat = {'Excellent': '#2ecc71', 'Good': '#3498db', 'Average': '#f39c12', 'Poor': '#e74c3c', 'Very Poor': '#95a5a6'}
colors_list = [colors_cat.get(cat, '#95a5a6') for cat in category_counts.index]
wedges, texts, autotexts = ax6.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%',
                                     colors=colors_list, startangle=90)
ax6.set_title('Transfer Efficiency Distribution', fontweight='bold', fontsize=12)

# 7. Fee vs Efficiency Score Scatter
ax7 = plt.subplot(3, 3, 7)
scatter = ax7.scatter(df['fee_millions'], df['efficiency_score'], 
                     c=df['perf_after_goals'], cmap='viridis', alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
ax7.set_xlabel('Transfer Fee (€M)', fontweight='bold')
ax7.set_ylabel('Efficiency Score', fontweight='bold')
ax7.set_title('Fee vs Efficiency (colored by goals)', fontweight='bold', fontsize=12)
ax7.grid(alpha=0.3)
cbar = plt.colorbar(scatter, ax=ax7)
cbar.set_label('Goals After Transfer', rotation=270, labelpad=15)

# Add trend line
z = np.polyfit(df['fee_millions'], df['efficiency_score'], 1)
p = np.poly1d(z)
ax7.plot(df['fee_millions'].sort_values(), p(df['fee_millions'].sort_values()), 
        "r--", alpha=0.8, linewidth=2, label=f'Trend: y={z[0]:.2f}x+{z[1]:.2f}')
ax7.legend()

# 8. Top 10 Most Efficient Transfers
ax8 = plt.subplot(3, 3, 8)
top_10 = df.nlargest(10, 'efficiency_score')[['player_name', 'efficiency_score', 'fee_millions']].copy()
top_10['label'] = top_10['player_name'].str[:15] + ' (€' + top_10['fee_millions'].round(1).astype(str) + 'M)'
y_pos = range(len(top_10))
bars = ax8.barh(y_pos, top_10['efficiency_score'], color='#2ecc71', alpha=0.8, edgecolor='black')
ax8.set_yticks(y_pos)
ax8.set_yticklabels(top_10['label'], fontsize=8)
ax8.set_xlabel('Efficiency Score', fontweight='bold')
ax8.set_title('Top 10 Most Efficient Transfers', fontweight='bold', fontsize=12)
ax8.grid(axis='x', alpha=0.3)

for i, bar in enumerate(bars):
    width = bar.get_width()
    ax8.text(width + 1, i, f'{width:.1f}', va='center', fontsize=8)

# 9. Bottom 10 Least Efficient Transfers
ax9 = plt.subplot(3, 3, 9)
bottom_10 = df.nsmallest(10, 'efficiency_score')[['player_name', 'efficiency_score', 'fee_millions']].copy()
bottom_10['label'] = bottom_10['player_name'].str[:15] + ' (€' + bottom_10['fee_millions'].round(1).astype(str) + 'M)'
y_pos = range(len(bottom_10))
bars = ax9.barh(y_pos, bottom_10['efficiency_score'], color='#e74c3c', alpha=0.8, edgecolor='black')
ax9.set_yticks(y_pos)
ax9.set_yticklabels(bottom_10['label'], fontsize=8)
ax9.set_xlabel('Efficiency Score', fontweight='bold')
ax9.set_title('Bottom 10 Least Efficient Transfers', fontweight='bold', fontsize=12)
ax9.grid(axis='x', alpha=0.3)

for i, bar in enumerate(bars):
    width = bar.get_width()
    ax9.text(width + 1, i, f'{width:.1f}', va='center', fontsize=8)

plt.suptitle('Transfer Economic Efficiency Analysis Dashboard', fontsize=16, fontweight='bold', y=0.995)
plt.tight_layout(rect=[0, 0, 1, 0.99])
plt.savefig('results/figures/efficiency_dashboard.png', dpi=300, bbox_inches='tight')
print("\n✅ Saved: results/figures/efficiency_dashboard.png")
plt.close()

# ============================================================================
# FIGURE 2: LEAGUE COMPARISON
# ============================================================================
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Average fee by league
ax1 = axes[0, 0]
league_fee = df.groupby('league')['fee_millions'].mean().sort_values(ascending=False)
bars = ax1.barh(range(len(league_fee)), league_fee, color='#3498db', alpha=0.8, edgecolor='black')
ax1.set_yticks(range(len(league_fee)))
ax1.set_yticklabels(league_fee.index)
ax1.set_xlabel('Average Transfer Fee (€M)', fontweight='bold')
ax1.set_title('Average Transfer Fee by League', fontweight='bold', fontsize=13)
ax1.grid(axis='x', alpha=0.3)

for i, bar in enumerate(bars):
    width = bar.get_width()
    ax1.text(width + 1, i, f'€{width:.1f}M', va='center')

# Average goals by league
ax2 = axes[0, 1]
league_goals = df.groupby('league')['perf_after_goals'].mean().sort_values(ascending=False)
bars = ax2.barh(range(len(league_goals)), league_goals, color='#2ecc71', alpha=0.8, edgecolor='black')
ax2.set_yticks(range(len(league_goals)))
ax2.set_yticklabels(league_goals.index)
ax2.set_xlabel('Average Goals After Transfer', fontweight='bold')
ax2.set_title('Average Goals by League', fontweight='bold', fontsize=13)
ax2.grid(axis='x', alpha=0.3)

for i, bar in enumerate(bars):
    width = bar.get_width()
    ax2.text(width + 0.1, i, f'{width:.2f}', va='center')

# Efficiency vs Fee by League
ax3 = axes[1, 0]
for league in df['league'].unique():
    league_data = df[df['league'] == league]
    ax3.scatter(league_data['fee_millions'], league_data['efficiency_score'], 
               label=league, alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
ax3.set_xlabel('Transfer Fee (€M)', fontweight='bold')
ax3.set_ylabel('Efficiency Score', fontweight='bold')
ax3.set_title('Efficiency vs Fee by League', fontweight='bold', fontsize=13)
ax3.legend(loc='best', fontsize=9)
ax3.grid(alpha=0.3)

# League efficiency comparison
ax4 = axes[1, 1]
league_eff = df.groupby('league')['efficiency_score'].mean().sort_values(ascending=False)
colors = ['#2ecc71' if x > 50 else '#e74c3c' for x in league_eff]
bars = ax4.bar(range(len(league_eff)), league_eff, color=colors, alpha=0.8, edgecolor='black')
ax4.set_xticks(range(len(league_eff)))
ax4.set_xticklabels(league_eff.index, rotation=45, ha='right')
ax4.set_ylabel('Average Efficiency Score', fontweight='bold')
ax4.set_title('Efficiency Score by League', fontweight='bold', fontsize=13)
ax4.axhline(y=50, color='red', linestyle='--', alpha=0.5, label='Average')
ax4.grid(axis='y', alpha=0.3)
ax4.legend()

for bar in bars:
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height + 1,
            f'{height:.1f}', ha='center', va='bottom')

plt.suptitle('League-wise Economic Efficiency Comparison', fontsize=15, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig('results/figures/league_efficiency_comparison.png', dpi=300, bbox_inches='tight')
print("✅ Saved: results/figures/league_efficiency_comparison.png")
plt.close()

print("\n" + "="*80)
print("VISUALIZATION GENERATION COMPLETE!")
print("="*80)
print(f"\nGenerated 2 comprehensive visualization files:")
print("  1. efficiency_dashboard.png - 9-panel comprehensive dashboard")
print("  2. league_efficiency_comparison.png - League-wise analysis")
print("\n" + "="*80)

