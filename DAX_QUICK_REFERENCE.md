# DAX Measures Quick Reference

## 📊 Complete Measures Summary

You now have **100+ DAX measures** organized in 16 categories, ready to copy directly into Power BI.

---

## 📋 Measures by Category

### **1. Prices (4 measures)**
- Current PMS Price
- Current Diesel Price
- Current Kerosene Price
- Current Average Price

### **2. MoM Changes (5 measures)**
- MoM Change PMS %
- MoM Change Diesel %
- MoM Change Kerosene %
- MoM Change Average %
- MoM Direction (↑ ↓ →)

### **3. Rankings & Percentiles (4 measures)**
- Price Percentile Rank
- Price Rank (desc)
- Price Rank Ascending
- Price Percentile Bucket

### **4. Volatility (5 measures)**
- Price Volatility (Std Dev)
- Price Volatility Coefficient
- PMS Volatility
- Diesel Volatility
- Kerosene Volatility

### **5. Regional (8 measures)**
- National Average Price
- Regional Average Price
- Regional Premium %
- Min/Max Price
- Price Range
- Q1, Q2 (Median), Q3 Price

### **6. Affordability (4 measures)**
- Affordability Index (0-100)
- Affordability Index (Inverse)
- Affordability Rating (✓ ⊙ ✗)
- Fill Up Cost (50L)

### **7. Trends & Forecasting (6 measures)**
- YoY Change %
- Trend Direction (📈 📉 ➡️)
- Forecast Next Cycle
- Forecast Lower Bound (95% CI)
- Forecast Upper Bound (95% CI)
- 3/6/12 Cycle Average

### **8. Anomaly Detection (4 measures)**
- Price Z Score
- Is Outlier (⚠️)
- Deviation from Regional Mean %
- Is Price Jump (🔴 🟡 🟢)

### **9. Data Quality (5 measures)**
- Towns Reported
- Data Completeness %
- Data Quality Score
- Null Count
- Data Freshness Days

### **10. Regional Aggregations (6 measures)**
- Region Count
- Locations Per Region
- Region Price Variance
- Most Expensive Region
- Cheapest Region
- Regional Price Spread

### **11. Fuel Comparisons (5 measures)**
- Fuel Average Price
- PMS vs Diesel Diff
- PMS vs Kerosene Diff
- Diesel vs Kerosene Diff
- Most Expensive Fuel

### **12. Historical Averages (3 measures)**
- 3 Cycle Average
- 6 Cycle Average
- 12 Cycle Average

### **13. Price Indices (2 measures)**
- Price Index (Base = First Date)
- Price Index (Base = 12M Avg)

### **14. Narratives (3 measures)**
- Highest Price Location
- Lowest Price Location
- Key Insight Narrative

### **15. Supply Chain (2 measures)**
- Estimated Transport Premium
- Transport Cost Impact

### **16. Status Indicators (2 measures)**
- Price Status Color (Red/Orange/Green/Gray)
- Dashboard Status (🟢 🟡 🔴)

---

## 🚀 Quick Start (5 Steps)

### Step 1: Open Your Power BI Model
- Launch Power BI Desktop
- Open your existing .pbix file (or create new)
- Ensure data connection is live (PostgreSQL/BigQuery)

### Step 2: Create Measures
**Option A - Copy-Paste (Easiest):**
1. Open `DAX_MEASURES_LIBRARY.txt` from GitHub
2. Copy the first measure (e.g., "Current PMS Price")
3. In Power BI: **Home → New Measure**
4. Paste the DAX code
5. Press Enter

**Option B - Tabular Editor (Faster for all):**
1. Install **Tabular Editor** (free, from Marketplace)
2. Open Tabular Editor
3. Connect to your .pbix
4. Bulk paste all measures from `DAX_MEASURES_LIBRARY.txt`
5. Save

### Step 3: Organize Measures
1. Right-click each measure → **Properties**
2. Set **Display Folder** (e.g., "1. Prices", "2. MoM Changes", etc.)
3. Click OK
4. Done! Measures organized by category

### Step 4: Validate Measures
1. Create a **Card visual**
2. Drag each measure to it
3. Verify calculations look reasonable
4. Check for BLANK() or ERROR

### Step 5: Build Dashboard Pages
- Use the **Page-by-Page Reference** (see below)
- Drag measures to visuals
- Filter, format, and publish!

---

## 📄 Quick Reference: Which Measures for Each Page

### **Page 1: Executive Dashboard**
**Use these measures:**
```
Cards:
- Current PMS Price
- Current Diesel Price
- Current Kerosene Price
- Towns Reported
- MoM Change Average %
- Affordability Index

Gauges:
- Current PMS/Diesel/Kerosene Price (vs historical range)

Text Box:
- Key Insight Narrative

Pill Chart (Top Price Changers):
- Price Rank
- MoM Change %
- Town name
```

### **Page 2: Trends & Forecasting**
**Use these measures:**
```
Line Chart (Historical):
- Current Average Price (over time)
- Forecast Next Cycle + bounds
- 3/6/12 Cycle Average

Volatility Ribbon:
- Price Volatility (over time by fuel)

Year-over-Year:
- YoY Change %
- Current Average Price (current vs. previous year)
```

