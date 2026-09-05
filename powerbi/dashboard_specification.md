# TeleConnect Power BI Dashboard Specification

## Executive Summary
This document provides a comprehensive technical blueprint for implementing the **TeleConnect Customer Churn & Retention Intelligence Dashboard** in Power BI Desktop / Service. The dashboard consists of 3 interactively connected pages designed for executive leadership, product managers, and retention operation leads.

---

## Global Canvas & Theme Guidelines
- **Canvas Size**: 16:9 Widescreen (1920 x 1080 px).
- **Color Palette**:
  - **Primary Corporate**: `#1E3A8A` (Navy Blue)
  - **Active / Positive Status**: `#10B981` (Emerald Green)
  - **Churn / High Risk Status**: `#EF4444` (Crimson Red)
  - **Neutral Background**: `#F8FAFC` (Light Gray Canvas)
  - **Card Container Fill**: `#FFFFFF` (Pure White with subtle 1px border `#E2E8F0`)
- **Typography**: Segoe UI / Helvetica, bold headers (16–20pt), KPI values (24–32pt), data labels (9–10pt).

---

## PAGE 1 — EXECUTIVE OVERVIEW

### Title
**TeleConnect Customer Churn Overview**

### Top Navigation & Slicer Panel (Header Row)
- **Global Slicers**:
  1. `Contract Type` (Dropdown: All, Month-to-month, One year, Two year)
  2. `Subscription Plan` (Dropdown: All, Basic, Standard, Premium)
  3. `Internet Service` (Dropdown: All, DSL, Fiber optic, None)
  4. `Payment Method` (Dropdown: All, Electronic check, Mailed check, Bank transfer, Credit card)
  5. `Age Group` (Multi-select pill buttons: Under 25, 25-34, 35-44, 45-54, 55-64, 65+)

### KPI Metric Cards (Row 1)
| Card Title | DAX Measure | Format | Accent Border |
| :--- | :--- | :--- | :--- |
| **Total Customers** | `[Total Customers]` | `#,##0` | Navy Blue |
| **Active Customers** | `[Active Customers]` | `#,##0` | Emerald Green |
| **Churned Customers** | `[Churned Customers]` | `#,##0` | Crimson Red |
| **Churn Rate** | `[Churn Rate %]` | `0.00%` | Crimson Red |
| **Avg Monthly Charge** | `[Avg Monthly Charge]` | `$#,##0.00` | Navy Blue |
| **Annual Rev at Risk**| `[Annualized Revenue at Risk]` | `$#,##0` | Crimson Red |

### Main Analytical Visuals (Row 2 & 3)
1. **Visual 1 (Bar Chart)**: *Churn Rate by Contract Type*
   - X-Axis: `contract_type`
   - Y-Axis: `[Churn Rate %]`
   - Data labels enabled. Color highlight: Month-to-month highlighted in Red.
2. **Visual 2 (Bar Chart)**: *Churn Rate by Subscription Plan Tier*
   - X-Axis: `subscription_plan` (Basic, Standard, Premium)
   - Y-Axis: `[Churn Rate %]`
3. **Visual 3 (Column Chart)**: *Churn Rate by Tenure Cohort*
   - X-Axis: `tenure_group` (`0–6 Months`, `7–12 Months`, `13–24 Months`, `25–48 Months`, `49+ Months`)
   - Y-Axis: `[Churn Rate %]`
4. **Visual 4 (Donut Chart)**: *Satisfaction Group Distribution*
   - Legend: `satisfaction_group` (Low, Medium, High)
   - Values: `[Total Customers]`

### Key Insight Card (Bottom Overlay)
> **Key Executive Takeaway**: Customers on **Month-to-month contracts** and **new subscriptions (<12 months tenure)** exhibit disproportionately higher churn rates compared to long-term contract holders, contributing to over 70% of total annual revenue at risk.

---

## PAGE 2 — CHURN DRIVERS & CUSTOMER BEHAVIOR

### Title
**Churn Drivers & Customer Behavior**

### Layout & Visual Grid
1. **Visual 1 (Stacked Bar Chart)**: *Churn vs Active Distribution by Payment Method*
   - Y-Axis: `payment_method`
   - X-Axis: `[Total Customers]`
   - Legend: `customer_status` (Active vs Churned)
2. **Visual 2 (Column Chart)**: *Churn Rate by Support Tickets Filed*
   - X-Axis: `support_ticket_group` (`0`, `1–2`, `3–5`, `6+`)
   - Y-Axis: `[Churn Rate %]`
3. **Visual 3 (Density / Area Chart)**: *Monthly Charge Density by Status*
   - X-Axis: `monthly_charges`
   - Y-Axis: Customer Count / Density
   - Split Series: `customer_status`
4. **Visual 4 (Horizontal Bar Chart)**: *Primary Reasons for Customer Cancellation*
   - Y-Axis: `churn_reason`
   - X-Axis: `[Churned Customers]`
   - Sorted descending by count.
5. **Visual 5 (Clustered Bar Chart)**: *CSAT Score Impact on Churn*
   - X-Axis: `satisfaction_score` (1 to 10)
   - Y-Axis: `[Churn Rate %]`

### Diagnostic Insight Cards
- **Support Ticket Threshold**: Customers filing **3 or more support tickets** show a significant jump in churn probability.
- **Competitor Pressure**: Competitor offers and pricing dissatisfaction account for the majority of stated cancellation reasons.

---

## PAGE 3 — RETENTION & REVENUE AT RISK

### Title
**Retention Opportunities & Revenue at Risk**

### Layout & Visual Grid
1. **Visual 1 (Treemap / Bar Chart)**: *Annualized Revenue at Risk by Contract & Internet Type*
   - Grouping: `contract_type`, `internet_service`
   - Values: `[Annualized Revenue at Risk]`
2. **Visual 2 (Matrix Table)**: *4-Quadrant Customer Value / Risk Segmentation*
   - Rows: `value_tier` (High-Value vs Low-Value)
   - Columns: `risk_tier` (High-Risk vs Low-Risk)
   - Values: `[Total Customers]`, `[Churn Rate %]`, `[Annualized Revenue at Risk]`
3. **Visual 3 (Detailed Actionable Retention Table)**:
   - Columns:
     - `Segment Name`
     - `Customer Count`
     - `Churn Rate %`
     - `Churned Customers`
     - `Monthly Revenue ($)`
     - `Annualized Revenue at Risk ($)`
   - Filtered for top retention priority segments.

### Priority Action Summary
1. **High-Value, High-Risk Target**: Immediate intervention for accounts paying >$60/mo with Month-to-month contracts.
2. **Onboarding Intervention**: Automated check-ins during months 1–6 to reduce early tenure drop-off.
