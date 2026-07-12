# Acquisition Campaign Measurement & ROI Analytics Framework

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

An end-to-end analytics framework for measuring multi-channel marketing acquisition performance — quantifying ROI, ROAS, CAC, and LTV across Google Ads, Facebook Ads, LinkedIn, Email, Organic Search, Referral, and Affiliate channels, and translating that into budget-allocation recommendations for a SaaS growth team.

---

## 📌 Project Overview

This project simulates a real-world **growth marketing analytics engagement** for a SaaS company. It covers the full lifecycle of a measurement framework: data modeling, SQL analysis, exploratory and statistical analysis in Python, machine learning prediction, and BI dashboarding — delivered the way an analytics team would hand it off to stakeholders.

## 🎯 Business Problem

Marketing spend is distributed across 7 acquisition channels with no unified measurement framework. Leadership cannot answer, with confidence:

- Which channel/campaign delivers the best ROI?
- Which campaigns should get **more** budget — and which should be **paused**?
- Which customer segments, geographies, and devices are most valuable?
- What will next quarter's acquisition trend look like?

## 🎯 Objectives

- Build a reproducible pipeline from raw transactional/campaign data → clean, analysis-ready tables
- Quantify ROI, ROAS, CAC, and LTV at the channel and campaign level
- Validate observed differences statistically (not just descriptively)
- Predict campaign success, revenue, and customer value using ML
- Deliver executive-ready dashboards (Power BI + Tableau specs) and a written recommendation

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Data Generation & ETL | Python, Pandas, NumPy |
| Database / Querying | SQL (PostgreSQL-flavored) — CTEs, window functions, views, stored procedures |
| Statistical Analysis | SciPy, Statsmodels (ANOVA, t-tests, OLS/Logit, confidence intervals) |
| Machine Learning | Scikit-learn (Random Forest, Logistic/Linear Regression, K-Means) |
| Visualization | Matplotlib, Seaborn, Plotly |
| BI Dashboards | Power BI (DAX), Tableau (calculated fields, parameters) |
| Environment | `requirements.txt` / `environment.yml`, config-driven (`config/config.yaml`) |

---

## 🏗️ Architecture

```
                ┌──────────────────┐
                │  Raw CSV Sources   │
                │  campaigns.csv     │
                │  customers.csv     │
                │  transactions.csv  │
                └─────────┬─────────┘
                          │
                          ▼
                ┌──────────────────┐
                │  src/preprocessing │  ← cleaning, validation, feature engineering
                └─────────┬─────────┘
                          │
           ┌──────────────┼───────────────┐
           ▼              ▼               ▼
   ┌───────────────┐ ┌───────────┐ ┌──────────────┐
   │  SQL Analysis  │ │  Python    │ │  ML Models    │
   │  (sql/*.sql)   │ │  Notebooks │ │  (src/model)  │
   └───────┬───────┘ └─────┬─────┘ └──────┬───────┘
           │                │               │
           └────────────────┼───────────────┘
                            ▼
                ┌────────────────────────┐
                │  src/dashboard_metrics  │  ← KPI tables → data/processed
                └───────────┬────────────┘
                            ▼
                ┌────────────────────────┐
                │  Power BI  /  Tableau   │
                │  Executive Dashboards   │
                └────────────────────────┘
```

## 🔄 Project Workflow

1. **Generate / ingest data** — `src/data_loader.py` (synthetic generator used for this portfolio build; swap for a real warehouse connector in production)
2. **Clean & validate** — `01_data_cleaning.ipynb`, `src/preprocessing.py`
3. **Explore** — `02_exploratory_analysis.ipynb`
4. **Analyze ROI** — `03_campaign_roi_analysis.ipynb`, `sql/02_roi_channel_analysis.sql`
5. **Segment customers** — `04_customer_segmentation.ipynb`, `sql/04_customer_segmentation_and_funnel.sql`
6. **Validate statistically** — `05_statistical_testing.ipynb`
7. **Optimize budget** — `06_budget_optimization.ipynb`
8. **Predict with ML** — `07_machine_learning_prediction.ipynb`
9. **Feed BI layer** — `src/dashboard_metrics.py` → `data/processed/*.csv` → Power BI / Tableau