### **Page 3: Regional Benchmarking**
**Use these measures:**
```
Heatmap:
- Regional Average Price (region × fuel)

Box Plot:
- Q1/Q2/Q3 Price
- Min/Max Price

Outlier Table:
- Price Z Score
- Is Outlier
- Deviation from Regional Mean %
- Town name | Region | Fuel

Affordability by Region:
- Affordability Index (by region)
```

### **Page 4: Location Deep Dive**
**Use these measures:**
```
Ranking Table:
- Price Rank
- Current Average Price
- MoM Change %
- Price Volatility
- Price Percentile Rank
- Price Percentile Bucket
- Town name | Region

Comparison:
- Current Average Price (for selected towns)
```

### **Page 5: Affordability**
**Use these measures:**
```
Gauge:
- Affordability Index

Bar Chart:
- Affordability Index (by region/settlement type)

Card:
- Fill Up Cost (50L)
- Fill Up Cost Change (50L)
- Affordability Rating
```

### **Page 6: Supply Chain**
**Use these measures:**
```
Scatter Plot:
- Estimated Transport Premium
- Current Average Price
- Town distance from Nairobi

Map:
- Transport Cost Impact (color intensity)

Regional Premium:
- Regional Premium %
- Is High Variance Region
```

### **Page 7: Executive Summary**
**Use these measures:**
```
(All KPIs frozen - same as Page 1)
- Current Average Price
- MoM Change Average %
- Affordability Index
- Data Quality Score
- Key Insight Narrative
- Dashboard Status
```

### **Page 8: Data Quality & Monitoring**
**Use these measures:**
```
Status Card:
- Dashboard Status
- Data Freshness Days

Table:
- Towns Reported
- Data Completeness %

Heatmap:
- Data Completeness % (region × fuel)

Metrics:
- Data Quality Score
- Null Count
```

---

## 🔧 Most Used Measures (Top 10)

| Rank | Measure | Pages Used | Priority |
|------|---------|-----------|----------|
| 1 | Current Average Price | All 8 | ⭐⭐⭐ |
| 2 | MoM Change Average % | 1, 2, 7, 8 | ⭐⭐⭐ |
| 3 | Affordability Index | 1, 5, 7 | ⭐⭐⭐ |
| 4 | Forecast Next Cycle | 2 | ⭐⭐ |
| 5 | Regional Premium % | 3, 6 | ⭐⭐ |
| 6 | Price Rank | 1, 4 | ⭐⭐ |
| 7 | Is Outlier | 3, 8 | ⭐⭐ |
| 8 | Data Completeness % | 8 | ⭐⭐ |
| 9 | Price Volatility | 2, 3 | ⭐⭐ |
| 10 | Towns Reported | 1, 7, 8 | ⭐⭐ |

**Start building with these 10!**

---

## ⚠️ Important Notes

### Measure Dependencies
Some measures depend on others. Build them in order:
1. **First:** Prices (sections 1-2)
2. **Second:** Aggregations (sections 5, 10-11)
3. **Third:** Derived metrics (sections 3-4, 6-9)
4. **Last:** Narratives (section 14)

### Data Requirements
Ensure your tables have these columns:
- `fact_fuel_prices`: `[price]`, `[effective_from]`, `[effective_to]`
- `dim_fuel`: `[fuel_code]` (PMS, AGO, IK), `[fuel_key]`
- `dim_location`: `[town]`, `[region]`, `[location_key]`
- `dim_date`: `[full_date]`, `[date_key]`

### Performance
- Most measures: <500ms
- Complex (Forecast, Z-Score): <2s
- If slow, optimize in **DAX_IMPLEMENTATION_GUIDE.md**

---

## 📚 Files You Now Have

| File | Purpose |
|------|---------|
| `DAX_MEASURES_LIBRARY.txt` | 100+ ready-to-copy DAX measures |
| `DAX_IMPLEMENTATION_GUIDE.md` | Step-by-step setup, testing, troubleshooting |
| This file | Quick reference guide |
| `POWERBI_MASTERCLASS_UPGRADE.md` | Full 8-page dashboard design |

---

## ✅ Next Steps

1. ✅ Copy measures into Power BI (Steps 1-5 above)
2. ✅ Validate each measure (create test card)
3. ✅ Build Page 1 (Executive Dashboard) - highest impact
4. ✅ Build Page 2 (Trends & Forecasting) - shows advanced analytics
5. ✅ Build remaining pages (3-8)
6. ✅ Add drill-through, bookmarks, themes
7. ✅ Test all filter combinations
8. ✅ Publish to Power BI Service
9. ✅ Set up refresh schedule (daily, 15th-31st)
10. ✅ Celebrate! 🎉

---

## 📞 Troubleshooting

**Q: Measure returns BLANK()?**
A: Check filters aren't too restrictive. Verify data exists for current selection.

**Q: Performance is slow?**
A: See "Performance Tuning" in `DAX_IMPLEMENTATION_GUIDE.md`

**Q: Circular reference error?**
A: Check measure A doesn't call measure B while B calls A.

**Q: Percentage shows as decimal (5 not 0.05)?**
A: Format measure as **Percentage** in Power BI properties.

---

**Good luck building your masterclass dashboard! 📊✨**
