# Power BI Dashboard Specification

**Data Source:** `data/processed/master_table.csv`, `channel_summary.csv`, `monthly_performance.csv`
**Refresh Cadence:** Daily (scheduled refresh via Power BI Service gateway)
**Model Type:** Star schema — `campaigns` and `customers` as dimension tables, `transactions` as the fact table, joined on `campaign_id` / `customer_id`.

---

## Global Filters / Slicers (apply across all pages)
- Date range (campaign start_date)
- Channel (multi-select)
- Customer segment
- Country
- Device

---

## Page 1 — Executive Overview
**Purpose:** One-glance health check for leadership.

**KPI Cards:**
- Total Revenue, Total Cost, Net Profit
- Overall ROI, Overall ROAS
- Total Conversions, Total Customers Acquired
- Blended CAC

**Visuals:**
- Line chart: Monthly Revenue vs Cost trend
- Donut chart: Revenue share by Channel
- Map: Revenue by Country
- KPI trend sparklines (MoM change indicators)

**Drill-through:** Click any channel slice → Page 2 (Campaign Performance), filtered to that channel.

---

## Page 2 — Campaign Performance
**Visuals:**
- Table: Campaign-level detail (campaign_name, channel, cost, revenue, ROI, ROAS, conversion_rate) with conditional formatting (green/red ROI)
- Bar chart: Top 15 campaigns by ROI
- Bar chart: Bottom 15 campaigns by ROI (pause candidates)
- Scatter plot: CTR vs Conversion Rate, bubble size = revenue, color = channel

**Drill-through:** Campaign name → campaign detail page with daily performance line.

---

## Page 3 — Customer Analytics
**Visuals:**
- Bar chart: Customers & LTV by segment
- Treemap: LTV by country
- Pie: Device split
- Table: Top 100 customers by LTV
- Scatter: Age vs LTV, colored by segment

---

## Page 4 — Marketing ROI
**Visuals:**
- Matrix: Channel x Month ROI heatmap
- Bar: ROAS by channel
- Bar: CAC by channel
- Line: Cumulative revenue by channel (running total)
- Card: Best/Worst performing channel (dynamic via DAX)

---

## Page 5 — Budget Optimization
**Visuals:**
- Waterfall chart: Current vs recommended budget allocation by channel
- Table: Budget recommendation (Increase / Maintain / Decrease) with rationale
- What-if parameter: Slider to simulate % budget shift between channels, dynamically recalculating projected profit (via DAX measure using the what-if parameter)

---

## Page 6 — Forecasting
**Visuals:**
- Line chart with Power BI built-in forecasting (Analytics pane) on Monthly Revenue
- Line chart: Forecasted vs Actual Conversions
- Table: Forecasted next-quarter revenue by channel

---

## Key DAX Measures

```DAX
Total Revenue := SUM(campaigns[revenue])

Total Cost := SUM(campaigns[cost])

Net Profit := [Total Revenue] - [Total Cost]

Overall ROI := DIVIDE([Net Profit], [Total Cost], 0)

Overall ROAS := DIVIDE([Total Revenue], [Total Cost], 0)

Blended CAC := DIVIDE([Total Cost], SUM(campaigns[conversions]), 0)

MoM Revenue Growth % :=
VAR CurrMonth = [Total Revenue]
VAR PrevMonth = CALCULATE([Total Revenue], DATEADD('Date'[Date], -1, MONTH))
RETURN DIVIDE(CurrMonth - PrevMonth, PrevMonth, 0)

Rolling 3-Month Revenue :=
CALCULATE(
    [Total Revenue],
    DATESINPERIOD('Date'[Date], MAX('Date'[Date]), -3, MONTH)
)

Budget Recommendation :=
VAR ChannelROI = [Overall ROI]
VAR AvgROI = CALCULATE([Overall ROI], ALL(campaigns[channel]))
RETURN
    SWITCH(
        TRUE(),
        ChannelROI > AvgROI * 1.15, "Increase Budget",
        ChannelROI < AvgROI * 0.85, "Decrease Budget",
        "Maintain"
    )

Best Performing Channel :=
CALCULATE(
    SELECTEDVALUE(campaigns[channel]),
    TOPN(1, VALUES(campaigns[channel]), [Overall ROI], DESC)
)
```

---

## Data Model Relationships
```
customers (1) ─── (∞) transactions (∞) ─── (1) campaigns
```

- `customers[customer_id]` → `transactions[customer_id]` (One-to-Many)
- `campaigns[campaign_id]` → `transactions[campaign_id]` (One-to-Many)
- A dedicated `Date` dimension table is built via `CALENDAR()` and marked as the official Date Table for time-intelligence DAX functions.
