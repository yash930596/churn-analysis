-- ==============================================================================
-- TELECONNECT CUSTOMER CHURN ANALYTICAL SQL SUITE
-- Author: Senior Data Analyst
-- Engine: PostgreSQL / MySQL 8.0+
-- Description: Comprehensive set of 20 KPI & segmentation queries.
-- ==============================================================================

-- ==============================================================================
-- PART 1: CORE BUSINESS KPIs
-- ==============================================================================

-- Query 1 - 7: Overall TeleConnect Executive KPIs
SELECT 
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(CASE WHEN churn = 'Yes' THEN 1 END) AS churned_customers,
    COUNT(CASE WHEN churn = 'No' THEN 1 END) AS active_customers,
    ROUND(COUNT(CASE WHEN churn = 'Yes' THEN 1 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges,
    ROUND(AVG(tenure_months), 2) AS avg_tenure_months,
    ROUND(SUM(monthly_charges), 2) AS total_monthly_revenue,
    ROUND(SUM(monthly_charges * 12), 2) AS total_annualized_revenue,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN monthly_charges * 12 ELSE 0 END), 2) AS estimated_annual_revenue_at_risk
FROM customers;


-- ==============================================================================
-- PART 2: SEGMENTATION & CHURN DRIVER ANALYSIS
-- ==============================================================================

-- Query 8: Churn Rate by Contract Type
SELECT 
    contract_type,
    COUNT(*) AS total_customers,
    COUNT(CASE WHEN churn = 'Yes' THEN 1 END) AS churned_customers,
    ROUND(COUNT(CASE WHEN churn = 'Yes' THEN 1 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN monthly_charges * 12 ELSE 0 END), 2) AS annual_revenue_at_risk
FROM customers
GROUP BY contract_type
ORDER BY churn_rate_pct DESC;


