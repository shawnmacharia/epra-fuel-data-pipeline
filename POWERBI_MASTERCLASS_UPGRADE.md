# EPRA Fuel Intelligence – Masterclass Power BI Dashboard Design

## Executive Summary

Your current dashboard has the foundation (KPIs, trends, spatial heat map, filters). This document provides a **pro-tier upgrade** covering 8 advanced pages and professional analytical features to make it a portfolio showcase.

---

## Current State Assessment

✅ **What's Working:**
- Clean beige/coral color scheme (on-brand)
- 4 KPI cards (PMS, Diesel, Kerosene, Town count)
- Historical price trends (line chart)
- Top 8 locations by price (bar chart)
- Kenya heat map (density visualization)
- Multi-page navigation (National Overview, Regional Benchmarking, Historical Trends)
- Professional filtering (Fuel Type, Year.Month, Town)

❌ **What's Missing (Masterclass Gaps):**
- No profitability/margin analysis (consumer impact metrics)
- No volatility or month-over-month change tracking
- No forecast or trend prediction
- No comparative analysis (regional outliers, anomalies)
- No drill-through capabilities
- No executive summary or KPI story
- Limited interactivity (no advanced tooltips, no ranking/flagging)
- No export-ready analytics

---

## 8-Page Masterclass Dashboard Architecture

### **Page 1: Executive Dashboard** (Landing Page)
**Purpose:** C-suite snapshot in 10 seconds

**Components:**
1. **Hero KPI Section** (Top 4 cards, larger fonts)
   - Current National Average (All Fuels Blended)
   - Highest Priced Location + Price + %ile rank
   - Lowest Priced Location + Price + %ile rank
   - Month-over-Month Change % (color-coded: 🔴 red if increase, 🟢 green if decrease)

2. **Gauge Charts** (3 gauges side-by-side)
   - PMS Price vs. historical range (min–max band)
   - Diesel Price vs. historical range
   - Kerosene Price vs. historical range
   - Visually show if price is high/mid/low relative to history

3. **Narrative Cards** (3 text boxes with DAX-generated insights)
   - "Fuel volatility: X% this month (vs. Y% average)"
   - "Highest regional variance: [Region] (±Z KES)"
   - "Affordability index: [Score/10] vs. last month"

4. **Trending Pill Chart**
   - Top 5 price changers (up/down) this period
   - Color bar length = magnitude of change
   - Icon (⬆️ ⬇️) to show direction

5. **Heatmap Sparklines**
   - Row = last 6 pricing cycles
   - Column = each fuel type
   - Color intensity = price level
   - Quick visual to spot seasonal patterns

**Filters (Top Bar):**
- Date range picker (defaults to latest cycle)
- Region (multi-select)
- Fuel Type (multi-select)

---

### **Page 2: Price Trends & Forecasting**
**Purpose:** Historical context + predictive insight

**Components:**

1. **Combination Chart** (Primary)
   - X-axis: Date (last 12 pricing cycles)
   - Y-axis Left: Price (KES) – line for each fuel type
   - Y-axis Right: Volume of towns reporting data (bar)
   - Overlay confidence bands (95% CI from forecasting)

2. **Forecast Panel** (Secondary)
   - Line chart: Observed + forecasted 3-cycle ahead (using DAX or Python)
   - Toggle: Show/hide different fuel types
   - Forecast method badge: "Exponential Smoothing (RMSE: 2.3%)"

3. **Volatility Ribbon Chart**
   - Rows = Fuel types
   - X-axis = Date
   - Color intensity = Standard Deviation (volatility) in that cycle
   - Hover: Exact volatility value, trigger events (e.g., "Oil price spike")

4. **Year-over-Year Comparison**
   - Small multiples: 3 small line charts (PMS, Diesel, Kerosene)
   - Overlay: Current year vs. previous year
   - Highlight seasonal peaks/troughs

5. **Decomposition Tree** (Optional Advanced)
   - Root: Average fuel price
   - Branches: By region → By location → By fuel type
   - Click to expand/collapse and drill down

**Filters:**
- Fuel Type
- Region
- Date range (with presets: Last 3 months, 6 months, 12 months, YTD)

---

### **Page 3: Regional Benchmarking & Outliers**
**Purpose:** Comparative analysis, anomaly detection

**Components:**

