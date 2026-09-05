# TeleConnect Customer Churn Data Dictionary

This document defines all schema attributes for the **TeleConnect Customer Churn Analysis & Retention Intelligence Dataset** (`customers.csv` and `customers_clean.csv`).

## 1. Raw Customer Attributes

| Column Name | Data Type | Description | Example Value | Business Meaning |
| :--- | :--- | :--- | :--- | :--- |
| `customer_id` | String | Unique customer identifier | `TC-10042` | Primary Key for customer record |
| `gender` | String | Gender of customer | `Female` | Demographic classification |
| `age` | Integer | Customer age in years | `38` | Demographic segment |
| `senior_citizen` | Integer (0/1) | Whether customer is 65 years or older | `0` | Senior citizen status flag |
| `marital_status` | String | Marital status | `Married` | Family structure metric |
| `dependents` | String | Whether customer has dependents | `Yes` | Household dependence indicator |
| `city` | String | Primary city of service | `Seattle` | Geographical distribution |
| `state` | String | Primary state of service | `WA` | Geographical region |
| `signup_date` | Date | Date account was created | `2021-03-15` | Account lifecycle start date |
| `tenure_months` | Integer | Months customer has subscribed | `24` | Customer relationship longevity |
| `contract_type` | String | Subscription contract commitment | `Month-to-month` | Billing contract tier |
| `subscription_plan` | String | Base tier plan | `Standard` | Core service plan tier |
| `internet_service` | String | Primary internet connection type | `Fiber optic` | Primary service infrastructure |
| `payment_method` | String | Payment method used for billing | `Electronic check` | Billing transaction channel |
| `paperless_billing` | String | Opted into paperless invoices | `Yes` | Billing preference |
| `monthly_charges` | Decimal | Recurring monthly fee ($) | `84.50` | Monthly recurring revenue (MRR) |
| `total_charges` | Decimal | Cumulative revenue spent ($) | `2028.00` | Historical customer revenue |
| `discount_percentage`| Decimal | Promotional discount percentage | `10.0` | Pricing incentive level |
| `lifetime_value` | Decimal | Estimated net revenue contribution | `1825.20` | Customer lifetime value (LTV) |
| `phone_service` | String | Has landline phone service | `Yes` | Voice product adoption |
| `multiple_lines` | String | Has multiple phone lines | `No` | Product add-on feature |
| `streaming_service` | String | Has video streaming add-on | `Yes` | Digital content add-on |
| `online_security` | String | Has security protection add-on | `No` | Cyber security add-on |
| `online_backup` | String | Has cloud backup service | `Yes` | Cloud storage add-on |
| `tech_support` | String | Has priority tech support | `No` | Support service add-on |
| `device_protection` | String | Has hardware warranty coverage | `Yes` | Device protection add-on |
| `support_tickets` | Integer | Count of technical support tickets | `3` | Operational friction indicator |
| `complaints` | Integer | Formally logged complaints | `1` | Service dissatisfaction signal |
| `avg_monthly_usage_gb`| Decimal | Average monthly data usage in GB | `245.5` | Network utilization volume |
| `satisfaction_score` | Integer | Customer rating (1 to 10 scale) | `4` | Direct CSAT feedback metric |
| `last_login_days_ago` | Integer | Days since last portal activity | `12` | Engagement recency indicator |
| `churn` | String | Whether account is cancelled | `Yes` | Primary target variable |
| `churn_date` | Date | Cancellation effective date | `2024-02-10` | Churn event timestamp |
| `churn_reason` | String | Primary stated reason for churn | `Price too high` | Churn qualitative driver |
| `competitor_offer` | String | Received competitor counter-offer | `Yes` | Market competition risk |
| `cancellation_channel`| String | Medium used to cancel service | `Online Portal` | Offboarding channel |

---

## 2. Feature-Engineered Derived Attributes

| Column Name | Data Type | Binning / Calculation Logic | Category Labels / Output |
| :--- | :--- | :--- | :--- |
| `age_group` | Categorical | `age` binned into standard cohorts | `Under 25`, `25–34`, `35–44`, `45–54`, `55–64`, `65+` |
| `tenure_group` | Categorical | `tenure_months` binned into cohorts | `0–6 Months`, `7–12 Months`, `13–24 Months`, `25–48 Months`, `49+ Months` |
| `monthly_charge_group`| Categorical | `monthly_charges`: `<$40`, `$40-$80`, `>$80` | `Low`, `Medium`, `High` |
| `support_ticket_group`| Categorical | `support_tickets`: `0`, `1-2`, `3-5`, `6+` | `0`, `1–2`, `3–5`, `6+` |
| `satisfaction_group` | Categorical | `satisfaction_score`: `1-4`, `5-7`, `8-10` | `Low`, `Medium`, `High` |
| `customer_status` | Categorical | `churn == 'Yes'` -> `Churned`, else `Active` | `Active`, `Churned` |
| `estimated_annual_revenue` | Decimal | `monthly_charges * 12` | Annualized customer value ($) |
| `estimated_revenue_at_risk` | Decimal | `estimated_annual_revenue` if `Churned` else `0.0` | Annualized revenue lost to churn ($) |
