# Evaluating Economic Efficiency in Football Transfers: A Data-Driven Approach

## 📋 Project Overview

This project analyzes the economic efficiency of football transfers by measuring the relationship between transfer fees and player contributions. Using advanced analytical methods including regression analysis and Data Envelopment Analysis (DEA), we evaluate whether clubs are getting value for money in their transfer investments.

## 🎯 Research Objective

**Main Question:** How economically efficient are football transfers? Are clubs paying fair prices for the performance they receive?

**Core Concept:** Economic efficiency measures how well a club optimizes the sporting and financial returns from a transfer relative to the cost paid.

In simpler terms: **"Was this player worth the money?"** - answered scientifically.

## 💰 Economic Efficiency Framework

### A. Cost Side (Input)

| Input Factor | Description | Unit |
|--------------|-------------|------|
| **Transfer Fee** | Initial acquisition cost | € (Euros) |
| **Salary + Bonuses** | Annual compensation | € per year |
| **Contract Duration** | Length of commitment | Years |
| **Player Age** | Age at transfer | Years (affects long-term investment potential) |

### B. Return Side (Output)

| Output Factor | Description | Measurement |
|---------------|-------------|-------------|
| **Performance Contribution** | Goals, assists, match ratings | Statistical metrics |
| **Team Ranking/Points Improvement** | Impact on team success | League position change, points gained |
| **Market Value Increase** | Player's value appreciation | € change |
| **Club Revenue Growth** | Financial returns | UEFA bonuses, merchandise sales, etc. |

## 📊 Measurement Methods

### 1. Value-for-Money (VfM) Score

**Formula:**

```
VfM = Performance Index / Total Cost
```

**Interpretation:** Performance contribution per € spent

**Example:** "For every €1 million in transfer fees, the player contributed 0.8 goals"

**Normalization:** Performance metrics are normalized to create a comparable index across different positions and leagues.

### 2. Regression Analysis

**Model Structure:**

```
Dependent Variable = Performance Contribution (goals, assists, points contribution)
Independent Variables = Transfer fee, salary, age, position, league level
```

**Purpose:**
- Predict "expected contribution" based on investment
- Compare actual vs expected performance
- Identify **over-valued** and **under-valued** transfers

**Output Example:**
- Expected contribution: 15 goals
- Actual contribution: 22 goals
- **Result:** Under-valued transfer (good deal)

### 3. Data Envelopment Analysis (DEA)

**What is DEA?**
A non-parametric method for evaluating the relative efficiency of decision-making units (DMUs).

**Application to Transfers:**
- **DMU:** Individual transfers or clubs
- **Inputs:** Transfer cost, salary, player age
- **Outputs:** Performance metrics, market value increase

**Efficiency Score:** Ranges from 0 to 1
- **1.0 = Fully efficient** (on the efficiency frontier)
- **< 1.0 = Inefficient** (could achieve better output with same input)

**Advantages:**
- Handles multiple inputs and outputs simultaneously
- No need to specify functional form
- Identifies best practices (benchmark transfers)

## 🔬 Analytical Approach

### Phase 1: Data Collection
- Transfer fees from multiple seasons
- Player performance statistics (pre and post-transfer)
- Salary information
- Team performance metrics
- Market value changes

### Phase 2: Performance Index Construction
Create normalized performance indices considering:
- Position-specific metrics (e.g., goals for forwards, clean sheets for defenders)
- Minutes played weighting
- Team context (league strength, team quality)

### Phase 3: Economic Efficiency Calculation

**Method A: VfM Ratio**
```python
vfm_score = (normalized_performance_index / total_cost) * 1_000_000
```

**Method B: Regression Residuals**
```python
expected_performance = model.predict(transfer_features)
efficiency = actual_performance - expected_performance
```

**Method C: DEA Efficiency**
```python
efficiency_score = DEA(inputs=[cost, age], outputs=[performance, value_increase])
```

### Phase 4: Comparative Analysis
- Identify most/least efficient transfers
- Compare efficiency across leagues, positions, and clubs
- Temporal trends in transfer efficiency

## 🤖 Technical Implementation

### Machine Learning Models

1. **Linear Regression:** Baseline model for cost-performance relationship
2. **Random Forest Regression:** Capture non-linear relationships
3. **Gradient Boosting (XGBoost):** Advanced predictive modeling
4. **DEA (PuLP/PyDEA):** Efficiency frontier analysis

### Key Performance Indicators (KPIs)