1. **Regional Heatmap** (Primary Visual)
   - Rows = Regions (Nairobi, Coast, Rift Valley, etc.)
   - Columns = Fuel types (PMS, Diesel, Kerosene)
   - Cells = Average price, colored by quartile (darkest = most expensive)
   - Hover: Show town count, min–max range

2. **Outlier Detection Panel**
   - Table: Towns with prices >2 std devs from regional mean
   - Columns: Town | Region | Fuel | Price | Regional Avg | Deviation % | Flag Reason
   - Conditional formatting: Red if >+15% deviation, Blue if <-15%
   - Action column: "Export for Investigation"

3. **Regional Box-and-Whisker Charts**
   - 3 charts (one per fuel type)
   - X-axis = Regions
   - Y-axis = Price distribution (quartiles, outliers, median)
   - Show which regions have widest price variance

4. **Affordability Index by Region**
   - Clustered bar chart: Regions × Fuel types
   - Y-axis = Affordability Score (inverse of price, normalized 0–100)
   - Color: Green = affordable, Red = unaffordable
   - Overlay threshold line = national average

5. **Map with Region Tooltips**
   - Kenya map (by county/region)
   - Bubble size = price level
   - Color = price trend (↑ red, ↓ green)
   - Hover: Region name, avg price, town count, fuel breakdown

**Filters:**
- Fuel Type
- Metric (Price Level / Volatility / Affordability)
- Comparison Period (Current vs. Previous cycle)

---

### **Page 4: Location Deep Dive & Ranking**
**Purpose:** Town-by-town analysis, performance ranking

**Components:**

1. **Interactive Location Ranking Table** (Primary)
   - Sortable columns: Rank | Town | Region | PMS | Diesel | Kerosene | Avg Price | Trend | Volatility
   - Conditional formatting: Heatmap on price columns
   - Hover actions: "View detail" → opens detail panel
   - Search/filter bar: Type town name to focus

2. **Comparison Slider**
   - Select 2–4 locations
   - Side-by-side bar charts showing their fuel prices
   - Variance arrows (↑ ↓) showing month-over-month change

3. **Location Performance Card** (Dynamic)
   - When user clicks a town from the table, populate:
     - Town name, Region, 6-cycle history graph
     - Current prices (3 cards: PMS | Diesel | Kerosene)
     - Percentile rank (e.g., "Most expensive for PMS: Top 15%")
     - Price vs. national/regional avg (% diff)
     - Trend sparkline (last 6 cycles)

4. **Price Distribution by Town Tier**
   - Histogram: X-axis = price bins, Y-axis = frequency
   - Segment by town tier (Metro, Secondary, Rural)
   - Show how pricing differs across settlement types

5. **"Price Jumpers" Alert Table**
   - Towns with largest price increases in current cycle
   - Columns: Town | Region | Previous Cycle Avg | Current Cycle Avg | Change | Change %
   - Conditional formatting: Gradient (green to red)
   - "Flag for analysis" checkbox column

**Filters:**
- Fuel Type
- Region
- Settlement Type (Metro / Secondary / Rural)
- Price Range Slider (e.g., only show towns 200–250 KES)

---

### **Page 5: Consumer Impact & Affordability**
**Purpose:** Socioeconomic lens, accessibility analysis

**Components:**

1. **Affordability Index Gauge** (Primary KPI)
   - Single large gauge: Affordability Index (0–100)
   - Green zone: 70–100 (affordable)
   - Yellow zone: 40–70 (moderate)
   - Red zone: 0–40 (unaffordable)
   - Calculation: Based on fuel prices vs. household income proxy (optional: blend with external income data)

2. **Price vs. Income Ratio Matrix**
   - Y-axis = Regions
   - X-axis = Time (last 6 cycles)
   - Cell value = (Fuel Cost / Avg Income) %
   - Color intensity = burden (high % = more red)

3. **Fuel Type Affordability Comparison**
   - 3 stacked bar charts (side-by-side):
     - Metro zones | Secondary towns | Rural areas
   - Stacks: PMS | Diesel | Kerosene (% of household budget estimate)
   - Hover: Show absolute KES amount and % of income

4. **Time to Fill Tank** Analysis Card
   - Assumes 50L tank for typical vehicle
   - Calculates: Cost = Price × 50L
   - Visualize: "Fill-up cost in KES over time" line chart
   - Annotate: "Average mechanic salary" horizontal line (external benchmark)

5. **Regional Affordability Scorecard**
   - Table: Region | Affordability Score | Trend | Alert
   - Color-coded by quintile
   - Red flag: Regions where affordability dropped >5% YoY

