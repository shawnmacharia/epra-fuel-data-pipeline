# DAX Measures Implementation Guide for Power BI

## Overview
This guide explains how to implement the 100+ DAX measures in your Power BI model.

---

## Step 1: Create a Measures Table (Best Practice)

### Option A: Dedicated Measures Table (Recommended)
1. In Power BI Desktop, go to **Home → Enter Data**
2. Create a table named `_Measures` with columns:
   - `MeasureCategory` (text)
   - `MeasureName` (text)
   - `Description` (text)

Example rows:
| MeasureCategory | MeasureName | Description |
|-----------------|-------------|-------------|
| Prices | Current PMS Price | Latest PMS price average |
| Prices | Current Diesel Price | Latest Diesel price average |
| Trends | MoM Change PMS % | Month-over-month % change |
| Affordability | Affordability Index | 0-100 scale affordability |

### Option B: Hide from Model (Alternative)
Keep measures in a hidden table, then reference them across the model.

---

## Step 2: Import Measures into Power BI

### Method 1: Copy-Paste (Simple)
1. Open `DAX_MEASURES_LIBRARY.txt`
2. Copy each measure code
3. In Power BI: **Home → New Measure**
4. Paste the DAX code
5. Press Enter

### Method 2: Use Tabular Editor (Faster)
1. Install **Tabular Editor** (free, from Marketplace)
2. Open your .pbix in Tabular Editor
3. Right-click on your model → **New Table** → name it `_Measures`
4. Paste all measures into Tabular Editor's DAX editor
5. Save and refresh in Power BI Desktop

### Method 3: DAX Studio (Advanced)
1. Install **DAX Studio** (open source)
2. Connect to your model
3. Use script execution to bulk-create measures
4. Reference the SQL/DAX script file

---

## Step 3: Organize Measures by Category

Create a hierarchy in your model:

```
_Measures (Display Folder: Off)
├── 1. Prices
│   ├── Current PMS Price
│   ├── Current Diesel Price
│   ├── Current Kerosene Price
│   └── Current Average Price
├── 2. MoM Changes
│   ├── MoM Change PMS %
│   ├── MoM Change Diesel %
│   └── MoM Direction
├── 3. Rankings & Percentiles
│   ├── Price Percentile Rank
│   ├── Price Rank
│   └── Price Percentile Bucket
├── 4. Volatility
│   ├── Price Volatility
│   ├── PMS Volatility
│   └── Price Volatility Coefficient
├── 5. Regional Measures
│   ├── National Average Price
│   ├── Regional Average Price
│   └── Regional Premium %
├── 6. Affordability
│   ├── Affordability Index
│   ├── Affordability Rating
│   └── Fill Up Cost (50L)
├── 7. Trends & Forecasting
│   ├── Forecast Next Cycle
│   ├── Forecast Lower Bound
│   ├── Forecast Upper Bound
│   └── YoY Change %
├── 8. Anomalies
│   ├── Price Z Score
│   ├── Is Outlier
│   └── Is Price Jump
├── 9. Data Quality
│   ├── Towns Reported
│   ├── Data Completeness %
│   └── Data Quality Score
├── 10. Regional Aggregations
│   ├── Region Count
│   ├── Regional Price Spread
│   └── Most Expensive Region
├── 11. Fuel Comparisons
│   ├── Fuel Average Price
│   ├── PMS vs Diesel Diff
│   └── Most Expensive Fuel
├── 12. Historical Averages
│   ├── 3 Cycle Average
│   ├── 6 Cycle Average
│   └── 12 Cycle Average
├── 13. Price Indices
│   ├── Price Index (Base = First Date)
│   └── Price Index (Base = 12M Avg)
├── 14. Narratives
│   ├── Highest Price Location
│   ├── Lowest Price Location
│   └── Key Insight Narrative
├── 15. Supply Chain
│   ├── Estimated Transport Premium
│   └── Transport Cost Impact
└── 16. Status Indicators
    ├── Price Status Color
    └── Dashboard Status
```

**To set display folders in Power BI:**
1. Right-click measure → **Properties**
2. Set **Display Folder** (e.g., "1. Prices")
3. Click OK

---

## Step 4: Validate Measures

After importing all measures:

1. **Check for errors:**
   - Go to **Model view**
   - Look for ⚠️ warning icons next to measures
   - Hover to see error details

