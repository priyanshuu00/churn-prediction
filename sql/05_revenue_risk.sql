-- ====================================================================
-- 05_revenue_risk.sql
-- Purpose: Financial impact analysis of churn (Historical).
-- Note: "Predicted Revenue at Risk" is excluded as it requires 
--       the ML model probabilities. We only calculate historical loss.
-- Database: MySQL
-- ====================================================================

USE telco_churn_db;

-- 1. Historical Monthly Revenue Lost to Churn (MRR Churn)
-- This shows the actual revenue bleeding from customers who have already left.
SELECT 
    ROUND(SUM(monthly_charges), 2) AS historical_mrr_lost,
    COUNT(customer_id) as churned_customers
FROM vw_customer_churn_analytics
WHERE churn_status = TRUE;

-- 2. Current Monthly Recurring Revenue (MRR) from Active Customers
SELECT 
    ROUND(SUM(monthly_charges), 2) AS active_mrr,
    COUNT(customer_id) as active_customers
FROM vw_customer_churn_analytics
WHERE churn_status = FALSE;

-- 3. High Friction Cohort: High Tech Tickets + Month-to-Month
-- This identifies a specific segment of ACTIVE users who exhibit high friction.
-- While we don't have ML predictions yet, this is a rule-based proxy for "At-Risk Revenue".
SELECT 
    COUNT(customer_id) as high_friction_active_customers,
    ROUND(SUM(monthly_charges), 2) as monthly_revenue_at_friction_risk
FROM vw_customer_churn_analytics
WHERE churn_status = FALSE
  AND contract_type = 'Month-to-month'
  AND num_tech_tickets >= 3;

-- 4. Historical Revenue Lost by Service Mix (Identifying biggest bleeders)
SELECT 
    internet_service_type,
    contract_type,
    ROUND(SUM(monthly_charges), 2) AS historical_mrr_lost,
    ROUND(SUM(total_charges), 2) AS historical_ltv_lost
FROM vw_customer_churn_analytics
WHERE churn_status = TRUE
GROUP BY internet_service_type, contract_type
ORDER BY historical_mrr_lost DESC;