**Filters:**
- Fuel Type
- Settlement Type
- Time Period (Last cycle / Last 3 cycles / Last year)

---

### **Page 6: Supply Chain & Distribution**
**Purpose:** Logistics perspective, stock/supply efficiency

**Components:**

1. **Price Correlation with Distance from Nairobi** (If data available)
   - Scatter plot: X = Distance from capital | Y = Price
   - Size = town population
   - Color = region
   - Trend line + R² value
   - Insight: Show transport cost impact

2. **Distribution Hub Analysis** (Optional)
   - Map: Major hub locations (Nairobi, Mombasa, Kisumu, etc.)
   - Concentric circles: Price impact zones (price decay with distance)
   - Toggle: Show/hide by fuel type

3. **Supply Disruption Alerts** (Anomaly Detection)
   - Table: Flag when regional prices spike >10% unexpectedly
   - Columns: Date | Region | Fuel | Price | Expected | Alert Reason (e.g., "Supply chain disruption detected")
   - DAX logic: Compares actual vs. predicted based on seasonal patterns

4. **Transportation Cost Proxy**
   - If coast/rural markup exists: Bar chart showing regional pricing variance
   - Hypothesis test visualization: Regions with >15% premium flagged as "high transport cost zones"

5. **Stock Availability Index** (If future data becomes available)
   - Placeholder or skeleton for: Reporting towns count, data freshness %

**Filters:**
- Region
- Time Period
- Alert Severity (High / Medium / Low)

---

### **Page 7: Executive Summary & KPI Dashboard**
**Purpose:** Print-ready, boardroom-focused single pager

**Components:**

1. **Header Section**
   - Large logo (EPRA Fuel Intelligence)
   - Report date: "As of [Latest Cycle Date]"
   - Refresh timestamp: "Updated: [Timestamp] UTC"

2. **Top 6 KPIs in Large Cards**
   - Current National Average Price (All Fuels)
   - National Price Index (Base 100)
   - Highest Regional Premium (%)
   - Affordability Score
   - Data Coverage (% of towns reporting)
   - Forecast Confidence (%)

3. **Key Insights Panel** (3–5 bullet points, DAX-generated)
   - Auto-populate top insights:
     - "PMS up 2.3% from previous cycle"
     - "Rural areas show 8.5% premium vs. metro"
     - "Forecast: Prices likely stable next cycle (±1%)"
     - "Affordability declined in [X] regions"

4. **Top 3 Risks Summary**
   - Risk 1: [Narrative] | Action: [Recommendation]
   - Risk 2: [Narrative] | Action: [Recommendation]
   - Risk 3: [Narrative] | Action: [Recommendation]

5. **Footer with Data Quality Notes**
   - "Data sourced from [N] towns across [N] regions"
   - "Pipeline refresh: Daily (15th–31st of month)"
   - "Next update: [Date]"

**Filters:** None (static summary page, or optional date range)

---

### **Page 8: Data Quality & Monitoring**
**Purpose:** Transparency, pipeline health, metadata

**Components:**

1. **Pipeline Health Dashboard**
   - Large status indicator (🟢 Healthy / 🟡 Warning / 🔴 Error)
   - Last successful run: [timestamp]
   - Data freshness: "Latest data: [X] days old"
   - Next scheduled run: [timestamp]

2. **Data Completeness Heatmap**
   - Rows = Regions
   - Columns = Fuel types
   - Cell color = % of towns reporting data (100% = full green, <100% = yellow/red)
   - Hover: Show count (e.g., "215 of 223 towns reporting")

3. **Town Coverage Trend**
   - Line chart: X = Date, Y = # towns reporting
   - Target line: 223 towns
   - Show any gaps or coverage drops

4. **Data Anomaly Report**
   - Table: Date | Region | Town | Fuel | Issue (Null value / Out of range / Duplicate)
   - Action column: "Auto-corrected" / "Flagged for manual review"
   - Color: Green (resolved) / Yellow (pending)

5. **Processing Metrics**
   - Card 1: "Avg load time: 2.4 min"
   - Card 2: "Data validation pass rate: 99.8%"
   - Card 3: "ETL job success rate: 100%"
   - Card 4: "Last error: None (7 days)"

6. **Model Lineage / Metadata**
   - Text box: "Source: EPRA pump prices | Grain: Town × Fuel × Cycle | Dimensions: Date, Location, Fuel"
   - "Last schema update: [Date] | dbt version: [X.X.X]"