```python
# Performance Index Components
performance_index = weighted_sum([
    goals_per_90,
    assists_per_90,
    xG_per_90,
    average_rating,
    minutes_played_ratio,
    team_points_contribution
])

# Economic Efficiency Metrics
efficiency_metrics = {
    'vfm_score': performance_index / total_cost,
    'cost_per_goal': transfer_fee / total_goals,
    'cost_per_point': transfer_fee / points_contributed,
    'roi_percentage': (market_value_increase - total_cost) / total_cost * 100
}
```

## 🔧 Technical Stack

- **Programming Language:** Python 3.11+
- **Data Collection:** Web scraping (BeautifulSoup, Selenium), APIs
- **Data Processing:** Pandas, NumPy
- **Statistical Analysis:** SciPy, Statsmodels
- **Machine Learning:** Scikit-learn, XGBoost
- **DEA Analysis:** PuLP, PyDEA
- **Visualization:** Matplotlib, Seaborn, Plotly

## 📁 Project Structure

```
transfer-economic-efficiency/
├── data/
│   ├── raw/                 # Raw transfer and performance data
│   ├── processed/           # Cleaned datasets
│   └── efficiency_scores/   # Calculated efficiency metrics
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_performance_index.ipynb
│   ├── 04_vfm_analysis.ipynb
│   ├── 05_regression_analysis.ipynb
│   └── 06_dea_analysis.ipynb
├── src/
│   ├── data_collection/     # Scraping scripts
│   ├── preprocessing/       # Data cleaning
│   ├── efficiency/          # Efficiency calculation methods
│   ├── models/              # Regression models
│   └── dea/                 # DEA implementation
├── results/
│   ├── figures/             # Visualizations
│   ├── reports/             # Analysis reports
│   └── rankings/            # Efficiency rankings
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### Prerequisites

```bash
python >= 3.11
pip install -r requirements.txt
```

### Installation

```bash
git clone https://github.com/mehmetyalc/transfer-economic-efficiency.git
cd transfer-economic-efficiency
pip install -r requirements.txt
```

### Usage

1. **Data Collection:** Run scraping scripts in `src/data_collection/`
2. **Preprocessing:** Clean and prepare data using notebooks 01-02
3. **Efficiency Analysis:** Execute analysis notebooks 03-06
4. **Results:** View efficiency rankings and visualizations in `results/`

## 📈 Expected Outcomes

- **Efficiency Rankings:** List of most/least efficient transfers
- **Value-for-Money Scores:** Quantitative assessment of transfer value
- **Predictive Models:** Forecast expected performance based on investment
- **Best Practice Identification:** Benchmark transfers for clubs to emulate
- **Strategic Insights:** Data-driven recommendations for transfer strategy

## 💡 Use Cases

### For Football Clubs
- **Transfer Strategy:** Identify market inefficiencies
- **Budget Allocation:** Optimize spending across positions
- **Negotiation:** Data-backed valuation for transfer targets

### For Analysts & Researchers
- **Market Analysis:** Study transfer market trends
- **Comparative Studies:** Cross-league efficiency comparisons
- **Academic Research:** Empirical evidence for football economics

### For Fans & Media
- **Transfer Evaluation:** Assess club's transfer business
- **Player Valuation:** Understand fair market prices

## 📚 Data Sources

- [Transfermarkt](https://www.transfermarkt.com/) - Transfer fees and market values
- [FBref](https://fbref.com/) - Advanced statistics
- [Capology](https://www.capology.com/) - Salary information
- [WhoScored](https://www.whoscored.com/) - Player ratings

## 📖 Theoretical Background

This project draws on:
- **Sports Economics:** Transfer market efficiency theory
- **Operations Research:** DEA methodology
- **Performance Analytics:** Player valuation models
- **Financial Analysis:** ROI and cost-benefit analysis

### Key References
- Farrell, M.J. (1957). "The Measurement of Productive Efficiency"
- Charnes, A., Cooper, W.W., & Rhodes, E. (1978). "Measuring the efficiency of decision making units"
- Carmichael, F., & Thomas, D. (2005). "Production and efficiency in team sports: An investigation of rugby league football"

## 🤝 Contributing

Contributions are welcome! Areas for contribution:
- Additional data sources
- Alternative efficiency metrics
- Advanced modeling techniques
- Visualization improvements

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact

For questions, collaboration, or suggestions, please open an issue or contact the repository owner.

## 🔗 Related Projects

- [Football Transfer Success Prediction](https://github.com/mehmetyalc/transfer-success-prediction)

---

**Disclaimer:** This is an academic research project. Results should complement, not replace, professional scouting and expert judgment in transfer decisions.

