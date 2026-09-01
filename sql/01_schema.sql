-- ====================================================================
-- 01_schema.sql
-- Purpose: Define the raw staging schema and the normalized target schema.
-- Database: MySQL
-- ====================================================================

CREATE DATABASE IF NOT EXISTS telco_churn_db;
USE telco_churn_db;

-- --------------------------------------------------------------------
-- 1. STAGING TABLE
-- All columns are imported as VARCHAR to prevent load errors.
-- --------------------------------------------------------------------
DROP TABLE IF EXISTS stg_raw_data;
CREATE TABLE stg_raw_data (
    customerID VARCHAR(50) PRIMARY KEY,
    gender VARCHAR(20),
    SeniorCitizen VARCHAR(10),
    Partner VARCHAR(10),
    Dependents VARCHAR(10),
    tenure VARCHAR(10),
    PhoneService VARCHAR(10),
    MultipleLines VARCHAR(50),
    InternetService VARCHAR(50),
    OnlineSecurity VARCHAR(50),
    OnlineBackup VARCHAR(50),
    DeviceProtection VARCHAR(50),
    TechSupport VARCHAR(50),
    StreamingTV VARCHAR(50),
    StreamingMovies VARCHAR(50),
    Contract VARCHAR(50),
    PaperlessBilling VARCHAR(10),
    PaymentMethod VARCHAR(100),
    MonthlyCharges VARCHAR(20),
    TotalCharges VARCHAR(20),
    numAdminTickets VARCHAR(10),
    numTechTickets VARCHAR(10),
    Churn VARCHAR(10)
);

-- --------------------------------------------------------------------
-- 2. NORMALIZED SCHEMA
-- Demonstrating product/data architecture by logically grouping domains.
-- --------------------------------------------------------------------

-- Table: dim_customers (Demographics)
DROP TABLE IF EXISTS dim_customers;
CREATE TABLE dim_customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    gender VARCHAR(20),
    is_senior_citizen BOOLEAN,
    has_partner BOOLEAN,
    has_dependents BOOLEAN
);

-- Table: dim_services (Service Subscriptions)
DROP TABLE IF EXISTS dim_services;
CREATE TABLE dim_services (
    customer_id VARCHAR(50) PRIMARY KEY,
    phone_service BOOLEAN,
    multiple_lines VARCHAR(50),
    internet_service_type VARCHAR(50),
    online_security BOOLEAN,
    online_backup BOOLEAN,
    device_protection BOOLEAN,
    tech_support BOOLEAN,
    streaming_tv BOOLEAN,
    streaming_movies BOOLEAN,
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id)
);

-- Table: fct_billing_churn (Account, Billing, and Target Variable)
DROP TABLE IF EXISTS fct_billing_churn;
CREATE TABLE fct_billing_churn (
    customer_id VARCHAR(50) PRIMARY KEY,
    tenure_months INT,
    contract_type VARCHAR(50),
    payment_method VARCHAR(100),
    paperless_billing BOOLEAN,
    monthly_charges DECIMAL(10,2),
    total_charges DECIMAL(10,2),
    num_admin_tickets INT,
    num_tech_tickets INT,
    churn_status BOOLEAN,
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id)
);
