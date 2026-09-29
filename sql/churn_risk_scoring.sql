-- ==============================================================================
-- E-Commerce Customer Retention & Churn Diagnostic Suite
-- Script: sql/churn_risk_scoring.sql
-- Description: RFM Scoring & Multidimensional Churn Risk Diagnostic
-- Dialect: ANSI SQL / PostgreSQL / Snowflake / BigQuery Compatible
-- ==============================================================================

WITH rfm_base AS (
    -- Step 1: Calculate raw Recency, Frequency, and Monetary metrics
    SELECT
        c.customer_id,
        c.customer_segment,
        c.acquisition_channel,
        c.customer_state,
        -- Recency: Days since last order relative to observation date
        DATE_PART('day', '2018-08-31'::TIMESTAMP - MAX(o.order_date)::TIMESTAMP)::INT AS recency_days,
        -- Frequency: Total orders placed
        COUNT(DISTINCT o.order_id) AS frequency_orders,
        -- Monetary: Total net revenue generated
        SUM(o.net_amount) AS monetary_spend,
        -- Experience indicators
        AVG(o.review_score) AS avg_review_score,
        SUM(o.is_late_delivery) AS late_deliveries_count,
        AVG(o.discount_rate) AS avg_discount_rate
    FROM customers c
    INNER JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY
        c.customer_id,
        c.customer_segment,
        c.acquisition_channel,
        c.customer_state
),

rfm_quintiles AS (
    -- Step 2: Assign RFM scores 1 to 5 using NTILE window functions
    SELECT
        *,
        -- For Recency: Lower days is better -> Invert score so 5 is most recent
        NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
        -- For Frequency: Higher count is better
        NTILE(5) OVER (ORDER BY frequency_orders ASC) AS f_score,
        -- For Monetary: Higher spend is better
        NTILE(5) OVER (ORDER BY monetary_spend ASC) AS m_score
    FROM rfm_base
),

composite_risk_scoring AS (
    -- Step 3: Compute Composite RFM string & calibrated churn risk index
    SELECT
        *,
        -- Combined RFM string (e.g. '555', '111')
        CONCAT(r_score, f_score, m_score) AS rfm_cell,
        
        -- Customer Persona Mapping
        CASE
            WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions / Core VIP'
            WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal Customers'
            WHEN r_score >= 4 AND f_score = 1 THEN 'Recent First-Time Buyers'
            WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk / Slipping Away'
            WHEN r_score = 1 AND f_score >= 4 THEN 'High-Value Dormant'
            WHEN r_score <= 2 AND f_score <= 2 THEN 'Lost / Hibernating'
            ELSE 'Potential Loyalists'
        END AS rfm_persona,

        -- 0-100 Churn Risk Index (Weighting Recency 40%, Inactivity/Review 35%, Promo/Delays 25%)
        LEAST(
            100,
            GREATEST(
                0,
                ROUND(
                    ((5 - r_score) * 8.0) +
                    (LEAST(recency_days, 180) / 180.0 * 25.0) +
                    (((5.0 - COALESCE(avg_review_score, 4.0)) / 4.0) * 20.0) +
                    (CASE WHEN late_deliveries_count > 0 THEN 10 ELSE 0 END) +
                    (avg_discount_rate * 15.0)
                )::NUMERIC,
                0
            )
        ) AS churn_risk_index_100
    FROM rfm_quintiles
)

-- Final Diagnostic Classification
SELECT
    customer_id,
    customer_segment,
    acquisition_channel,
    recency_days,
    frequency_orders,
    ROUND(monetary_spend::NUMERIC, 2) AS monetary_spend,
    ROUND(avg_review_score::NUMERIC, 2) AS avg_review_score,
    late_deliveries_count,
    ROUND(avg_discount_rate * 100.0, 1) AS avg_discount_pct,
    r_score,
    f_score,
    m_score,
    rfm_cell,
    rfm_persona,
    churn_risk_index_100,
    
    -- Recommended Automated CRM Strategy
    CASE
        WHEN churn_risk_index_100 >= 75 AND monetary_spend >= 250 THEN 'High-Touch Concierge / VIP Winback Campaign'
        WHEN churn_risk_index_100 >= 75 THEN 'Automated Lapsed Re-engagement Email Sequence'
        WHEN churn_risk_index_100 BETWEEN 50 AND 74 AND late_deliveries_count > 0 THEN 'Service Recovery Apology + Shipping Credit'
        WHEN churn_risk_index_100 BETWEEN 50 AND 74 THEN 'Personalized Product Recommendation'
        ELSE 'Loyalty Retention & Upsell'
    END AS prescriptive_action
FROM composite_risk_scoring
ORDER BY churn_risk_index_100 DESC, monetary_spend DESC;