2. **Test on a visual:**
   - Create a table or card visual
   - Drag each measure to it
   - Verify calculations look reasonable
   - Check for BLANK() or ERROR results

3. **Compare with source data:**
   - Spot-check a few calculations manually
   - Verify MoM change % matches expected
   - Confirm price ranges are sensible

---

## Step 5: Create Supporting Columns (Optional)

Some visuals benefit from helper columns in your dimension tables:

### In `dim_date`:
```dax
Date Label = FORMAT(dim_date[full_date], "MMM dd, yyyy")
Month Name = FORMAT(dim_date[full_date], "MMMM")
Month Year = FORMAT(dim_date[full_date], "MMM yyyy")
Year = YEAR(dim_date[full_date])
Cycle Number = MONTH(dim_date[full_date]) -- Proxy for pricing cycle
```

### In `dim_location`:
```dax
Town Rank by Price = RANKX(ALL(dim_location[town]), [Current Average Price],, DESC)
Region Town Count = CALCULATE(DISTINCTCOUNT(dim_location[town]), FILTER(ALL(dim_location), dim_location[region] = [region]))
Town Settlement Type = IF([town] IN {"Nairobi", "Mombasa", "Kisumu", "Nakuru"}, "Metro", IF([town] IN {"...secondary towns..."}, "Secondary", "Rural"))
```

---

## Step 6: Create Calculated Tables (Optional)

For advanced filtering/drill-through:

### Top 10 Most Expensive Towns:
```dax
Top 10 Expensive Towns = 
TOPN(
    10,
    SUMMARIZE(dim_location, dim_location[town], dim_location[region]),
    [Current Average Price],
    DESC
)
```

### Regional Summary:
```dax
Regional Summary = 
SUMMARIZE(
    dim_location,
    dim_location[region],
    "Avg Price", [Region Average Price],
    "Town Count", DISTINCTCOUNT(dim_location[town]),
    "Premium %", [Regional Premium %]
)
```

---

## Step 7: Performance Tuning

If your model is slow:

1. **Check measure complexity:**
   - Measures with nested CALCULATE() are slower
   - Consider converting complex measures to `SUMMARIZECOLUMNS()` alternatives

2. **Reduce context transitions:**
   - Avoid FILTER() inside CALCULATE() when possible
   - Use ALL() for entire table operations instead of filtering

3. **Test refresh time:**
   - Create a bookmark to test: **View → Bookmarks → Edit Bookmark**
   - Check DirectQuery vs. Import settings

4. **Use query folding (if applicable):**
   - Ensure data source can push down calculations
   - Verify in Power Query editor

---

## Step 8: Document Your Measures

Create a **Measures Dictionary** (Excel or PDF):

| Measure Name | Formula | Category | Business Logic | Used In (Page) |
|--------------|---------|----------|-----------------|----------------|
| Current PMS Price | CALCULATE(AVERAGE...) | Prices | Avg PMS price in current cycle | Executive, Trends |
| MoM Change PMS % | DIVIDE(...) / ... * 100 | Changes | Percentage change vs previous cycle | Executive, Summary |
| Affordability Index | 100 - DIVIDE(...) | Affordability | 0-100 scale, 100 = most affordable | Affordability, Summary |

---

## Step 9: Testing Scenarios

Test each measure with these scenarios:

### Scenario 1: All Data Selected
- Expected: National-level aggregation
- Verify: Matches manual calculation

### Scenario 2: Single Region Filter
- Expected: Region-level aggregation
- Verify: Regional Premium % correct

### Scenario 3: Single Town Filter
- Expected: Town-level detail
- Verify: Price matches source data

### Scenario 4: Single Fuel Type Filter
- Expected: Fuel-specific metrics only
- Verify: MoM change correct for that fuel

### Scenario 5: Empty Selection
- Expected: BLANK() or 0 (depends on measure)
- Verify: No error messages

---

## Step 10: Measure Dependencies (Important)

Some measures depend on others. Build them in this order:

1. **Core Prices** (Current/Previous prices)
2. **Aggregations** (National, Regional, Fuel)
3. **Changes** (MoM %, YoY %)
4. **Volatility** (Std Dev, Z-Score)
5. **Derived Metrics** (Percentile, Index, Affordability)
6. **Outliers** (Is Outlier, Price Jump)
7. **Narratives** (Auto-generated text)

---