---

## 📂 Dataset Description

| File | Rows | Grain |
|---|---|---|
| `campaigns.csv` | 5,200 | 1 row per campaign |
| `customers.csv` | 5,400 | 1 row per customer |
| `transactions.csv` | 21,500 | 1 row per purchase |
| `monthly_performance.csv` | 245 | 1 row per month × channel |

Full column-level definitions are in [`reports/Data_Dictionary.md`](reports/Data_Dictionary.md).

> Data is synthetically generated (`src/data_loader.py`, seeded for reproducibility) to model realistic channel-level behavior — e.g. Email/Organic/Referral channels carry near-zero marginal cost and outsized ROI, while paid social/search show tighter, more variable margins — mirroring patterns typical of real SaaS acquisition portfolios.

**Entity Relationship Diagram:**

```
customers (1) ──────< transactions >────── (1) campaigns
   customer_id                                campaign_id
   age, gender, country                       channel, budget
   device, segment                            impressions, clicks
   lifetime_value                             revenue, cost, roi
```

---

## 🗄️ SQL Analysis (`/sql`)

| File | Contents |
|---|---|
| `01_schema.sql` | Table DDL, indexes, load statements |
| `02_roi_channel_analysis.sql` | Channel ROI/ROAS/CAC, `RANK()`/`DENSE_RANK()`, performance tiering (`CASE WHEN`), pause candidates, budget recommendation |
| `03_trends_and_moving_averages.sql` | Monthly trend, 3-month rolling average, MoM growth (`LAG`), cumulative revenue |
| `04_customer_segmentation_and_funnel.sql` | Segment/geo/device performance, `NTILE()` quartiles, conversion funnel, value-tier `VIEW` |
| `05_views_and_stored_procedures.sql` | Reusable views for BI, a `PROCEDURE` to refresh a nightly snapshot table, and a refund-flagging `TRIGGER` |

---

## 🐍 Python Analysis (`/notebooks`)

| Notebook | Focus |
|---|---|
| `01_data_cleaning.ipynb` | Validation, integrity checks, cleaning |
| `02_exploratory_analysis.ipynb` | Channel mix, revenue distribution, seasonality |
| `03_campaign_roi_analysis.ipynb` | ROI/ROAS/CAC by channel & campaign, budget recommendation |
| `04_customer_segmentation.ipynb` | K-Means clustering, segment/geo/device performance |
| `05_statistical_testing.ipynb` | t-tests, ANOVA, correlation, OLS/Logit regression, confidence intervals |
| `06_budget_optimization.ipynb` | Revenue forecasting (Holt-Winters), budget-shift simulation |
| `07_machine_learning_prediction.ipynb` | Campaign success classifier, revenue regressor, CLV model — with full evaluation |

All notebooks are pre-executed with real outputs so results are visible directly on GitHub.

## 🤖 Machine Learning

| Model | Task | Result |
|---|---|---|
| Random Forest Classifier | Predict campaign success (ROI > median) | **ROC-AUC ≈ 0.97**, Accuracy ≈ 0.90 |
| Logistic Regression | Same task, linear baseline | Benchmark comparison |
| Random Forest Regressor | Predict campaign revenue | **R² ≈ 0.93**, MAE reported in-notebook |
| Linear Regression | Predict customer LTV | Baseline CLV benchmark |
| K-Means | Customer segmentation (4 clusters) | Surfaces a high-LTV/low-frequency micro-segment |

Evaluated with MAE, RMSE, R², Accuracy, Precision, Recall, F1, ROC-AUC, and Confusion Matrix — see `07_machine_learning_prediction.ipynb`.

## 📊 Statistical Methods

Correlation analysis · Independent t-tests (channel A/B comparison) · One-way ANOVA (channel effect on ROI) · OLS & Logistic regression (ROI/success drivers) · 95% confidence intervals per channel — full detail in `05_statistical_testing.ipynb`.

---

## 📈 Dashboard Screenshots