**Filters:**
- Time Period (Last 30 days / 90 days / All time)
- Severity (All / Warnings / Errors)

---

## Advanced Power BI Features to Implement

### **1. DAX Measures Library** (Core)
Create a `_Measures` table with calculated columns:

```dax
-- Basic Measures
Current Price PMS = CALCULATE(
    AVERAGE(fact_fuel_prices[price]),
    FILTER(dim_fuel, dim_fuel[fuel_code] = "PMS")
)

Month over Month % Change = DIVIDE(
    [Current Month Sales] - [Previous Month Sales],
    [Previous Month Sales]
)

Price Percentile Rank = RANKX(
    ALL(dim_location[town]),
    [Current Price],
    , DESC
)

Affordability Index = 100 - ([Current Price] / MAX([Price Range]) * 100)

Forecast Next Cycle = FORECAST.LINEAR(
    MAX(dim_date[date_key]),
    VALUES(fact_fuel_prices[price]),
    VALUES(dim_date[date_key])
)

Data Completeness % = DIVIDE(
    COUNTA(fact_fuel_prices[location_key]),
    223  -- total towns
)
```

### **2. Drill-Through Pages**
- From ranking table → click town → drill to location detail page
- From heatmap → click region → drill to regional deep dive
- From anomaly table → click flag → drill to diagnostics

### **3. Advanced Tooltips**
- On KPI cards: Show 3-month trend sparkline + MoM change %
- On heatmap cells: Show top/bottom 3 towns in that region for that fuel
- On trend lines: Show forecast band + next cycle prediction

### **4. Custom Visuals** (Optional Premium)
- `Variance Chart` (visually show target vs. actual)
- `Competitor Matrix` (plot regions on 2D chart: affordability vs. volatility)
- `Waterfall Chart` (show price decomposition: national base + regional premium)

### **5. Bookmarks & Navigation**
- Bookmark: "Focus on Nairobi" (auto-filters all pages to Nairobi)
- Bookmark: "Affordability Deep Dive" (hides price visuals, shows affordability visuals)
- Bookmark: "Regional Benchmark View"
- Nav buttons: Back / Forward / Home

### **6. RLS (Row-Level Security)** (Enterprise)
- Role: "Regional Manager" → sees only their region
- Role: "National Analyst" → sees all data
- Implement via `[Region] = USERNAME()`

### **7. Q&A / AI Visuals** (If Premium)
- Q&A visual: Users type questions like "Which region has highest fuel prices?"
- Natural language queries → auto-generate charts

### **8. Export & Subscription**
- "Export to PDF" button → downloads dashboard to file (for email)
- Email subscriptions: Daily executive summary
- Power BI alerts: "PMS price exceeded 220 KES"

---

## Color Palette & Branding

### **Recommended Theme:**
Keep your beige/coral, but formalize:

| Element | Color | Hex |
|---------|-------|-----|
| Primary Accent (Fuel Type highlights) | Coral/Orange | #E8977B |
| Secondary Accent (Diesel) | Teal | #4CA6A0 |
| Tertiary Accent (Kerosene) | Navy Blue | #2C3E50 |
| Background | Cream/Beige | #F5F2ED |
| Text (Primary) | Dark Gray | #2D2D2D |
| Text (Secondary) | Medium Gray | #757575 |
| Success/Green | Sage Green | #6FA876 |
| Warning/Yellow | Amber | #FFA500 |
| Alert/Red | Coral Red | #D46A54 |
| Neutral Grid | Light Gray | #E8E5E0 |

---

## Implementation Roadmap

### **Phase 1: Quick Wins (Week 1)**
- ✅ Expand KPI section (add MoM %, affordability, forecast)
- ✅ Add advanced tooltips to existing visuals
- ✅ Create "Price Volatility" ribbon chart
- ✅ Build "Top Changers" pill chart
- Estimated effort: 6–8 hours

### **Phase 2: Core Pages (Week 2–3)**
- ✅ Page 2: Trends & Forecasting (with DAX forecast)
- ✅ Page 3: Regional Benchmarking & Outliers
- ✅ Page 4: Location Deep Dive
- ✅ Page 8: Data Quality Monitoring
- Estimated effort: 16–20 hours

