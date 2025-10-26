"""
Comprehensive Economic Efficiency Analysis
Analyzes efficiency by league, position, fee bracket, age group, and club
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 12)
plt.rcParams['font.size'] = 10

logger.info("="*80)
logger.info("COMPREHENSIVE ECONOMIC EFFICIENCY ANALYSIS")
logger.info("="*80)

# Load data
df = pd.read_csv('data/processed/transfer_efficiency_metrics.csv')

logger.info(f"\nLoaded {len(df)} transfers with efficiency metrics")
logger.info(f"Leagues: {df['league'].unique()}")

# Create results directory
Path('results/figures').mkdir(parents=True, exist_ok=True)

# ============================================================================
# 1. FEE BRACKET ANALYSIS
# ============================================================================
logger.info("\n" + "="*80)
logger.info("1. EFFICIENCY BY FEE BRACKET")
logger.info("="*80)

# Define fee brackets
df['fee_bracket'] = pd.cut(
    df['fee_millions'],
    bins=[0, 1, 5, 10, 20, 50, 200],
    labels=['<€1M', '€1-5M', '€5-10M', '€10-20M', '€20-50M', '>€50M']
)

fee_analysis = df.groupby('fee_bracket').agg({
    'efficiency_score': ['mean', 'median', 'std', 'count'],
    'vfm_score': 'mean',
    'cost_per_goal': 'mean',
    'cost_per_contribution': 'mean',
    'perf_after_goals': 'mean',
    'perf_after_assists': 'mean'
}).round(2)

logger.info("\nEfficiency by Fee Bracket:")
print(fee_analysis)

# ============================================================================
# 2. POSITION ANALYSIS
# ============================================================================
logger.info("\n" + "="*80)
logger.info("2. EFFICIENCY BY POSITION")
logger.info("="*80)

position_analysis = df.groupby('position').agg({
    'efficiency_score': ['mean', 'median', 'count'],
    'vfm_score': 'mean',
    'cost_per_goal': 'mean',
    'fee_millions': 'mean',
    'perf_after_goals': 'mean'
}).round(2)

position_analysis = position_analysis.sort_values(('efficiency_score', 'mean'), ascending=False)
logger.info("\nEfficiency by Position:")
if len(position_analysis) > 0:
    print(position_analysis.head(10))
else:
    logger.warning("No position data available")

# ============================================================================
# 3. LEAGUE ANALYSIS
# ============================================================================
logger.info("\n" + "="*80)
logger.info("3. EFFICIENCY BY LEAGUE")
logger.info("="*80)

league_analysis = df[df['league'] != 'Unknown'].groupby('league').agg({
    'efficiency_score': ['mean', 'median', 'count'],
    'vfm_score': 'mean',
    'cost_per_goal': 'mean',
    'fee_millions': 'mean',
    'perf_after_goals': 'mean'
}).round(2)

league_analysis = league_analysis.sort_values(('efficiency_score', 'mean'), ascending=False)
logger.info("\nEfficiency by League:")
print(league_analysis)

# ============================================================================
# 4. AGE GROUP ANALYSIS
# ============================================================================
logger.info("\n" + "="*80)
logger.info("4. EFFICIENCY BY AGE GROUP")
logger.info("="*80)

df['age_group'] = pd.cut(
    df['age'],
    bins=[0, 21, 24, 27, 30, 100],
    labels=['<21 (Youth)', '21-24 (Young)', '24-27 (Prime)', '27-30 (Experienced)', '30+ (Veteran)']
)

age_analysis = df.groupby('age_group').agg({
    'efficiency_score': ['mean', 'median', 'count'],
    'vfm_score': 'mean',
    'cost_per_goal': 'mean',
    'fee_millions': 'mean',
    'perf_after_goals': 'mean'
}).round(2)

logger.info("\nEfficiency by Age Group:")
print(age_analysis)

# ============================================================================
# 5. SAVE ANALYSIS RESULTS
# ============================================================================
logger.info("\n" + "="*80)
logger.info("SAVING ANALYSIS RESULTS")
logger.info("="*80)

# Save detailed analysis
fee_analysis.to_csv('results/efficiency_by_fee_bracket.csv')
position_analysis.to_csv('results/efficiency_by_position.csv')
league_analysis.to_csv('results/efficiency_by_league.csv')
age_analysis.to_csv('results/efficiency_by_age_group.csv')

logger.info("\n✅ Saved analysis results to results/ directory")

# ============================================================================
# 6. KEY INSIGHTS
# ============================================================================
logger.info("\n" + "="*80)
logger.info("KEY INSIGHTS")
logger.info("="*80)

# Best fee bracket
best_fee_bracket = fee_analysis[('efficiency_score', 'mean')].idxmax()
logger.info(f"\n1. Most efficient fee bracket: {best_fee_bracket}")
logger.info(f"   Average efficiency score: {fee_analysis.loc[best_fee_bracket, ('efficiency_score', 'mean')]:.2f}")

# Best league
if len(league_analysis) > 0:
    best_league = league_analysis[('efficiency_score', 'mean')].idxmax()
    logger.info(f"\n2. Most efficient league: {best_league}")
    logger.info(f"   Average efficiency score: {league_analysis.loc[best_league, ('efficiency_score', 'mean')]:.2f}")

# Best age group
best_age = age_analysis[('efficiency_score', 'mean')].idxmax()
logger.info(f"\n3. Most efficient age group: {best_age}")
logger.info(f"   Average efficiency score: {age_analysis.loc[best_age, ('efficiency_score', 'mean')]:.2f}")

# Best position
if len(position_analysis) > 0:
    best_position = position_analysis[('efficiency_score', 'mean')].idxmax()
    logger.info(f"\n4. Most efficient position: {best_position}")
    logger.info(f"   Average efficiency score: {position_analysis.loc[best_position, ('efficiency_score', 'mean')]:.2f}")

# Correlation analysis
logger.info("\n" + "-"*80)
logger.info("CORRELATION ANALYSIS")
logger.info("-"*80)

correlations = df[['fee_millions', 'age', 'efficiency_score', 'vfm_score', 
                   'perf_after_goals', 'perf_after_assists']].corr()

logger.info("\nCorrelation with Efficiency Score:")
eff_corr = correlations['efficiency_score'].sort_values(ascending=False)
for metric, corr in eff_corr.items():
    if metric != 'efficiency_score':
        logger.info(f"  {metric}: {corr:.3f}")

logger.info("\n" + "="*80)
logger.info("ANALYSIS COMPLETE!")
logger.info("="*80)