| Channel ROI | Monthly Revenue Trend |
|---|---|
| ![Channel ROI](images/channel_roi.png) | ![Monthly Revenue](images/monthly_revenue_trend.png) |

| Correlation Matrix | LTV by Country |
|---|---|
| ![Correlation](images/correlation_heatmap.png) | ![Geo LTV](images/geo_ltv.png) |

Full **Power BI** (6 pages, DAX measures) and **Tableau** (6 dashboards, calculated fields, parameters) specifications: [`dashboards/powerbi`](dashboards/powerbi/PowerBI_Dashboard_Spec.md), [`dashboards/tableau`](dashboards/tableau/Tableau_Dashboard_Spec.md).

---

## 📐 KPIs Tracked

CTR · CPC · Conversion Rate · CAC · LTV · ROI · ROAS · Incremental ROI · MoM Revenue Growth · Rolling 3-Month Revenue — formulas in [`reports/Data_Dictionary.md`](reports/Data_Dictionary.md).

## 💡 Business Insights & Recommendations

See the full [`Executive Summary`](reports/Executive_Summary.md). Highlights:

- **Referral, Organic Search, and Email Marketing** deliver the highest ROI, driven by low marginal cost.
- **Google Ads and Facebook Ads** provide necessary top-of-funnel scale but at materially lower ROI — a meaningful subset of individual campaigns are loss-making and are flagged for pause.
- Reallocating ~10% of spend from the lowest- to highest-ROI channel produces a **positive projected profit impact** under current response-rate assumptions (see `06_budget_optimization.ipynb`).
- A distinct high-LTV, low-order-frequency customer cluster is better served by retention/upsell campaigns than broad acquisition spend.

## 🔮 Future Improvements

- Replace last-touch attribution with a proper incrementality/holdout testing framework
- Upgrade the CLV model to a probabilistic BG/NBD + Gamma-Gamma approach
- Connect BI tools to a live warehouse instead of flat-file extracts; automate the nightly stored-procedure refresh

---

## 📁 Folder Structure

```
Acquisition-Campaign-ROI-Analytics/
├── data/
│   ├── raw/                # campaigns.csv, customers.csv, transactions.csv, monthly_performance.csv
│   └── processed/          # cleaned tables + KPI exports for BI
├── notebooks/              # 01–07, pre-executed
├── sql/                    # schema + 4 analysis scripts
├── dashboards/
│   ├── powerbi/             # Power BI spec + DAX
│   └── tableau/             # Tableau spec + calculated fields
├── reports/                 # Data dictionary, executive summary
├── images/                  # Chart exports used in this README
├── src/                     # utils, data_loader, preprocessing, visualization, model, dashboard_metrics
├── config/config.yaml
├── requirements.txt
├── environment.yml
├── LICENSE
└── README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/<your-username>/Acquisition-Campaign-ROI-Analytics.git
cd Acquisition-Campaign-ROI-Analytics

# Option A: pip
pip install -r requirements.txt

# Option B: conda
conda env create -f environment.yml
conda activate acquisition-roi-analytics
```

## ▶️ Usage

```bash
# 1. Generate the synthetic datasets
python -m src.data_loader

# 2. Run the notebooks in order (or open in Jupyter Lab)
jupyter lab notebooks/

# 3. Export KPI tables for the BI layer
python -c "from src.data_loader import load_raw_data; from src.preprocessing import DataPreprocessor; from src.dashboard_metrics import export_all; export_all(DataPreprocessor(load_raw_data()).run_all())"
```

## 📊 Results

- **~$130M** in simulated spend/revenue analyzed across 5,200 campaigns
- **90% accuracy / 0.97 ROC-AUC** predicting campaign success
- **R² ≈ 0.93** predicting campaign revenue
- Concrete, quantified budget-reallocation and pause recommendations delivered in `reports/Executive_Summary.md`

---

## 📄 License

Distributed under the MIT License — see [`LICENSE`](LICENSE) for details.

## 👤 Author

**Akansh** — MCA (AI & ML), Amity University · BCA, Kalinga University
Background in Data Analysis transitioning into AI/ML engineering.
