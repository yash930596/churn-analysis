-- ==============================================================================
-- DATA QUALITY & VALIDATION QUERIES FOR TELECONNECT
-- Use these queries to audit dataset integrity after loading data into PostgreSQL/MySQL.
-- ==============================================================================

-- 1. Check for Duplicate Customer IDs
SELECT 
    customer_id, 
    COUNT(*) AS record_count
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1;

-- 2. Check for NULL Values in Key Analytical Fields
SELECT
    COUNT(*) AS total_records,
    SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS null_customer_id,
    SUM(CASE WHEN monthly_charges IS NULL THEN 1 ELSE 0 END) AS null_monthly_charges,
    SUM(CASE WHEN total_charges IS NULL THEN 1 ELSE 0 END) AS null_total_charges,
    SUM(CASE WHEN contract_type IS NULL THEN 1 ELSE 0 END) AS null_contract_type,
    SUM(CASE WHEN churn IS NULL THEN 1 ELSE 0 END) AS null_churn
FROM customers;

-- 3. Verify Logical Consistency for Active vs Churned Customers
-- Active customers MUST NOT have churn dates or churn reasons
SELECT 
    customer_id, 
    churn, 
    churn_date, 
    churn_reason 
FROM customers
WHERE churn = 'No' AND (churn_date IS NOT NULL OR churn_reason != 'None');

-- 4. Check for Out-of-Bound Numerical Values
SELECT 
    COUNT(*) AS invalid_records
FROM customers
WHERE age < 18 OR age > 100
   OR monthly_charges < 0
   OR total_charges < 0
   OR tenure_months < 0;

-- 5. Inspect Distinct Categorical Values for Inconsistencies
SELECT DISTINCT contract_type FROM customers;
SELECT DISTINCT internet_service FROM customers;
SELECT DISTINCT payment_method FROM customers;
SELECT DISTINCT subscription_plan FROM customers;