-- Query 9: Churn Rate by Subscription Plan
SELECT 
    subscription_plan,
    COUNT(*) AS total_customers,
    COUNT(CASE WHEN churn = 'Yes' THEN 1 END) AS churned_customers,
    ROUND(COUNT(CASE WHEN churn = 'Yes' THEN 1 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges
FROM customers
GROUP BY subscription_plan
ORDER BY churn_rate_pct DESC;


-- Query 10: Churn Rate by Internet Service Type
SELECT 
    internet_service,
    COUNT(*) AS total_customers,
    COUNT(CASE WHEN churn = 'Yes' THEN 1 END) AS churned_customers,
    ROUND(COUNT(CASE WHEN churn = 'Yes' THEN 1 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges
FROM customers
GROUP BY internet_service
ORDER BY churn_rate_pct DESC;


-- Query 11: Churn Rate by Payment Method
SELECT 
    payment_method,
    COUNT(*) AS total_customers,
    COUNT(CASE WHEN churn = 'Yes' THEN 1 END) AS churned_customers,
    ROUND(COUNT(CASE WHEN churn = 'Yes' THEN 1 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY payment_method
ORDER BY churn_rate_pct DESC;


-- Query 12: Churn Rate by Age Group
SELECT 
    age_group,
    COUNT(*) AS total_customers,
    COUNT(CASE WHEN churn = 'Yes' THEN 1 END) AS churned_customers,
    ROUND(COUNT(CASE WHEN churn = 'Yes' THEN 1 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY age_group
ORDER BY age_group;


-- Query 13: Churn Rate by Tenure Group
SELECT 
    tenure_group,
    COUNT(*) AS total_customers,
    COUNT(CASE WHEN churn = 'Yes' THEN 1 END) AS churned_customers,
    ROUND(COUNT(CASE WHEN churn = 'Yes' THEN 1 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN monthly_charges * 12 ELSE 0 END), 2) AS annual_revenue_at_risk
FROM customers
GROUP BY tenure_group
ORDER BY churn_rate_pct DESC;


-- Query 14: Churn Rate by Satisfaction Group
SELECT 
    satisfaction_group,
    COUNT(*) AS total_customers,
    COUNT(CASE WHEN churn = 'Yes' THEN 1 END) AS churned_customers,
    ROUND(COUNT(CASE WHEN churn = 'Yes' THEN 1 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY satisfaction_group
ORDER BY churn_rate_pct DESC;


-- Query 15: Churn Rate by Support Ticket Count Group
SELECT 
    support_ticket_group,
    COUNT(*) AS total_customers,
    COUNT(CASE WHEN churn = 'Yes' THEN 1 END) AS churned_customers,
    ROUND(COUNT(CASE WHEN churn = 'Yes' THEN 1 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY support_ticket_group
ORDER BY churn_rate_pct DESC;


-- ==============================================================================
-- PART 3: FINANCIAL & REVENUE IMPACT ANALYSIS
-- ==============================================================================

-- Query 16: Total Monthly & Annualized Revenue Breakdown by Subscription Plan
SELECT 
    subscription_plan,
    ROUND(SUM(monthly_charges), 2) AS monthly_revenue,
    ROUND(SUM(monthly_charges * 12), 2) AS annualized_revenue,
    ROUND(SUM(monthly_charges * 12) * 100.0 / (SELECT SUM(monthly_charges * 12) FROM customers), 2) AS pct_of_total_revenue
FROM customers
GROUP BY subscription_plan
ORDER BY annualized_revenue DESC;


-- Query 17: Revenue Breakdown by Customer Status (Active vs Churned)
SELECT 
    customer_status,
    COUNT(*) AS customer_count,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charge,
    ROUND(SUM(monthly_charges * 12), 2) AS annualized_revenue,
    ROUND(SUM(monthly_charges * 12) * 100.0 / (SELECT SUM(monthly_charges * 12) FROM customers), 2) AS revenue_share_pct
FROM customers
GROUP BY customer_status;


-- Query 18: Revenue at Risk by Contract Type & Internet Service (CTE Example)
WITH RiskSummary AS (
    SELECT 
        contract_type,
        internet_service,
        COUNT(*) AS total_cust,
        COUNT(CASE WHEN churn = 'Yes' THEN 1 END) AS churned_cust,
        SUM(CASE WHEN churn = 'Yes' THEN monthly_charges * 12 ELSE 0 END) AS rev_at_risk
    FROM customers
    GROUP BY contract_type, internet_service
)
SELECT 
    contract_type,
    internet_service,
    total_cust,
    churned_cust,
    ROUND(churned_cust * 100.0 / total_cust, 2) AS churn_rate_pct,
    ROUND(rev_at_risk, 2) AS annual_revenue_at_risk
FROM RiskSummary
WHERE total_cust >= 50
ORDER BY annual_revenue_at_risk DESC;


-- Query 19: 4-Quadrant Customer Value/Risk Matrix Segmentation (Advanced CTE)
WITH CustomerTiers AS (
    SELECT 
        customer_id,
        contract_type,
        monthly_charges,
        support_tickets,
        churn,
        monthly_charges * 12 AS annual_rev,
        CASE WHEN monthly_charges >= 60.0 THEN 'High-Value' ELSE 'Low-Value' END AS value_segment,
        CASE WHEN churn = 'Yes' OR (contract_type = 'Month-to-month' AND support_tickets >= 3) THEN 'High-Risk' ELSE 'Low-Risk' END AS risk_segment
    FROM customers
)
SELECT 
    value_segment,
    risk_segment,
    COUNT(*) AS total_customers,
    COUNT(CASE WHEN churn = 'Yes' THEN 1 END) AS churned_customers,
    ROUND(COUNT(CASE WHEN churn = 'Yes' THEN 1 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(annual_rev), 2) AS total_annual_revenue,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN annual_rev ELSE 0 END), 2) AS annualized_revenue_at_risk
FROM CustomerTiers
GROUP BY value_segment, risk_segment
ORDER BY annualized_revenue_at_risk DESC;


-- Query 20: Top 10 High-Value Churned Customers Ranked by Revenue Loss (Window Function ROW_NUMBER)
WITH RankedLoss AS (
    SELECT 
        customer_id,
        subscription_plan,
        contract_type,
        tenure_months,
        monthly_charges,
        monthly_charges * 12 AS annual_revenue_lost,
        churn_reason,
        ROW_NUMBER() OVER (ORDER BY monthly_charges DESC, tenure_months DESC) AS rank_by_loss
    FROM customers
    WHERE churn = 'Yes'
)
SELECT 
    rank_by_loss,
    customer_id,
    subscription_plan,
    contract_type,
    tenure_months,
    monthly_charges,
    annual_revenue_lost,
    churn_reason
FROM RankedLoss
WHERE rank_by_loss <= 10;
