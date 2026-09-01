-- ====================================================================
-- 03_customer_analysis.sql
-- Purpose: Broad customer-level analytics (Tenure, Demographics, Segments)
-- Database: MySQL
-- ====================================================================

USE telco_churn_db;

-- 1. High-Level Customer Metrics
SELECT 
    COUNT(customer_id) AS total_customers,
    ROUND(AVG(tenure_months), 2) AS avg_tenure_months,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges,
    SUM(CASE WHEN churn_status = TRUE THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN churn_status = TRUE THEN 1 ELSE 0 END) / COUNT(customer_id) * 100, 2) AS churn_rate_pct
FROM vw_customer_churn_analytics;

-- 2. Customer Segment Ranking by Value (Using Window Functions)
-- Ranks customer segments (Contract + Internet) by total revenue generated.
WITH segment_revenue AS (
    SELECT 
        contract_type,
        internet_service_type,
        COUNT(customer_id) AS customer_count,
        SUM(total_charges) AS total_revenue
    FROM vw_customer_churn_analytics
    GROUP BY contract_type, internet_service_type
)
SELECT 
    contract_type,
    internet_service_type,
    customer_count,
    ROUND(total_revenue, 2) AS segment_total_revenue,
    RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank
FROM segment_revenue;

-- 3. Tenure Cohort Analysis
-- Group customers into tenure buckets to identify drop-off patterns.
SELECT 
    CASE 
        WHEN tenure_months <= 12 THEN '0-12 Months (New)'
        WHEN tenure_months <= 36 THEN '13-36 Months (Mid)'
        WHEN tenure_months <= 60 THEN '37-60 Months (Established)'
        ELSE '61+ Months (Loyal)'
    END AS tenure_cohort,
    COUNT(customer_id) AS cohort_size,
    SUM(CASE WHEN churn_status = TRUE THEN 1 ELSE 0 END) AS churned_count,
    ROUND((SUM(CASE WHEN churn_status = TRUE THEN 1 ELSE 0 END) / COUNT(customer_id)) * 100, 2) AS churn_rate_pct
FROM vw_customer_churn_analytics
GROUP BY tenure_cohort
ORDER BY churn_rate_pct DESC;
