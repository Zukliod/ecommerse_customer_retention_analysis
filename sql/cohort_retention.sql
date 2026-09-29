-- ==============================================================================
-- E-Commerce Customer Retention & Churn Diagnostic Suite
-- Script: sql/cohort_retention.sql
-- Description: Advanced SQL Cohort Retention Matrix using Window Functions
-- Dialect: ANSI SQL / Compatible with PostgreSQL, Snowflake, and Google BigQuery
-- ==============================================================================

WITH customer_first_orders AS (
    -- Step 1: Identify the exact acquisition cohort for each customer
    SELECT
        customer_id,
        MIN(order_date) AS first_order_date,
        DATE_TRUNC('month', MIN(order_date))::DATE AS cohort_month
    FROM orders
    GROUP BY customer_id
),

customer_activities AS (
    -- Step 2: Map each subsequent purchase back to the customer's acquisition cohort
    SELECT DISTINCT
        o.customer_id,
        cfo.cohort_month,
        DATE_TRUNC('month', o.order_date)::DATE AS order_month,
        -- Calculate cohort index (number of months elapsed since acquisition)
        (
            (EXTRACT(YEAR FROM o.order_date) - EXTRACT(YEAR FROM cfo.cohort_month)) * 12 +
            (EXTRACT(MONTH FROM o.order_date) - EXTRACT(MONTH FROM cfo.cohort_month))
        )::INT AS cohort_index
    FROM orders o
    INNER JOIN customer_first_orders cfo
        ON o.customer_id = cfo.customer_id
    WHERE o.order_date >= cfo.first_order_date
),

cohort_sizes AS (
    -- Step 3: Count total initial cohort size (customers acquired in Month 0)
    SELECT
        cohort_month,
        COUNT(DISTINCT customer_id) AS cohort_size
    FROM customer_first_orders
    GROUP BY cohort_month
),

cohort_retention_counts AS (
    -- Step 4: Count active retained customers for each month period (0 to 12)
    SELECT
        ca.cohort_month,
        ca.cohort_index,
        COUNT(DISTINCT ca.customer_id) AS retained_customers
    FROM customer_activities ca
    WHERE ca.cohort_index BETWEEN 0 AND 12
    GROUP BY ca.cohort_month, ca.cohort_index
)

-- Step 5: Final output with retention rate percentages
SELECT
    TO_CHAR(crc.cohort_month, 'YYYY-MM') AS cohort,
    cs.cohort_size AS total_cohort_customers,
    crc.cohort_index AS month_period,
    crc.retained_customers,
    ROUND(
        (crc.retained_customers::NUMERIC / cs.cohort_size::NUMERIC) * 100.0, 
        2
    ) AS retention_rate_pct
FROM cohort_retention_counts crc
INNER JOIN cohort_sizes cs
    ON crc.cohort_month = cs.cohort_month
ORDER BY
    crc.cohort_month ASC,
    crc.cohort_index ASC;
