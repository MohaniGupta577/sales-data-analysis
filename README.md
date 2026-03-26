# 📈 Sales Data Analysis
### End-to-End Pipeline: Cleaning → Analysis → Visualisation | Python · SQL · Matplotlib

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3776AB?style=for-the-badge)
![Seaborn](https://img.shields.io/badge/Seaborn-3776AB?style=for-the-badge)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge)

---

## 📌 Problem Statement

A retail company holds years of sales transaction data in flat CSV files — but no systematic way to understand **what's selling, where revenue is leaking, or what seasonal patterns exist**.

**Goal:** Design a complete, modular Python pipeline to ingest, clean, statistically analyse, and visualise sales data to deliver 10 actionable business insights.

---

## 🎯 Business Questions Answered

1. What is the total revenue, profit, and margin by year?
2. Which region drives the most revenue — and has the worst margin?
3. What is the YoY growth trend and seasonal pattern?
4. Which product categories are most and least profitable?
5. How does discount depth affect profitability?
6. Who are the top 10 revenue-generating products?
7. What is the quarterly revenue distribution?
8. Which ship mode correlates with higher profit?
9. What is the average order value trend?
10. Which sub-categories should be deprioritised?

---

## 📊 Dataset

| Attribute | Detail |
|---|---|
| Source | Simulated retail sales (Superstore-style) |
| Rows | ~30,000 transactions |
| Columns | 15 |
| Format | CSV |

**Key columns:** `order_id`, `order_date`, `ship_date`, `customer_id`, `product_name`, `category`, `sub_category`, `region`, `sales`, `quantity`, `discount`, `profit`, `ship_mode`

---

## 📁 Folder Structure

```
sales-data-analysis/
│
├── data/
│   ├── raw/
│   │   └── sales_data.csv
│   └── processed/
│       └── sales_cleaned.csv
│
├── src/
│   ├── clean.py          ← Data ingestion & cleaning
│   ├── analyse.py        ← Statistical analysis & business Q&A
│   └── visualise.py      ← Chart generation (6 charts)
│
├── outputs/
│   └── charts/           ← All PNG charts saved here
│
├── requirements.txt
└── README.md
```

---

## 💻 Key Code Highlights

### Data Cleaning (`src/clean.py`)
- Drops duplicates on `order_id`
- Parses dates and engineers `year`, `month`, `quarter`, `weekday`
- Fills missing discounts/profits with 0
- Clips discount to valid range [0, 1]
- Derives `revenue`, `profit_margin`, `is_profitable`

### Analysis (`src/analyse.py`)
- Overall KPIs: revenue, profit, margin, avg order value
- Region breakdown with revenue share %
- Category deep-dive: margin, discount, order count
- YoY growth with % delta
- Discount bucket analysis (impact on profit)
- Quarterly seasonality breakdown

### Visualisations (`src/visualise.py`)
| Chart | Type | Insight |
|---|---|---|
| Monthly Revenue Trend | Line + Area | Seasonality peaks |
| Revenue by Region | Horizontal Bar | Top/bottom regions |
| Category Margin | Bubble Scatter | Profitability map |
| Discount Impact | Box Plot | Margin erosion |
| Top 10 Products | Ranked Bar | Revenue concentration |
| Quarterly Heatmap | Seaborn Heatmap | Q4 dominance pattern |

---

## 📈 Key Insights Uncovered

- 💰 **West region** = 38% revenue share but highest return rate
- 📦 **Technology** = 17.2% margin vs Furniture's 2.4% — wide gap
- 🔻 Discounts above **30%** consistently produce **negative profit**
- 📅 **Q4 (Oct–Dec)** drives ~40% of annual revenue — clear seasonality
- 🏆 Top 5 products = **22% of total revenue** — high concentration risk

---

## 🚀 How to Run

```bash
# Clone & setup
git clone https://github.com/mohanigupta/sales-data-analysis.git
cd sales-data-analysis
pip install -r requirements.txt

# Step 1: Clean
python src/clean.py

# Step 2: Analyse
python src/analyse.py

# Step 3: Visualise
python src/visualise.py
```

### `requirements.txt`
```
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
```

---

## 👩‍💻 Author
**Mohani Gupta** | 📧 mohanigupta279@gmail.com | 🔗 [LinkedIn](https://linkedin.com/in/mohanigupta)

⭐ *Star this repo if you found it helpful!*
