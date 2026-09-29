# Executive Retention & Churn Diagnostic Suite — Tableau Workbook Specification

This document provides the blueprint for building the **Executive Retention & Churn Diagnostic Suite** in Tableau Desktop / Tableau Public.

---

## 1. Canvas Dimensions & Web Embedding Parameters

To ensure pixel-perfect responsive embedding into web portfolios without horizontal/vertical scrollbars:
- **Dashboard Size**: Fixed Size: **1200 px (Width) x 800 px (Height)**
- **Device Layouts**: Default (1200x800) + Phone Layout (375 px Auto-fit single column)
- **Tableau Public Toolbar**: `toolbar=no` (or hidden via embed parameter `:toolbar=no`)
- **Container Ratio**: 3:2 (1200 / 800 = 1.5 aspect ratio)

---

## 2. Calculated Fields & Level of Detail (LOD) Expressions

### Cohort & Retention Fields
1. **`[Customer First Order Date]`** (LOD Expression):
   ```tableau
   { FIXED [Customer Id] : MIN([Order Date]) }
   ```
2. **`[Cohort Month]`**:
   ```tableau
   DATETRUNC('month', [Customer First Order Date])
   ```
3. **`[Order Month]`**:
   ```tableau
   DATETRUNC('month', [Order Date])
   ```
4. **`[Cohort Index (Months Elapsed)]`**:
   ```tableau
   DATEDIFF('month', [Cohort Month], [Order Month])
   ```
5. **`[Initial Cohort Size (Month 0)]`** (LOD Expression):
   ```tableau
   { FIXED [Cohort Month] : COUNTD(IF [Cohort Index (Months Elapsed)] = 0 THEN [Customer Id] END) }
   ```
6. **`[Cohort Retention %]`**:
   ```tableau
   COUNTD([Customer Id]) / SUM([Initial Cohort Size (Month 0)])
   ```

### Financial & Churn Opportunity Fields
7. **`[Is Churned]`**:
   ```tableau
   IF [Days Inactive] >= 90 THEN 1 ELSE 0 END
   ```
8. **`[Churn Rate %]`**:
   ```tableau
   SUM([Is Churned]) / COUNTD([Customer Id])
   ```
9. **`[Historical LTV]`**:
   ```tableau
   { FIXED [Customer Id] : SUM([Net Amount]) }
   ```
10. **`[Churn Revenue Recovery Opportunity ($)]`**:
    ```tableau
    SUM(IF [Is Churned] = 1 THEN [Net Amount] END) * 0.128
    ```
11. **`[Discount Tier]`**:
    ```tableau
    IF [Discount Rate] = 0 THEN "0% (Full Price)"
    ELSEIF [Discount Rate] <= 0.05 THEN "1% - 5%"
    ELSEIF [Discount Rate] <= 0.15 THEN "6% - 15%"
    ELSEIF [Discount Rate] <= 0.25 THEN "16% - 25%"
    ELSE "25%+ (Deep Promo)"
    END
    ```

---

## 3. Visualizations & Sheet Architecture

### Sheet 1: Executive KPI Header (Tiled Top Container, 1200x90)
- **KPI 1: Active Retained Base**: `COUNTD(IF [Is Churned]=0 THEN [Customer Id] END)` (e.g. 18,073)
- **KPI 2: Overall Churn Rate**: `80.6%` (with alert threshold color)
- **KPI 3: Average LTV**: `$138.35`
- **KPI 4: Churn Recovery Opportunity**: `$1,327,385` (12.8% benchmark target)

### Sheet 2: Cohort Retention Heatmap (Dimensions: 720x420)
- **Rows**: `[Cohort Month]` (Discrete Month-Year, e.g. Jan 2017 to Jul 2018)
- **Columns**: `[Cohort Index (Months Elapsed)]` (Discrete, filtered 0 to 12)
- **Marks**: Square
- **Color**: `[Cohort Retention %]` using sequential palette (`#1E293B` to `#3B82F6` or Emerald Green)
- **Label**: `[Cohort Retention %]` formatted as percentage with 1 decimal place (`0.0%`)
- **Tooltip**: Cohort Month, Months Elapsed, Active Customers, Initial Cohort Size, Retention Rate

### Sheet 3: Discount Sensitivity & Elasticity Curves (Dimensions: 460x420)
- **Columns**: `[Discount Tier]` (Ordered 0% to 25%+)
- **Rows (Dual Axis)**:
  - Axis 1 (Bars): `SUM([Net Amount])` or `AVG([Gross Profit])` (Emerald Green)
  - Axis 2 (Line): `[Churn Rate %]` (Crimson Red `#EF4444`)
- **Insight Callout**: Highlights the margin collapse beyond the 15% discount threshold.

### Sheet 4: Category Churn vs. Margin Matrix (Dimensions: 1180x260)
- **Columns**: `[Product Category]` (Sorted by Net Revenue descending)
- **Rows**: `[Profit Margin %]` vs `[Churn Rate %]` (Scatter or horizontal bullet bars)
- **Color by**: `[Profit Margin %]` gradient (Red to Green)
- **Size by**: `SUM([Net Amount])`

---

## 4. Tableau Public Web Embedding Configuration

When publishing to Tableau Public:
1. In Tableau Desktop: Select **Server** > **Tableau Public** > **Save to Tableau Public As...**
2. On Tableau Public: Click **Edit Details**:
   - Check **Show workbook sheets as tabs**: Uncheck (keep clean single dashboard)
   - Check **Allow others to download this workbook**: Yes (good for recruiters)
3. Embed Code Options:
   ```html
   <div class='tableauPlaceholder' id='viz1700000000000' style='position: relative; width: 100%; height: 100%;'>
       <noscript>
           <a href='#'><img alt='Executive Retention Dashboard' src='https://public.tableau.com/static/images/...' border='none' /></a>
       </noscript>
       <object class='tableauViz' style='display:none;'>
           <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
           <param name='embed_code_version' value='3' />
           <param name='site_root' value='' />
           <param name='name' value='EcommerceRetentionDiagnosticSuite/ExecutiveDashboard' />
           <param name='tabs' value='no' />
           <param name='toolbar' value='no' />
           <param name='animate_transition' value='yes' />
           <param name='display_static_image' value='yes' />
           <param name='display_spinner' value='yes' />
           <param name='display_overlay' value='yes' />
           <param name='display_count' value='yes' />
           <param name='language' value='en-US' />
       </object>
   </div>
   ```
