# E-Commerce Customer Retention & Churn Diagnostic Suite

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B.svg)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-7.1+-3F4F75.svg)](https://plotly.com)
[![Kaggle Datasets](https://img.shields.io/badge/Kaggle-Real%20Data-20BEFF.svg)](https://kaggle.com)
[![Tableau Public](https://img.shields.io/badge/Tableau-1200x800-E97627.svg)](https://public.tableau.com)
[![Power BI](https://img.shields.io/badge/Power%20BI-DAX%20Model-F2C811.svg)](https://powerbi.microsoft.com)

A comprehensive, enterprise-ready data analytics portfolio project designed to showcase deep expertise in **longitudinal cohort retention**, **promotional elasticity modeling**, **predictive churn classification**, and **conversational business intelligence web integration**.

---

## 🌟 Project Deliverables Overview

1. **Relational Data Pipeline & Modeling**:
   - Ingests real-world Kaggle datasets (**Brazilian E-Commerce Olist** with 96k+ orders & **E-Commerce Customer Churn** with 5.6k customer records).
   - Generates production-clean relational tables (`customers.csv`, `orders.csv`, `churn_logs.csv`).
   - Production SQL scripts calculating **Monthly Cohort Retention**, **Historical & Predictive LTV**, and **RFM Quintile Churn Risk Scoring** (`sql/`).
   - Power Query (M) scripts for Power BI desktop modeling (`sql/power_query_m.txt`).

2. **Executive BI Dashboard (Tableau & Power BI)**:
   - Full specification and calculation formulas for Tableau LOD expressions and Power BI DAX (`dashboard/`).
   - Standardized fixed **1200 x 800** canvas resolution with responsive CSS aspect ratio container, loading states, and fullscreen modal toggle (`dashboard/iframe_embed.html`).

3. **Conversational Analytics Web App ("Chat with Data")**:
   - Streamlit interactive application featuring a **"Chat with your Retention Data"** natural language query engine (`app/streamlit_app.py`).
   - Generates dynamic, interactive Plotly visualizations (Heatmaps, Dual-Axis Elasticity Curves, Category Matrices) in real time.
   - Dual-mode architecture: Works with OpenAI / LangChain API or seamlessly offline via built-in deterministic analytical query router.

4. **Web Portfolio Integration Suite**:
   - Modern React + Tailwind CSS component (`portfolio_component/RetentionSuiteWidget.jsx`) ready to drop into Next.js, Vite, or Gatsby.
   - Standalone live HTML preview page (`portfolio_component/index.html`) using Tailwind CDN.
   - Complete Executive Case Study & PDF writeup (`portfolio_component/case_study_summary.md`).

---

## 📁 Repository Structure

```
project/
├── data/                               # Real Kaggle Relational Dataset (Exported)
│   ├── customers.csv                   # 93,104 unique customers, LTV, segment, tenure
│   ├── orders.csv                      # 96,211 delivered orders, categories, margins, discounts
│   ├── churn_logs.csv                  # 75,031 customer churn events & risk scores
│   ├── churn_ml_dataset.csv            # 5,630 Kaggle ML feature records
│   ├── feature_importance.csv          # Random Forest feature rankings
│   └── high_risk_customers_drilldown.csv # Top prioritized intervention targets
│
├── src/                                # Core Python Analytics & ML Pipeline
│   ├── kaggle_importer.py              # Ingestion & ETL pipeline for real Kaggle data
│   ├── churn_model.py                  # Random Forest ML model (0.976 AUC) & LTV engine
│   ├── analytics_engine.py             # Cohort matrix, elasticity curves, category diagnostics
│   └── chat_engine.py                  # Conversational NLP & Plotly visual router
│
├── sql/                                # Production SQL & Power Query Assets
│   ├── cohort_retention.sql            # Window functions for 12-month cohort retention matrix
│   ├── customer_ltv.sql                # Historical & predictive Customer Lifetime Value
│   ├── churn_risk_scoring.sql          # RFM quintile scoring & 0-100 risk index
│   └── power_query_m.txt               # Power Query (M) transformations for Power BI
│
├── dashboard/                          # BI Dashboard Blueprints & Embed Containers
│   ├── tableau_spec.md                 # Tableau LOD calculations, sheet hierarchy & parameters
│   ├── powerbi_dax.md                  # Power BI DAX measures library & star schema
│   └── iframe_embed.html               # 1200x800 responsive iframe embed with spinner & fullscreen
│
├── app/                                # Streamlit Web Application
│   ├── streamlit_app.py                # Executive KPI dashboard & "Chat with Data" UI
│   └── requirements.txt                # Streamlit cloud dependencies
│
├── portfolio_component/                # Web Portfolio Integration
│   ├── RetentionSuiteWidget.jsx        # Production React + Tailwind CSS portfolio component
│   ├── index.html                      # Standalone HTML preview page (Tailwind CDN)
│   └── case_study_summary.md           # Executive Portfolio Case Study & PDF writeup
│
└── README.md                           # Documentation & quickstart guide
```

---

## 🚀 Quickstart Guide

### 1. Environment Setup
```bash
# Clone or navigate to the directory
cd "c:/Users/RARCH/Desktop/data analytics/project"

# Ensure dependencies are installed
pip install -r app/requirements.txt
```

### 2. Ingest Real Data & Train ML Models (Optional - Already Pre-Computed)
```bash
# Run Kaggle ETL pipeline
python src/kaggle_importer.py

# Run Random Forest predictive churn model & LTV engine
python src/churn_model.py

# Verify analytical calculations
python src/analytics_engine.py
```

### 3. Launch the Streamlit "Chat with Data" Web App
```bash
streamlit run app/streamlit_app.py
```
*Access the interactive interface locally at `http://localhost:8501`.*

### 4. Preview the Web Portfolio Integration
Open `portfolio_component/index.html` in any browser to inspect the responsive 1200x800 BI embed, metric summary cards, and case study overview.

---

## 📊 Key Executive Findings

| Metric | Analyzed Value | Strategic Takeaway |
| :--- | :--- | :--- |
| **Tracked Revenue** | **$12.88 Million** | 96,211 delivered orders across 20 months of operations. |
| **Active Retention Rate** | **19.4%** | Baseline active customer base (18,073 customers). |
| **Repeat Buyer LTV Multiplier** | **3.8x** | Customers who purchase in Month 1 generate $310.47 in LTV vs $138.51 for single-order dropouts. |
| **Optimal Discount Cap** | **12% - 15%** | Discounts above 15% do not reduce churn (flat at ~82%), while customer gross profit drops by 95% (from $146.80 to $7.28). |
| **Predictive Churn AUC** | **0.976** | Random Forest model detects early churn signals (Tenure, Discount Dependency, Complaints, and Transit Delays). |
| **Reclaim Opportunity** | **$1.33 Million** | Annual revenue recovered by achieving a 12.8% winback of at-risk customers. |

---

## 💼 Portfolio Embedding Instructions

### In React / Next.js
Copy `portfolio_component/RetentionSuiteWidget.jsx` into your project's `components/` directory:
```jsx
import RetentionSuiteWidget from '@/components/RetentionSuiteWidget';

export default function PortfolioPage() {
  return (
    <main>
      <RetentionSuiteWidget />
    </main>
  );
}
```

### In Webflow / WordPress / Static HTML
Embed the code from `portfolio_component/index.html` or `dashboard/iframe_embed.html` into a custom HTML embed block. Ensure container dimensions respect `aspect-ratio: 1200 / 800`.
