-- ====================================================================
-- 02_data_cleaning.sql
-- Purpose: Extract data from staging, clean it, and load it into 
--          the normalized schema. 
-- Database: MySQL
-- ====================================================================

USE telco_churn_db;

-- --------------------------------------------------------------------
-- 1. LOAD: dim_customers
-- Standardizes binary values.
-- --------------------------------------------------------------------
INSERT INTO dim_customers (customer_id, gender, is_senior_citizen, has_partner, has_dependents)
SELECT 
    customerID,
    gender,
    CASE WHEN SeniorCitizen = '1' THEN TRUE ELSE FALSE END AS is_senior_citizen,
    CASE WHEN Partner = 'Yes' THEN TRUE ELSE FALSE END AS has_partner,
    CASE WHEN Dependents = 'Yes' THEN TRUE ELSE FALSE END AS has_dependents
FROM stg_raw_data;

-- --------------------------------------------------------------------
-- 2. LOAD: dim_services
-- Cleans redundant categorical values (e.g., 'No internet service' -> NULL/False).
-- --------------------------------------------------------------------
INSERT INTO dim_services (
    customer_id, phone_service, multiple_lines, internet_service_type, 
    online_security, online_backup, device_protection, tech_support, 
    streaming_tv, streaming_movies
)
SELECT 
    customerID,
    CASE WHEN PhoneService = 'Yes' THEN TRUE ELSE FALSE END,
    CASE 
        WHEN MultipleLines = 'No phone service' THEN 'None'
        ELSE MultipleLines 
    END AS multiple_lines,
    CASE WHEN InternetService = 'No' THEN 'None' ELSE InternetService END,
    CASE WHEN OnlineSecurity = 'Yes' THEN TRUE ELSE FALSE END,
    CASE WHEN OnlineBackup = 'Yes' THEN TRUE ELSE FALSE END,
    CASE WHEN DeviceProtection = 'Yes' THEN TRUE ELSE FALSE END,
    CASE WHEN TechSupport = 'Yes' THEN TRUE ELSE FALSE END,
    CASE WHEN StreamingTV = 'Yes' THEN TRUE ELSE FALSE END,
    CASE WHEN StreamingMovies = 'Yes' THEN TRUE ELSE FALSE END
FROM stg_raw_data;

-- --------------------------------------------------------------------
-- 3. LOAD: fct_billing_churn
-- Handled whitespace strings in TotalCharges (setting them to 0 since tenure=0).
-- --------------------------------------------------------------------
INSERT INTO fct_billing_churn (
    customer_id, tenure_months, contract_type, payment_method, paperless_billing,
    monthly_charges, total_charges, num_admin_tickets, num_tech_tickets, churn_status
)
SELECT 
    customerID,
    CAST(tenure AS SIGNED) AS tenure_months,
    Contract AS contract_type,
    PaymentMethod AS payment_method,
    CASE WHEN PaperlessBilling = 'Yes' THEN TRUE ELSE FALSE END,
    CAST(MonthlyCharges AS DECIMAL(10,2)) AS monthly_charges,
    
    -- CRITICAL FIX: Handle whitespace blank (' ') issue.
    -- MySQL TRIM() removes spaces. If empty, fallback to 0.00.
    CASE 
        WHEN TRIM(TotalCharges) = '' THEN 0.00 
        ELSE CAST(TotalCharges AS DECIMAL(10,2)) 
    END AS total_charges,
    
    CAST(numAdminTickets AS SIGNED) AS num_admin_tickets,
    CAST(numTechTickets AS SIGNED) AS num_tech_tickets,
    CASE WHEN Churn = 'Yes' THEN TRUE ELSE FALSE END AS churn_status
FROM stg_raw_data;

-- --------------------------------------------------------------------
-- 4. CREATE ANALYTICAL VIEW (For Python & Tableau Consumption)
-- --------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_customer_churn_analytics AS
SELECT 
    c.customer_id,
    c.gender,
    c.is_senior_citizen,
    c.has_partner,
    c.has_dependents,
    b.tenure_months,
    b.contract_type,
    b.payment_method,
    b.monthly_charges,
    b.total_charges,
    b.num_admin_tickets,
    b.num_tech_tickets,
    s.internet_service_type,
    s.phone_service,
    s.tech_support,
    b.churn_status
FROM dim_customers c
JOIN fct_billing_churn b ON c.customer_id = b.customer_id
JOIN dim_services s ON c.customer_id = s.customer_id;