## Quick Reference: Measures by Page

### **Page 1: Executive Dashboard**
- Current PMS/Diesel/Kerosene Price (4 cards)
- MoM Change % (4 cards with sparklines)
- Affordability Index (gauge)
- Towns Reported
- Dashboard Status
- Price Status Color (conditional formatting)
- Key Insight Narrative (text box)

### **Page 2: Trends & Forecasting**
- Current Average Price (line chart)
- Forecast Next Cycle + bounds (trend line)
- YoY Change %
- 3/6/12 Cycle Average
- Price Volatility Coefficient
- Price Index variants

### **Page 3: Regional Benchmarking**
- Regional Average Price (heatmap)
- Regional Premium %
- Price Z Score (outlier detection)
- Is High Variance Region
- National Average Price (reference line)
- Region Price Variance (box plot)

### **Page 4: Location Deep Dive**
- Price Rank / Price Rank Ascending (table)
- Price Percentile Rank (table)
- Current Average Price (table)
- MoM Change % (table)
- Price Percentile Bucket (table)
- Price Status Color (conditional format)

### **Page 5: Affordability**
- Affordability Index (gauge, multiple by region)
- Affordability Rating (text label)
- Fill Up Cost (50L) (card)
- Fill Up Cost Change (card)
- Affordability Index (Inverse Percentile) (alternative)

### **Page 6: Supply Chain**
- Estimated Transport Premium (map color)
- Transport Cost Impact (scatter plot)
- Regional Premium % (bar chart)
- Most Expensive / Cheapest Region

### **Page 7: Executive Summary**
- All KPIs (frozen for export)
- Data Quality Score
- Key Insight Narrative

### **Page 8: Data Quality**
- Data Completeness %
- Towns Reported
- Data Quality Score
- Data Freshness Days
- Null Count
- Dashboard Status

---

## Common Issues & Solutions

### Issue 1: Circular Dependency Error
**Symptom:** "The formula contains a circular reference."
**Solution:** Check if measure A calls measure B, and measure B calls measure A. Break cycle by inlining one formula.

### Issue 2: Measure Returns BLANK()
**Symptom:** Visual shows no data.
**Solution:** 
- Verify filters are not too restrictive
- Check if data exists in fact table for current selection
- Use IFERROR() to debug: `IFERROR([Your Measure], "Error")`

### Issue 3: Very Slow Performance
**Symptom:** Visual takes >2 seconds to load.
**Solution:**
- Reduce complexity (avoid nested CALCULATE)
- Use TOPN() instead of ALL() + FILTER where possible
- Consider Query Folding in source data
- Move to DirectQuery if data size >1GB

### Issue 4: Percentage Shows as Decimal
**Symptom:** 5% shows as 5 instead of 0.05.
**Solution:** Format the measure as **Percentage** in Power BI (not multiply by 100 in DAX).

---

## Advanced: Creating Measure Groups

For enterprise deployments, organize measures by business domain:

```
Sales & Revenue
├── Total Revenue
├── Revenue YoY %
└── Revenue Forecast

Customer Metrics
├── Customer Count
├── Repeat Customer %
└── Customer Churn

Operational Metrics
├── Data Quality Score
├── Pipeline Health
└── SLA Compliance
```

Use **Display Folder** to create these hierarchies (see Step 3).

---

## Performance Benchmarks

Typical measure performance (on PostgreSQL/BigQuery with 50K rows):

| Measure Type | Typical Time | Acceptable Range |
|--------------|--------------|------------------|
| Simple SUM/AVG | <100ms | <200ms |
| CALCULATE with single filter | 100-300ms | <500ms |
| Percentile/Rank | 200-500ms | <1000ms |
| Z-Score/Complex | 300-800ms | <1500ms |
| Forecast | 500-1500ms | <2000ms |

If your measures exceed these, optimize!

---

## Next Steps

1. ✅ Import all 100+ measures
2. ✅ Validate each measure returns sensible values
3. ✅ Test with different filter scenarios
4. ✅ Document in Excel (Measures Dictionary)
5. ✅ Create page-by-page visual layout
6. ✅ Build visuals using measures
7. ✅ Test drill-through and bookmarks
8. ✅ Performance tune if needed
9. ✅ Publish to Power BI Service
10. ✅ Set up refresh schedule & alerts

---

**Happy Power BI-ing! 📊**
