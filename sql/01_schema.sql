-- ==============================================================================
-- TELECONNECT CUSTOMER CHURN DATABASE SCHEMA
-- Compatible with PostgreSQL and MySQL 8.0+
-- ==============================================================================

DROP TABLE IF EXISTS customers CASCADE;

CREATE TABLE customers (
    -- Primary Key
    customer_id                 VARCHAR(20) PRIMARY KEY,
    
    -- Demographics
    gender                      VARCHAR(10) NOT NULL,
    age                         INT CHECK (age >= 18 AND age <= 120),
    senior_citizen              INT CHECK (senior_citizen IN (0, 1)),
    marital_status              VARCHAR(15) NOT NULL,
    dependents                  VARCHAR(5) NOT NULL,
    city                        VARCHAR(50) NOT NULL,
    state                       VARCHAR(5) NOT NULL,
    
    -- Subscription Information
    signup_date                 DATE NOT NULL,
    tenure_months               INT NOT NULL CHECK (tenure_months >= 0),
    contract_type               VARCHAR(20) NOT NULL,
    subscription_plan           VARCHAR(20) NOT NULL,
    internet_service            VARCHAR(20) NOT NULL,
    payment_method              VARCHAR(30) NOT NULL,
    paperless_billing           VARCHAR(5) NOT NULL,
    
    -- Financial Information
    monthly_charges             DECIMAL(10, 2) NOT NULL CHECK (monthly_charges >= 0),
    total_charges               DECIMAL(10, 2) NOT NULL CHECK (total_charges >= 0),
    discount_percentage         DECIMAL(5, 2) DEFAULT 0.00,
    lifetime_value              DECIMAL(10, 2) NOT NULL,
    
    -- Services & Features
    phone_service               VARCHAR(5) NOT NULL,
    multiple_lines              VARCHAR(20) NOT NULL,
    streaming_service           VARCHAR(5) NOT NULL,
    online_security             VARCHAR(5) NOT NULL,
    online_backup               VARCHAR(5) NOT NULL,
    tech_support                VARCHAR(5) NOT NULL,
    device_protection           VARCHAR(5) NOT NULL,
    
    -- Customer Engagement & Satisfaction
    support_tickets             INT NOT NULL DEFAULT 0,
    complaints                  INT NOT NULL DEFAULT 0,
    avg_monthly_usage_gb        DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    satisfaction_score          INT CHECK (satisfaction_score BETWEEN 1 AND 10),
    last_login_days_ago         INT NOT NULL DEFAULT 0,
    
    -- Churn Information
    churn                       VARCHAR(5) NOT NULL CHECK (churn IN ('Yes', 'No')),
    churn_date                  DATE NULL,
    churn_reason                VARCHAR(100) NULL,
    competitor_offer            VARCHAR(5) NULL,
    cancellation_channel        VARCHAR(30) NULL,

    -- Derived Features
    age_group                   VARCHAR(20) NULL,
    tenure_group                VARCHAR(20) NULL,
    monthly_charge_group        VARCHAR(15) NULL,
    support_ticket_group        VARCHAR(15) NULL,
    satisfaction_group          VARCHAR(15) NULL,
    customer_status             VARCHAR(15) NULL,
    estimated_annual_revenue    DECIMAL(10, 2) NULL,
    estimated_revenue_at_risk   DECIMAL(10, 2) NULL
);

-- Indexes for performance optimization on frequent analytical queries
CREATE INDEX idx_customers_churn ON customers(churn);
CREATE INDEX idx_customers_contract ON customers(contract_type);
CREATE INDEX idx_customers_tenure ON customers(tenure_months);
CREATE INDEX idx_customers_plan ON customers(subscription_plan);
CREATE INDEX idx_customers_satisfaction ON customers(satisfaction_score);
CREATE INDEX idx_customers_status ON customers(customer_status);