### **Phase 3: Advanced Features (Week 4)**
- ✅ Page 5: Consumer Impact & Affordability
- ✅ Page 6: Supply Chain (if data available)
- ✅ Page 7: Executive Summary (print-ready)
- ✅ Add drill-through pages
- ✅ Implement bookmarks & navigation
- Estimated effort: 12–16 hours

### **Phase 4: Polish & Enterprise (Week 5)**
- ✅ Custom theme/branding pass
- ✅ RLS setup (optional)
- ✅ Q&A visual + AI features (optional)
- ✅ Email subscription setup
- ✅ Power BI alerts
- Estimated effort: 8–12 hours

---

## DAX Snippets for Key Measures

```dax
-- 1. Price Index (Base = First Date in Selection)
Price Index = DIVIDE(
    [Current Average Price],
    CALCULATE(
        [Current Average Price],
        FILTER(ALL(dim_date), dim_date[date_key] = MIN(dim_date[date_key]))
    )
) * 100

-- 2. Volatility (Std Dev of last N cycles)
Price Volatility = STDEV.P(
    CALCULATE(
        [Current Average Price],
        DATESBETWEEN(dim_date[full_date], TODAY()-90, TODAY())
    )
)

-- 3. Affordability Index (Inverse of Price Percentile)
Affordability Index = 100 - PERCENTILE.INC(
    ALL(fact_fuel_prices[price]),
    [Current Average Price]
)

-- 4. Regional Premium (Region Avg vs National Avg)
Regional Premium % = DIVIDE(
    [Regional Average Price] - [National Average Price],
    [National Average Price]
) * 100

-- 5. Forecast (Simple exponential smoothing)
Price Forecast Next Cycle = 
VAR LastPrice = [Current Average Price]
VAR PreviousPrice = CALCULATE(
    [Current Average Price],
    DATEADD(dim_date[full_date], -30, DAY)
)
RETURN LastPrice + (LastPrice - PreviousPrice) * 0.5
```

---

## Success Metrics for Masterclass Status

✅ **Technical:**
- [ ] 8 pages, each with 3–5 distinct visualizations
- [ ] 15+ DAX measures (beyond basic SUM/AVG)
- [ ] Drill-through pages implemented
- [ ] Advanced tooltips on 80% of visuals
- [ ] Forecasting model with 90%+ accuracy

✅ **Usability:**
- [ ] Page load time <3 seconds
- [ ] Mobile-responsive layout (if applicable)
- [ ] Intuitive filtering (max 5 filters per page)
- [ ] Clear KPI hierarchy (hero metrics + supporting)
- [ ] Bookmarks for common use cases (5–10 bookmarks)

✅ **Business:**
- [ ] Actionable insights (top 3 per page)
- [ ] Exec summary exports < 1 page
- [ ] RLS for different user roles
- [ ] Email subscription setup
- [ ] On-premise or cloud deployment tested

---

## Next Steps

1. **Create Sketch:** Draft wireframes for pages 2–8 (use PowerPoint or Figma)
2. **Build Measures:** Implement DAX library in Power BI (start with 5–10 core measures)
3. **Connect Data:** Set up live connection to PostgreSQL/BigQuery (refresh policy: hourly)
4. **Design Visuals:** Page by page, starting with Page 2 (Trends & Forecasting)
5. **Test & Iterate:** Gather feedback, iterate, polish
6. **Deploy:** Publish to Power BI Service, enable refresh, set up alerts

---

## Reference: Current vs. Masterclass

| Feature | Current | Masterclass |
|---------|---------|-------------|
| Pages | 3 | 8 |
| Visualizations | ~12 | 40+ |
| DAX Measures | ~3 | 15+ |
| Interactivity | Basic filters | Drill-through, bookmarks, Q&A |
| Forecasting | None | 3-cycle ahead prediction |
| Anomaly Detection | None | Outlier flagging + alerts |
| RLS | No | Yes (by region/role) |
| Export/Subscribe | Manual | Automated (PDF + email) |
| Data Quality Monitoring | None | Dedicated page + alerts |
| Mobile Responsive | Partial | Full |

---

## Estimated Total Build Time

- **Quick Wins:** 8 hours
- **Core Pages:** 20 hours
- **Advanced Features:** 14 hours
- **Polish & Enterprise:** 10 hours
- **Testing & Iteration:** 8 hours

**Total: ~60 hours** (2–3 weeks full-time, or 4–6 weeks part-time)

---

**Happy building! This will be a portfolio showcase.** 🚀
