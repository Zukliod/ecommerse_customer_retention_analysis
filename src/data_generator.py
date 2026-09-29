"""
E-Commerce Customer Retention & Churn Diagnostic Suite
Synthetic Multi-Table Relational Data Generator
Generates: customers.csv, orders.csv, churn_logs.csv
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Set deterministic seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_ecommerce_data(
    num_customers: int = 4000,
    start_date: str = "2024-01-01",
    end_date: str = "2025-06-30",
    output_dir: str = "data"
):
    os.makedirs(output_dir, exist_ok=True)
    
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    total_days = (end_dt - start_dt).days

    print(f"Generating synthetic e-commerce retention dataset ({num_customers} customers)...")

    # -------------------------------------------------------------
    # 1. CUSTOMERS TABLE
    # -------------------------------------------------------------
    channels = ["Paid Search", "Organic Search", "Social Media", "Email Marketing", "Referral"]
    channel_weights = [0.32, 0.24, 0.20, 0.14, 0.10]
    
    segments = ["VIP", "Regular", "Budget / Bargain Hunter"]
    segment_weights = [0.15, 0.55, 0.30]
    
    regions = ["North America", "Europe", "Asia-Pacific", "Latin America"]
    region_weights = [0.45, 0.30, 0.18, 0.07]
    
    devices = ["Mobile", "Desktop", "Tablet"]
    device_weights = [0.62, 0.31, 0.07]

    customer_records = []
    
    # Cohort signup dates: Distributed over 2024 (12 monthly cohorts)
    # 2024-01-01 to 2024-12-31
    signup_days_span = 365

    for i in range(1, num_customers + 1):
        cust_id = f"CUST-{10000 + i}"
        signup_offset = random.randint(0, signup_days_span - 1)
        signup_date = start_dt + timedelta(days=signup_offset)
        
        channel = np.random.choice(channels, p=channel_weights)
        segment = np.random.choice(segments, p=segment_weights)
        region = np.random.choice(regions, p=region_weights)
        device = np.random.choice(devices, p=device_weights)
        
        # Base annual purchase propensity by segment
        if segment == "VIP":
            base_propensity = np.random.uniform(0.75, 0.95)
            avg_order_target = np.random.uniform(180, 350)
            target_reorders = random.randint(5, 14)
        elif segment == "Regular":
            base_propensity = np.random.uniform(0.40, 0.70)
            avg_order_target = np.random.uniform(70, 160)
            target_reorders = random.randint(2, 6)
        else: # Budget / Bargain Hunter
            base_propensity = np.random.uniform(0.20, 0.45)
            avg_order_target = np.random.uniform(35, 95)
            target_reorders = random.randint(1, 3)

        customer_records.append({
            "customer_id": cust_id,
            "signup_date": signup_date.strftime("%Y-%m-%d"),
            "acquisition_channel": channel,
            "customer_segment": segment,
            "region": region,
            "preferred_device": device,
            "cohort_month": signup_date.strftime("%Y-%m"),
            "_base_propensity": base_propensity,
            "_avg_order_target": avg_order_target,
            "_target_reorders": target_reorders
        })

    df_customers = pd.DataFrame(customer_records)

    # -------------------------------------------------------------
    # 2. ORDERS TABLE
    # -------------------------------------------------------------
    categories = ["Electronics", "Apparel", "Home & Living", "Beauty", "Fitness"]
    category_weights = [0.22, 0.35, 0.18, 0.15, 0.10]
    category_cost_ratios = {
        "Electronics": 0.68,   # 32% gross margin
        "Apparel": 0.45,       # 55% gross margin
        "Home & Living": 0.52, # 48% gross margin
        "Beauty": 0.35,        # 65% gross margin
        "Fitness": 0.50        # 50% gross margin
    }

    order_records = []
    order_counter = 10001
    customer_last_order = {}

    for _, cust in df_customers.iterrows():
        c_id = cust["customer_id"]
        c_signup = datetime.strptime(cust["signup_date"], "%Y-%m-%d")
        seg = cust["customer_segment"]
        propensity = cust["_base_propensity"]
        target_orders = cust["_target_reorders"]
        
        # 1st order happens right at or near signup (within 0-5 days)
        first_order_date = c_signup + timedelta(days=random.randint(0, 5))
        if first_order_date > end_dt:
            continue
            
        cur_order_date = first_order_date
        customer_last_order[c_id] = cur_order_date

        # Initial discount strategy based on acquisition channel
        if cust["acquisition_channel"] == "Paid Search":
            first_discount = round(float(np.random.choice([0.10, 0.15, 0.20, 0.25], p=[0.2, 0.4, 0.3, 0.1])), 2)
        elif cust["acquisition_channel"] == "Social Media":
            first_discount = round(float(np.random.choice([0.15, 0.20, 0.25, 0.30], p=[0.2, 0.4, 0.3, 0.1])), 2)
        elif cust["acquisition_channel"] == "Organic Search":
            first_discount = round(float(np.random.choice([0.0, 0.05, 0.10], p=[0.6, 0.3, 0.1])), 2)
        else:
            first_discount = round(float(np.random.choice([0.0, 0.10, 0.15], p=[0.4, 0.4, 0.2])), 2)

        cat = np.random.choice(categories, p=category_weights)
        base_val = max(18.0, float(np.random.normal(cust["_avg_order_target"], cust["_avg_order_target"] * 0.25)))
        gross_rev = round(base_val, 2)
        net_rev = round(gross_rev * (1 - first_discount), 2)
        cogs = round(net_rev * category_cost_ratios[cat], 2)
        profit = round(net_rev - cogs, 2)
        margin = round(profit / max(net_rev, 1.0), 3)

        order_records.append({
            "order_id": f"ORD-{order_counter}",
            "customer_id": c_id,
            "order_date": cur_order_date.strftime("%Y-%m-%d"),
            "product_category": cat,
            "gross_amount": gross_rev,
            "discount_rate": first_discount,
            "discount_amount": round(gross_rev * first_discount, 2),
            "net_amount": net_rev,
            "cogs": cogs,
            "gross_profit": profit,
            "profit_margin": margin,
            "is_first_order": 1
        })
        order_counter += 1

        # Subsequent repeat orders with retention decay
        for order_num in range(2, target_orders + 1):
            reorder_prob = propensity * (0.88 ** (order_num - 1))
            if random.random() > reorder_prob:
                break
                
            if seg == "VIP":
                gap_days = random.randint(18, 48)
            elif seg == "Regular":
                gap_days = random.randint(30, 85)
            else:
                gap_days = random.randint(45, 120)

            cur_order_date = cur_order_date + timedelta(days=gap_days)
            if cur_order_date > end_dt:
                break
                
            customer_last_order[c_id] = cur_order_date

            if seg == "Budget / Bargain Hunter":
                discount = round(float(np.random.choice([0.15, 0.20, 0.25, 0.35], p=[0.3, 0.4, 0.2, 0.1])), 2)
            elif seg == "VIP":
                discount = round(float(np.random.choice([0.0, 0.05, 0.10, 0.15], p=[0.5, 0.3, 0.15, 0.05])), 2)
            else:
                discount = round(float(np.random.choice([0.0, 0.05, 0.10, 0.15, 0.20], p=[0.35, 0.25, 0.20, 0.15, 0.05])), 2)

            cat = np.random.choice(categories, p=category_weights)
            base_val = max(15.0, float(np.random.normal(cust["_avg_order_target"], cust["_avg_order_target"] * 0.22)))
            gross_rev = round(base_val, 2)
            net_rev = round(gross_rev * (1 - discount), 2)
            cogs = round(net_rev * category_cost_ratios[cat], 2)
            profit = round(net_rev - cogs, 2)
            margin = round(profit / max(net_rev, 1.0), 3)

            order_records.append({
                "order_id": f"ORD-{order_counter}",
                "customer_id": c_id,
                "order_date": cur_order_date.strftime("%Y-%m-%d"),
                "product_category": cat,
                "gross_amount": gross_rev,
                "discount_rate": discount,
                "discount_amount": round(gross_rev * discount, 2),
                "net_amount": net_rev,
                "cogs": cogs,
                "gross_profit": profit,
                "profit_margin": margin,
                "is_first_order": 0
            })
            order_counter += 1

    df_orders = pd.DataFrame(order_records)

    # Clean internal columns from df_customers before export
    df_customers_clean = df_customers.drop(columns=["_base_propensity", "_avg_order_target", "_target_reorders"])

    # -------------------------------------------------------------
    # 3. CHURN LOGS TABLE
    # -------------------------------------------------------------
    churn_threshold_days = 90
    churn_reasons = [
        "Price Sensitivity / High Shipping",
        "Competitor Switch",
        "Product Quality / Expectation Gap",
        "Poor Customer Service / Delivery Delay",
        "Inactive / Seasonal Disinterest"
    ]
    churn_reason_weights = [0.34, 0.26, 0.18, 0.12, 0.10]

    churn_records = []
    churn_counter = 5001

    cust_agg = df_orders.groupby("customer_id").agg(
        total_orders=("order_id", "count"),
        total_net_spend=("net_amount", "sum"),
        avg_discount=("discount_rate", "mean"),
        last_order_date=("order_date", "max")
    ).reset_index()

    for _, row in cust_agg.iterrows():
        c_id = row["customer_id"]
        last_dt = datetime.strptime(row["last_order_date"], "%Y-%m-%d")
        days_inactive = (end_dt - last_dt).days
        
        if days_inactive >= churn_threshold_days:
            churn_offset = min(days_inactive, random.randint(45, 90))
            churn_dt = last_dt + timedelta(days=churn_offset)
            
            if row["avg_discount"] > 0.20 and row["total_orders"] <= 2:
                reason = "Price Sensitivity / High Shipping"
                nps = random.choice([2, 3, 4, 5, 6])
            else:
                reason = np.random.choice(churn_reasons, p=churn_reason_weights)
                if reason in ["Product Quality / Expectation Gap", "Poor Customer Service / Delivery Delay"]:
                    nps = random.choice([0, 1, 2, 3, 4])
                elif reason == "Competitor Switch":
                    nps = random.choice([5, 6, 7])
                else:
                    nps = random.choice([6, 7, 8])

            hazard = round(min(0.99, 0.55 + (days_inactive / 365.0) * 0.45 + (row["avg_discount"] * 0.2)), 3)

            churn_records.append({
                "churn_id": f"CHURN-{churn_counter}",
                "customer_id": c_id,
                "churn_date": churn_dt.strftime("%Y-%m-%d"),
                "churn_reason": reason,
                "last_survey_nps": nps,
                "days_inactive": days_inactive,
                "prior_lifetime_spend": round(row["total_net_spend"], 2),
                "churn_hazard_score": hazard,
                "is_churned": 1
            })
            churn_counter += 1

    df_churn = pd.DataFrame(churn_records)

    cust_path = os.path.join(output_dir, "customers.csv")
    orders_path = os.path.join(output_dir, "orders.csv")
    churn_path = os.path.join(output_dir, "churn_logs.csv")

    df_customers_clean.to_csv(cust_path, index=False)
    df_orders.to_csv(orders_path, index=False)
    df_churn.to_csv(churn_path, index=False)

    print(f"Data generation complete!")
    print(f" - {len(df_customers_clean):,} Customers saved to {cust_path}")
    print(f" - {len(df_orders):,} Orders saved to {orders_path}")
    print(f" - {len(df_churn):,} Churn Logs saved to {churn_path}")
    print(f" - Churn Rate: {len(df_churn) / len(df_customers_clean):.1%}")

if __name__ == "__main__":
    generate_ecommerce_data()
