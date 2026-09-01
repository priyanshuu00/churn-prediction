-- ====================================================================
-- 04_churn_analysis.sql
-- Purpose: Investigate dimensions highly correlated with churn.
-- Database: MySQL
-- ====================================================================

USE telco_churn_db;

-- 1. Churn by Contract Type
SELECT 
    contract_type,
    COUNT(customer_id) AS total_customers,
    SUM(CASE WHEN churn_status = TRUE THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN churn_status = TRUE THEN 1 ELSE 0 END) / COUNT(customer_id) * 100, 2) AS churn_rate_pct
FROM vw_customer_churn_analytics
GROUP BY contract_type
ORDER BY churn_rate_pct DESC;

-- 2. Churn by Internet Service Type
SELECT 
    internet_service_type,
    COUNT(customer_id) AS total_customers,
    SUM(CASE WHEN churn_status = TRUE THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN churn_status = TRUE THEN 1 ELSE 0 END) / COUNT(customer_id) * 100, 2) AS churn_rate_pct
FROM vw_customer_churn_analytics
GROUP BY internet_service_type
ORDER BY churn_rate_pct DESC;

-- 3. Churn by Payment Method
SELECT 
    payment_method,
    COUNT(customer_id) AS total_customers,
    SUM(CASE WHEN churn_status = TRUE THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN churn_status = TRUE THEN 1 ELSE 0 END) / COUNT(customer_id) * 100, 2) AS churn_rate_pct
FROM vw_customer_churn_analytics
GROUP BY payment_method
ORDER BY churn_rate_pct DESC;

-- 4. Churn by Senior Citizen Status
SELECT 
    is_senior_citizen,
    COUNT(customer_id) AS total_customers,
    SUM(CASE WHEN churn_status = TRUE THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN churn_status = TRUE THEN 1 ELSE 0 END) / COUNT(customer_id) * 100, 2) AS churn_rate_pct
FROM vw_customer_churn_analytics
GROUP BY is_senior_citizen;

-- 5. Churn by Tech Support Subscriptions
-- Insight: Customers with tech issues and NO tech support are highly vulnerable.
SELECT 
    tech_support,
    COUNT(customer_id) AS total_customers,
    SUM(CASE WHEN churn_status = TRUE THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN churn_status = TRUE THEN 1 ELSE 0 END) / COUNT(customer_id) * 100, 2) AS churn_rate_pct
FROM vw_customer_churn_analytics
WHERE internet_service_type != 'None' -- Only evaluate for those who CAN have tech support
GROUP BY tech_support;
