"""
Calculate Economic Efficiency Metrics for Football Transfers
Metrics: VfM Score, Cost-per-Goal, Cost-per-Assist, ROI, Efficiency Score
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info("="*80)
logger.info("CALCULATING ECONOMIC EFFICIENCY METRICS")
logger.info("="*80)

# Load transfer data
df = pd.read_csv('data/raw/transfers_with_performance.csv')
logger.info(f"\nLoaded {len(df)} transfer records")

# Filter to transfers with valid fees (exclude free transfers for efficiency analysis)
df_paid = df[df['fee_millions'] > 0].copy()
logger.info(f"Transfers with fees: {len(df_paid)} ({len(df_paid)/len(df)*100:.1f}%)")

# ============================================================================
# 1. VALUE-FOR-MONEY (VfM) SCORE
# ============================================================================
logger.info("\n" + "-"*80)
logger.info("1. Calculating Value-for-Money (VfM) Score")
logger.info("-"*80)

# Create performance index (normalized 0-100)
# Weighted combination of goals, assists, and minutes
df_paid['performance_index'] = (
    df_paid['perf_after_goals'] * 10 +  # Goals weighted heavily
    df_paid['perf_after_assists'] * 5 +  # Assists weighted moderately
    (df_paid['perf_after_minutes'] / 90) * 0.5  # Minutes as baseline
)

# Normalize to 0-100 scale
perf_min = df_paid['performance_index'].min()
perf_max = df_paid['performance_index'].max()
df_paid['performance_index_normalized'] = (
    (df_paid['performance_index'] - perf_min) / (perf_max - perf_min) * 100
)

# VfM Score: Performance per million euros spent
df_paid['vfm_score'] = df_paid['performance_index_normalized'] / df_paid['fee_millions']

logger.info(f"VfM Score range: {df_paid['vfm_score'].min():.2f} to {df_paid['vfm_score'].max():.2f}")
logger.info(f"VfM Score mean: {df_paid['vfm_score'].mean():.2f}")
logger.info(f"VfM Score median: {df_paid['vfm_score'].median():.2f}")

# ============================================================================
# 2. COST-PER-GOAL
# ============================================================================
logger.info("\n" + "-"*80)
logger.info("2. Calculating Cost-per-Goal")
logger.info("-"*80)

# Filter to players who scored at least 1 goal
df_scorers = df_paid[df_paid['perf_after_goals'] > 0].copy()
df_scorers['cost_per_goal'] = df_scorers['fee_millions'] / df_scorers['perf_after_goals']

logger.info(f"Scorers: {len(df_scorers)} ({len(df_scorers)/len(df_paid)*100:.1f}% of paid transfers)")
logger.info(f"Cost-per-goal range: €{df_scorers['cost_per_goal'].min():.2f}M to €{df_scorers['cost_per_goal'].max():.2f}M")
logger.info(f"Cost-per-goal mean: €{df_scorers['cost_per_goal'].mean():.2f}M")
logger.info(f"Cost-per-goal median: €{df_scorers['cost_per_goal'].median():.2f}M")

# Add back to main dataframe
df_paid['cost_per_goal'] = df_paid.apply(
    lambda row: row['fee_millions'] / row['perf_after_goals'] if row['perf_after_goals'] > 0 else np.nan,
    axis=1
)

# ============================================================================
# 3. COST-PER-ASSIST
# ============================================================================
logger.info("\n" + "-"*80)
logger.info("3. Calculating Cost-per-Assist")
logger.info("-"*80)

df_assisters = df_paid[df_paid['perf_after_assists'] > 0].copy()
df_assisters['cost_per_assist'] = df_assisters['fee_millions'] / df_assisters['perf_after_assists']

logger.info(f"Assisters: {len(df_assisters)} ({len(df_assisters)/len(df_paid)*100:.1f}% of paid transfers)")
logger.info(f"Cost-per-assist range: €{df_assisters['cost_per_assist'].min():.2f}M to €{df_assisters['cost_per_assist'].max():.2f}M")
logger.info(f"Cost-per-assist mean: €{df_assisters['cost_per_assist'].mean():.2f}M")
logger.info(f"Cost-per-assist median: €{df_assisters['cost_per_assist'].median():.2f}M")

df_paid['cost_per_assist'] = df_paid.apply(
    lambda row: row['fee_millions'] / row['perf_after_assists'] if row['perf_after_assists'] > 0 else np.nan,
    axis=1
)

# ============================================================================
# 4. COST-PER-GOAL-CONTRIBUTION
# ============================================================================
logger.info("\n" + "-"*80)
logger.info("4. Calculating Cost-per-Goal-Contribution")
logger.info("-"*80)

df_paid['goal_contribution_after'] = df_paid['perf_after_goals'] + df_paid['perf_after_assists']
df_contributors = df_paid[df_paid['goal_contribution_after'] > 0].copy()
df_contributors['cost_per_contribution'] = (
    df_contributors['fee_millions'] / df_contributors['goal_contribution_after']
)

logger.info(f"Contributors: {len(df_contributors)} ({len(df_contributors)/len(df_paid)*100:.1f}%)")
logger.info(f"Cost-per-contribution range: €{df_contributors['cost_per_contribution'].min():.2f}M to €{df_contributors['cost_per_contribution'].max():.2f}M")
logger.info(f"Cost-per-contribution mean: €{df_contributors['cost_per_contribution'].mean():.2f}M")
logger.info(f"Cost-per-contribution median: €{df_contributors['cost_per_contribution'].median():.2f}M")

df_paid['cost_per_contribution'] = df_paid.apply(
    lambda row: row['fee_millions'] / row['goal_contribution_after'] if row['goal_contribution_after'] > 0 else np.nan,
    axis=1
)

# ============================================================================
# 5. EFFICIENCY SCORE (Composite Metric)
# ============================================================================
logger.info("\n" + "-"*80)
logger.info("5. Calculating Composite Efficiency Score")
logger.info("-"*80)

# Normalize all metrics to 0-100 scale (higher is better)
# For cost metrics, invert so lower cost = higher score

# VfM already normalized (higher is better)
vfm_normalized = (df_paid['vfm_score'] - df_paid['vfm_score'].min()) / (df_paid['vfm_score'].max() - df_paid['vfm_score'].min()) * 100

# Cost-per-goal (invert: lower cost is better)
cpg_valid = df_paid['cost_per_goal'].dropna()
if len(cpg_valid) > 0:
    cpg_normalized = 100 - ((df_paid['cost_per_goal'] - cpg_valid.min()) / (cpg_valid.max() - cpg_valid.min()) * 100)
else:
    cpg_normalized = pd.Series([50] * len(df_paid))

# Cost-per-contribution (invert: lower cost is better)
cpc_valid = df_paid['cost_per_contribution'].dropna()
if len(cpc_valid) > 0:
    cpc_normalized = 100 - ((df_paid['cost_per_contribution'] - cpc_valid.min()) / (cpc_valid.max() - cpc_valid.min()) * 100)
else:
    cpc_normalized = pd.Series([50] * len(df_paid))

# Composite efficiency score (weighted average)
df_paid['efficiency_score'] = (
    vfm_normalized * 0.4 +  # 40% weight on VfM
    cpg_normalized.fillna(50) * 0.3 +  # 30% weight on cost-per-goal
    cpc_normalized.fillna(50) * 0.3  # 30% weight on cost-per-contribution
)

logger.info(f"Efficiency Score range: {df_paid['efficiency_score'].min():.2f} to {df_paid['efficiency_score'].max():.2f}")
logger.info(f"Efficiency Score mean: {df_paid['efficiency_score'].mean():.2f}")
logger.info(f"Efficiency Score median: {df_paid['efficiency_score'].median():.2f}")

# ============================================================================
# 6. EFFICIENCY CATEGORIES
# ============================================================================
logger.info("\n" + "-"*80)
logger.info("6. Categorizing Transfer Efficiency")
logger.info("-"*80)

# Define efficiency categories based on efficiency score
def categorize_efficiency(score):
    if pd.isna(score):
        return 'Unknown'
    elif score >= 80:
        return 'Excellent'
    elif score >= 60:
        return 'Good'
    elif score >= 40:
        return 'Average'
    elif score >= 20:
        return 'Poor'
    else:
        return 'Very Poor'

df_paid['efficiency_category'] = df_paid['efficiency_score'].apply(categorize_efficiency)

category_counts = df_paid['efficiency_category'].value_counts()
logger.info("\nEfficiency Distribution:")
for category, count in category_counts.items():
    logger.info(f"  {category}: {count} ({count/len(df_paid)*100:.1f}%)")

# ============================================================================
# 7. SAVE RESULTS
# ============================================================================
logger.info("\n" + "="*80)
logger.info("SAVING RESULTS")
logger.info("="*80)

# Create output directory
Path('data/processed').mkdir(parents=True, exist_ok=True)

# Get position from position indicators
if 'is_forward' in df_paid.columns:
    df_paid['position'] = 'Unknown'
    df_paid.loc[df_paid['is_forward'] == 1, 'position'] = 'Forward'
    df_paid.loc[df_paid['is_midfielder'] == 1, 'position'] = 'Midfielder'
    df_paid.loc[df_paid['is_defender'] == 1, 'position'] = 'Defender'
    df_paid.loc[df_paid['is_goalkeeper'] == 1, 'position'] = 'Goalkeeper'

# Get league from league dummies
league_cols = [c for c in df_paid.columns if c.startswith('league_')]
if league_cols:
    df_paid['league'] = 'Unknown'
    for col in league_cols:
        league_name = col.replace('league_', '')
        df_paid.loc[df_paid[col] == 1, 'league'] = league_name

# Select relevant columns for efficiency analysis
efficiency_cols = [
    'player_name', 'club_name', 'position', 'age', 'season',
    'fee_millions', 'perf_after_goals', 'perf_after_assists',
    'perf_after_minutes', 'goal_contribution_after',
    'performance_index', 'performance_index_normalized',
    'vfm_score', 'cost_per_goal', 'cost_per_assist', 'cost_per_contribution',
    'efficiency_score', 'efficiency_category', 'league'
]

# Filter to available columns
available_cols = [col for col in efficiency_cols if col in df_paid.columns]
df_efficiency = df_paid[available_cols].copy()

# Save to CSV
output_path = 'data/processed/transfer_efficiency_metrics.csv'
df_efficiency.to_csv(output_path, index=False)
logger.info(f"\n✅ Saved efficiency metrics to: {output_path}")
logger.info(f"   Records: {len(df_efficiency)}")
logger.info(f"   Columns: {len(df_efficiency.columns)}")

# Save summary statistics
summary_stats = {
    'total_transfers': len(df_paid),
    'avg_fee': df_paid['fee_millions'].mean(),
    'median_fee': df_paid['fee_millions'].median(),
    'avg_vfm_score': df_paid['vfm_score'].mean(),
    'avg_cost_per_goal': df_paid['cost_per_goal'].mean(),
    'avg_cost_per_contribution': df_paid['cost_per_contribution'].mean(),
    'avg_efficiency_score': df_paid['efficiency_score'].mean(),
    'excellent_transfers': len(df_paid[df_paid['efficiency_category'] == 'Excellent']),
    'good_transfers': len(df_paid[df_paid['efficiency_category'] == 'Good']),
    'poor_transfers': len(df_paid[df_paid['efficiency_category'] == 'Poor'])
}

import json
with open('results/efficiency_summary.json', 'w') as f:
    json.dump(summary_stats, f, indent=2)

logger.info(f"\n✅ Saved summary statistics to: results/efficiency_summary.json")

# Print top 10 most efficient transfers
logger.info("\n" + "="*80)
logger.info("TOP 10 MOST EFFICIENT TRANSFERS")
logger.info("="*80)

top_10 = df_efficiency.nlargest(10, 'efficiency_score')[
    ['player_name', 'club_name', 'fee_millions', 'perf_after_goals', 
     'perf_after_assists', 'efficiency_score', 'efficiency_category']
]

for idx, row in top_10.iterrows():
    logger.info(f"\n{row.name + 1}. {row['player_name']} → {row['club_name']}")
    logger.info(f"   Fee: €{row['fee_millions']:.1f}M | Goals: {row['perf_after_goals']:.0f} | Assists: {row['perf_after_assists']:.0f}")
    logger.info(f"   Efficiency Score: {row['efficiency_score']:.2f} ({row['efficiency_category']})")

logger.info("\n" + "="*80)
logger.info("EFFICIENCY METRICS CALCULATION COMPLETE!")
logger.info("="*80)

