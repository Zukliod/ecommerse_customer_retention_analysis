-- ==============================================================================
-- E-Commerce Customer Retention & Churn Diagnostic Suite
-- Script: sql/customer_ltv.sql
-- Description: Historical & Predictive Customer Lifetime Value (LTV) Calculation
-- Dialect: ANSI SQL / PostgreSQL / Snowflake / BigQuery Compatible
-- ==============================================================================

WITH customer_order_summary AS (
    -- Step 1: Compute core transaction aggregates per customer
    SELECT
        o.customer_id,
        MIN(o.order_date) AS first_order_date,
        MAX(o.order_date) AS last_order_date,
        COUNT(DISTINCT o.order_id) AS total_orders,
        SUM(o.net_amount) AS total_historical_spend,
        SUM(o.gross_profit) AS total_historical_profit,
        AVG(o.net_amount) AS avg_order_value,
        AVG(o.discount_rate) AS avg_discount_rate,
        AVG(o.review_score) AS avg_review_score,
        -- Days active between first and last purchase
        DATE_PART('day', MAX(o.order_date)::TIMESTAMP - MIN(o.order_date)::TIMESTAMP) AS active_tenure_days,
        -- Days inactive since last purchase (Observation cutoff: 2018-08-31)
        DATE_PART('day', '2018-08-31'::TIMESTAMP - MAX(o.order_date)::TIMESTAMP) AS days_inactive
    FROM orders o
    GROUP BY o.customer_id
),

customer_segmentation AS (
    -- Step 2: Join customer metadata and assign strategic value tiers
    SELECT
        cos.*,
        c.acquisition_channel,
        c.customer_state,
        c.customer_segment,
        -- Churn status: Inactivity >= 90 days
        CASE WHEN cos.days_inactive >= 90 THEN 1 ELSE 0 END AS is_churned,
        -- Gross profit margin realized
        CASE 
            WHEN cos.total_historical_spend > 0 
            THEN ROUND((cos.total_historical_profit / cos.total_historical_spend)::NUMERIC, 4)
            ELSE 0.40
        END AS realized_margin_rate
    FROM customer_order_summary cos
    INNER JOIN customers c
        ON cos.customer_id = c.customer_id
),

predictive_ltv_modeling AS (
    -- Step 3: Compute Predictive LTV over 24-Month Horizon
    -- Formula: LTV = (Avg Order Value * Annual Order Frequency * Margin) / Churn Hazard
    SELECT
        cs.*,
        -- Calibrated churn hazard probability based on inactivity & reviews
        ROUND(
            LEAST(
                0.99,
                GREATEST(
                    0.05,
                    (cs.days_inactive / 365.0) * 0.45 +
                    ((5.0 - COALESCE(cs.avg_review_score, 4.0)) / 4.0) * 0.35 +
                    (cs.avg_discount_rate * 0.20)
                )
            )::NUMERIC, 
            3
        ) AS churn_hazard_score,
        
        -- Segment-adjusted retention multiplier
        CASE 
            WHEN cs.customer_segment = 'VIP' THEN 2.80
            WHEN cs.customer_segment = 'Regular' THEN 1.40
            ELSE 0.90
        END AS segment_retention_multiplier
    FROM customer_segmentation cs
)

SELECT
    customer_id,
    customer_segment,
    acquisition_channel,
    customer_state,
    total_orders,
    ROUND(total_historical_spend::NUMERIC, 2) AS historical_ltv,
    ROUND(total_historical_profit::NUMERIC, 2) AS historical_gross_profit,
    ROUND(avg_order_value::NUMERIC, 2) AS aov,
    ROUND(realized_margin_rate * 100.0, 1) AS margin_pct,
    days_inactive,
    churn_hazard_score,
    is_churned,
    
    -- Predicted 24-Month Future Value
    ROUND(
        (total_historical_spend * segment_retention_multiplier * (1.0 - (is_churned * 0.75)))::NUMERIC,
        2
    ) AS predicted_future_ltv,
    
    -- High-priority intervention flag: VIP or High Historical Spend with High Churn Risk
    CASE 
        WHEN is_churned = 0 AND churn_hazard_score >= 0.50 AND total_historical_spend >= 250 THEN 'Critical Retention Priority'
        WHEN is_churned = 0 AND churn_hazard_score >= 0.35 THEN 'Medium Risk Watchlist'
        WHEN is_churned = 1 AND total_historical_spend >= 200 THEN 'Winback Candidate'
        ELSE 'Standard Lifecycle'
    END AS retention_action_tier
FROM predictive_ltv_modeling
ORDER BY historical_ltv DESC;
