# Customer Churn Analysis & Retention Intelligence Dashboard (TeleConnect)

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Interactive_Web_Dashboard-10B981?style=for-the-badge&logo=googlechrome&logoColor=white)](https://yash930596.github.io/churn-analysis/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-1.5+-150458?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![SQL](https://img.shields.io/badge/SQL-PostgreSQL%20%2F%20MySQL-4169E1?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Power BI](https://img.shields.io/badge/Power_BI-Dashboard_Spec-F2C94C?style=flat&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)

An end-to-end data analytics portfolio project investigating subscription customer churn, quantifying annualized revenue at risk, constructing a 4-quadrant customer risk matrix, and delivering data-driven retention strategies for a telecommunications provider called **TeleConnect**.

---

## 🌐 Live Interactive Dashboard Demo
Click below to open and interact with the live deployed dashboard in your browser (no installation required):

👉 **[Launch Live Web Dashboard](https://yash930596.github.io/churn-analysis/)**

---

## 📌 Project Overview
**TeleConnect** provides high-speed internet, mobile, streaming, and landline phone services to subscription customers. Executive leadership noticed an increasing rate of account cancellations and requested a comprehensive analytical audit to understand:
1. **Who is churning?** (Demographics, contract types, tenure cohorts)
2. **Why are they churning?** (Pricing, technical support friction, competitor offers, CSAT)
3. **What is the financial impact?** (Monthly recurring revenue and annualized revenue at risk)
4. **How can TeleConnect retain vulnerable accounts?** (Targeted intervention campaigns)

---

## 🛠️ Tools & Technologies
- **Live Web App Host**: GitHub Pages ([Live App Link](https://yash930596.github.io/churn-analysis/))
- **Data Generation & Cleaning**: Python (`pandas`, `numpy`)
- **Exploratory Visual Analytics**: Python (`matplotlib`, `seaborn`)
- **Database & Querying**: PostgreSQL / MySQL (`DDL Schema`, `Validation Queries`, `20 Advanced Analytical Queries`)
- **BI Reporting Specification**: Power BI (`3-Page Dashboard Blueprint`, `DAX Measures Specification`)
- **Documentation**: Data Dictionary, Executive Insights Report, 20 Interview Q&As, Resume Portfolio Summary

---

## 📊 Key Baseline Metrics
- **Total Customers**: 10,000
- **Active Customers**: 7,121 (**71.21%**)
- **Churned Customers**: 2,879 (**28.79%** Baseline Churn Rate)
- **Average Monthly Charge**: **$62.74**
- **Average Customer Tenure**: **22.55 Months**
- **Annualized Revenue at Risk**: **$2,220,133.56** (**29.49%** of ARR)

---

## 📂 Project Structure
```
customer-churn-analysis/
├── README.md                           # Repository Overview & Live Demo Link
├── requirements.txt                    # Python Dependencies
├── index.html                          # Live Web Dashboard Application
├── styles.css                          # Custom Glassmorphism UI Styling
├── app.js                             # Interactive Dashboard Logic & Chart.js Visuals
│
├── data/
│   ├── raw/
│   │   └── customers.csv               # Raw Synthetic Dataset (10,000 records + quality flaws)
│   └── processed/
│       └── customers_clean.csv         # Cleaned & Feature-Engineered Dataset
│
├── src/
│   ├── data_generation.py              # Reproducible Data Generation Script (seed=42)
│   ├── data_cleaning.py                # Reproducible Cleaning & Derived Variable Pipeline
│   ├── eda.py                          # Visual Analytics & Chart Generation Script
│   └── churn_analysis.py               # Statistical Summary & Customer Segmentation Engine
│
├── sql/
│   ├── 01_schema.sql                   # Database DDL Schema (PostgreSQL/MySQL)
│   ├── 02_data_validation.sql          # Data Quality Audit Scripts
│   └── 03_churn_analysis.sql           # 20 Analytical SQL Queries (CTEs, Window Functions)
│
├── docs/
│   ├── data_dictionary.md              # Complete Feature Schema & Data Dictionary
│   ├── business_insights.md            # Executive Insights Report & Recommendations
│   ├── powerbi_measures.md             # Power BI DAX Measures Specification
│   ├── project_documentation.md        # Full End-to-End Technical Narrative
│   ├── interview_questions.md          # 20 Interview Q&As with Sample Answers
│   └── portfolio_description.md        # Resume Bullets & LinkedIn/GitHub Summaries
│
├── outputs/
│   ├── charts/                         # 10 High-Res PNG Visual Analytics Charts
│   └── reports/                        # JSON Summary Metrics & Analytical Outputs
│
└── powerbi/
    └── dashboard_specification.md      # 3-Page Power BI Canvas Specification & Wireframes
```

---

## 📊 Key Analytical Findings
1. **Overall Churn Rate**: **28.79%** of total accounts have cancelled, placing over **$2.22M in estimated annualized revenue at risk**.
2. **Contract Type Impact**: **Month-to-month subscribers** churn at **35.71%**, compared to **22.31%** for 1-year contracts and **17.68%** for 2-year contracts.
3. **Tenure Vulnerability**: Over **53% of churn** occurs within the first 12 months of service (`0–6 Months` and `7–12 Months`).
4. **Support Ticket Threshold**: Customers filing **6 or more support tickets** display a churn rate of **46.53%**.
5. **Competitor & Price Pressure**: Premium subscribers facing competitor counter-offers and high monthly charges (>$80/mo) represent the largest high-value churn segment.

---

## 🎯 Strategic Business Recommendations
1. **Contract Migration Incentives**: Offer a 10% annual discount or 6 months of free streaming for month-to-month customers upgrading to 12-month contracts.
2. **First-Year Onboarding Sequence**: Proactive CSAT and support check-ins at Day 14, 45, and 90 for new subscribers.
3. **High-Ticket Proactive Escalation**: Automated CRM workflow routing accounts reaching their 3rd support ticket to Senior Customer Success specialists.
4. **Competitor Price Matching**: Flexible retention counter-offer toolkits for Fiber Optic accounts targeted by competitor offers.

---

## 🚀 How to Run the Project Locally

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/yash930596/churn-analysis.git
cd churn-analysis
pip install -r requirements.txt
```

### 2. Generate & Clean Data
```bash
python src/data_generation.py
python src/data_cleaning.py
```

### 3. Run Visual Analytics & Statistical Analysis
```bash
python src/eda.py
python src/churn_analysis.py
```

---

## 💡 Skills Demonstrated
- **Full Web App Deployment**: GitHub Pages live demo hosting.
- **Data Engineering**: Data generation, deduplication, missing value imputation, outlier handling, categorical standardization.
- **SQL Analytics**: DDL schema design, indexes, CTEs, Window Functions (`RANK()`, `ROW_NUMBER()`), conditional aggregations (`CASE WHEN`).
- **Data Visualization**: Publication-quality Seaborn/Matplotlib charts and Power BI 3-page canvas design.
- **Business Acumen**: Revenue-at-risk modeling, 4-quadrant customer segmentation matrix, executive storytelling, actionable recommendations.
