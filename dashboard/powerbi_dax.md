# Executive Retention & Churn Diagnostic Suite — Power BI DAX & Architecture Guide

This guide contains the complete DAX calculation library, star schema data modeling architecture, and iframe export instructions for Power BI Desktop & Service.

---

## 1. Star Schema Data Model Relationships

Connect the tables in Power BI Model View:
```
DimCustomers [customer_id] 1 <-------- * FactOrders [customer_id] (Single direction)
DimCustomers [customer_id] 1 <-------- 1 FactChurnLogs [customer_id] (Both or Single)
DimDate [Date]             1 <-------- * FactOrders [order_date]
```

---

## 2. Core DAX Measures Library

### Executive KPIs
```dax
Total Customers = 
DISTINCTCOUNT(DimCustomers[customer_id])
```

```dax
Active Customers = 
CALCULATE(
    [Total Customers],
    DimCustomers[is_churned] = 0
)
```

```dax
Churned Customers = 
CALCULATE(
    [Total Customers],
    DimCustomers[is_churned] = 1
)
```

```dax
Churn Rate % = 
DIVIDE([Churned Customers], [Total Customers], 0)
```

```dax
Net Revenue = 
SUM(FactOrders[net_amount])
```

```dax
Gross Profit = 
SUM(FactOrders[gross_profit])
```

```dax
Gross Margin % = 
DIVIDE([Gross Profit], [Net Revenue], 0)
```

```dax
Average Order Value (AOV) = 
DIVIDE([Net Revenue], DISTINCTCOUNT(FactOrders[order_id]), 0)
```

```dax
Historical LTV = 
DIVIDE([Net Revenue], [Total Customers], 0)
```

```dax
Churn Recovery Opportunity ($) = 
CALCULATE(
    [Net Revenue],
    DimCustomers[is_churned] = 1
) * 0.128
```

---

### Cohort Retention DAX Measures

```dax
Initial Cohort Customers (Month 0) = 
CALCULATE(
    DISTINCTCOUNT(FactOrders[customer_id]),
    ALLEXCEPT(FactOrders, DimCustomers[cohort_month])
)
```

```dax
Cohort Retention Rate % = 
VAR ActiveInPeriod = DISTINCTCOUNT(FactOrders[customer_id])
VAR InitialCohort = [Initial Cohort Customers (Month 0)]
RETURN
DIVIDE(ActiveInPeriod, InitialCohort, 0)
```

---

### Discount Elasticity & Sensitivity Measures

```dax
Discount Rate Average % = 
AVERAGE(FactOrders[discount_rate])
```

```dax
Repeat Customer Order Rate % = 
VAR RepeatCount = CALCULATE(
    [Total Customers],
    FILTER(DimCustomers, DimCustomers[total_orders] > 1)
)
RETURN
DIVIDE(RepeatCount, [Total Customers], 0)
```

```dax
Net Profit per Customer = 
DIVIDE([Gross Profit], [Total Customers], 0)
```

---

## 3. Power BI "Publish to Web" Configuration

1. In Power BI Desktop: Click **File** > **Publish** > **Publish to Power BI**.
2. Select your portfolio workspace.
3. In Power BI Service (app.powerbi.com):
   - Open report > Click **File** > **Embed report** > **Publish to web (public)**.
   - Set default display size to **1200 x 800** (or 16:9).
   - Copy the iframe embed URL.
4. Iframe embed snippet:
   ```html
   <iframe 
       title="E-Commerce Customer Retention & Churn Diagnostic Suite" 
       width="1200" 
       height="800" 
       src="https://app.powerbi.com/view?r=eyJrIjoi..." 
       frameborder="0" 
       allowFullScreen="true">
   </iframe>
   ```
