# TeleConnect Customer Churn Analysis & Retention Intelligence — End-to-End Project Documentation

## 1. Executive Summary & Introduction
**TeleConnect** is a nationwide telecommunications service provider delivering high-speed internet, mobile, streaming, and landline services to subscription customers. Over recent quarters, executive leadership observed an unsettling uptick in customer cancellations (churn), leading to lost recurring revenue and increased customer acquisition costs (CAC).

This portfolio project provides a comprehensive, end-to-end analytical solution designed to identify **who is churning**, **why they are leaving**, **what revenue is at risk**, and **how TeleConnect can strategically retain high-value accounts**.

---

## 2. Business Context & Strategic Objectives
Retaining existing subscription customers is significantly more cost-effective than acquiring new ones in the saturated telecom market. Management set out the following core operational objectives:

1. **Quantify Baseline Churn Metrics**: Establish overall churn rate, active customer counts, and annualized revenue at risk.
2. **Identify Primary Risk Drivers**: Pinpoint the relationship between churn and contract types, service tiers, tenure cohorts, payment methods, customer support tickets, and CSAT scores.
3. **Isolate Vulnerable Customer Segments**: Construct a 4-quadrant Customer Value / Churn Risk matrix to prioritize retention efforts.
4. **Deliver Executive & Operational Intelligence**: Provide interactive Power BI dashboards, reproducible data cleaning pipelines, and automated SQL analysis.

---

## 3. Business Questions Answered
- What is TeleConnect's overall churn rate and total annualized revenue lost?
- Do customers on month-to-month contracts churn at a higher rate than long-term contract holders?
- Does customer tenure mitigate churn risk?
- How does support interaction frequency (tickets and complaints) correlate with customer departure?
- Which subscription plans and payment methods present the highest churn vulnerability?
- What actionable strategies can reduce churn among high-value accounts?

---

## 4. Dataset Architecture & Design
The project utilizes a synthetic dataset of **10,000 customer records** (`data/raw/customers.csv`) built using Python (`pandas`, `numpy`) with a fixed seed (`seed=42`) for 100% reproducibility.

The dataset includes 36 core variables spanning 6 domains:
- **Demographics**: `customer_id`, `gender`, `age`, `senior_citizen`, `marital_status`, `dependents`, `city`, `state`.
- **Subscriptions**: `signup_date`, `tenure_months`, `contract_type`, `subscription_plan`, `internet_service`, `payment_method`, `paperless_billing`.
- **Financials**: `monthly_charges`, `total_charges`, `discount_percentage`, `lifetime_value`.
- **Services**: `phone_service`, `multiple_lines`, `streaming_service`, `online_security`, `online_backup`, `tech_support`, `device_protection`.
- **Engagement**: `support_tickets`, `complaints`, `avg_monthly_usage_gb`, `satisfaction_score`, `last_login_days_ago`.
- **Churn Target**: `churn`, `churn_date`, `churn_reason`, `competitor_offer`, `cancellation_channel`.

---

## 5. Data Quality Auditing & Cleaning Pipeline
Raw production data inevitably suffers from anomalies. To simulate real-world data engineering challenges, intentional flaws were injected into `customers.csv`:
- ~20 duplicate customer IDs.
- ~1.5% missing values in `total_charges`, `satisfaction_score`, and `internet_service`.
- Non-standard formatting (e.g. `' Month-to-month '`, `'dsl'`, `'electronic check'`).
- Extreme numeric outliers (negative charges, unrealistic ages).

### Reproducible Cleaning Steps (`src/data_cleaning.py`)
1. **Deduplication**: Filtered duplicate `customer_id` records.
2. **String Standardization**: Stripped leading/trailing whitespace and normalized all categorical variables to Title Case.
3. **Missing Value Imputation**:
   - `total_charges`: Imputed via `monthly_charges * tenure_months`.
   - `satisfaction_score`: Imputed using median CSAT per contract group.
   - `internet_service`: Defaulted missing values to `'DSL'`.
4. **Outlier Capping**: Cleaned invalid ages (<18 or >85 mapped to median 45) and monthly charges (<$18 or >$150 capped to standard median).
5. **Feature Engineering**: Engineered derived cohorts: `age_group`, `tenure_group`, `monthly_charge_group`, `support_ticket_group`, `satisfaction_group`, `customer_status`, `estimated_annual_revenue`, `estimated_revenue_at_risk`.
6. Output saved to `data/processed/customers_clean.csv`.

---

## 6. SQL Analytical Suite
A complete 3-file SQL repository was created under `sql/`:
- `01_schema.sql`: DDL schema for PostgreSQL/MySQL with primary key constraints, field data types, and index optimizations on `churn`, `contract_type`, and `tenure_months`.
- `02_data_validation.sql`: Automated data quality verification queries.
- `03_churn_analysis.sql`: 20 advanced SQL analytical queries covering basic KPIs, cross-tabulations, Common Table Expressions (CTEs), window functions (`RANK()`, `ROW_NUMBER()`), and conditional aggregations (`CASE WHEN`).

---

## 7. Key Findings & Diagnostic Insights
1. **Contract Type is the Primary Driver**: Customers on **Month-to-month contracts** exhibit a significantly higher churn rate compared to One-year and Two-year contract holders.
2. **Tenure Vulnerability Window**: Churn is heavily concentrated in the first 12 months of customer tenure (`0–6 Months` and `7–12 Months`). Accounts surviving past 24 months demonstrate strong loyalty.
3. **Support Interaction Spike**: Customers filing **3 or more support tickets** display a marked increase in cancellation rates, signaling operational friction.
4. **Competitor & Price Pressure**: Competitor offers ("higher speed counter-offers") and high monthly charges (>$80/mo) represent the top stated reasons for departure.

---

## 8. Business Recommendations
1. **Contract Migration Incentives**: Launch targeted promotional discounts (e.g. 10% off for 12 months) encouraging Month-to-month customers to switch to annual contracts.
2. **First-Year Onboarding Program**: Establish proactive customer success touchpoints at day 30, 60, and 90 to guide new subscribers.
3. **High-Ticket Proactive Escalation**: Implement an automated trigger alerting retention specialists whenever an account files its 3rd support ticket.
4. **Competitor Price Matching**: Empower retention agents with flexible counter-offer packages for fiber-optic customers targeted by competitors.

---

## 9. Limitations
- **Synthetic Data Baseline**: The dataset is generated synthetically for portfolio purposes; findings reflect modeled probabilities rather than real-world telecommunications logs.
- **Observational Nature**: Statistical associations between variables and churn do not prove direct causality.
- **Annualized Metric Estimation**: Revenue at risk is calculated as an annualized projection (`monthly_charges * 12`) rather than historical actual cash flow loss.

---

## 10. Optional Predictive Machine Learning Extension
To extend this descriptive/diagnostic portfolio into predictive analytics:
- **Model Choice**: Logistic Regression or Random Forest Classifier trained on cleaned customer features.
- **Target Variable**: Binary `churn_flag` (1 = Churned, 0 = Active).
- **Key Metrics**: Evaluated via **Recall** (maximizing detection of actual churners), **Precision**, **F1-Score**, and **ROC-AUC**.
- **Business Rationale**: In customer retention, **Recall** is prioritized over Precision because the business cost of missing a churner (losing annual MRR) far exceeds the small cost of sending a retention discount offer to a false positive active customer.
