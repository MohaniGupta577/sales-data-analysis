# ================================================================
# Sales Data Analysis — analyse.py
# Author  : Mohani Gupta | mohanigupta279@gmail.com
# Purpose : Statistical analysis and key business question answers
# ================================================================

import pandas as pd
import numpy as np


def run_analysis(df: pd.DataFrame) -> None:
    """Run and print all key business analyses."""

    sep = "=" * 58

    # ── OVERVIEW ─────────────────────────────────────────────
    print(f"\n{sep}")
    print("  SALES PERFORMANCE ANALYSIS  —  Mohani Gupta")
    print(sep)

    total_rev    = df["revenue"].sum()
    total_profit = df["profit"].sum()
    margin       = total_profit / total_rev * 100 if total_rev else 0

    print(f"\n{'📊 SUMMARY':}")
    print(f"  Total Revenue   : ₹{total_rev:>15,.2f}")
    print(f"  Total Profit    : ₹{total_profit:>15,.2f}")
    print(f"  Profit Margin   : {margin:>6.1f}%")
    print(f"  Unique Orders   : {df['order_id'].nunique():>15,}")
    avg_ov = df.groupby("order_id")["revenue"].sum().mean()
    print(f"  Avg Order Value : ₹{avg_ov:>15,.2f}")

    # ── BY REGION ────────────────────────────────────────────
    print(f"\n{'🌍 REVENUE BY REGION':}")
    region = (
        df.groupby("region")[["revenue", "profit"]]
        .sum()
        .assign(margin_pct=lambda x: (x["profit"] / x["revenue"] * 100).round(1))
        .sort_values("revenue", ascending=False)
    )
    for reg, row in region.iterrows():
        share = row["revenue"] / total_rev * 100
        print(f"  {reg:<14} ₹{row['revenue']:>12,.0f}  ({share:.1f}%)  "
              f"margin: {row['margin_pct']:.1f}%")

    # ── BY CATEGORY ──────────────────────────────────────────
    print(f"\n{'📦 CATEGORY PERFORMANCE':}")
    cat = (
        df.groupby("category")
        .agg(
            Revenue=("revenue", "sum"),
            Profit=("profit", "sum"),
            Orders=("order_id", "count"),
            Avg_Discount=("discount", "mean"),
        )
        .assign(
            Margin=lambda x: (x["Profit"] / x["Revenue"] * 100).round(1),
            Avg_Discount=lambda x: (x["Avg_Discount"] * 100).round(1),
        )
        .sort_values("Revenue", ascending=False)
    )
    print(cat[["Revenue", "Profit", "Margin", "Orders", "Avg_Discount"]].to_string())

    # ── TOP 5 PRODUCTS ───────────────────────────────────────
    print(f"\n{'🏆 TOP 5 PRODUCTS BY REVENUE':}")
    top5 = (
        df.groupby("product_name")["revenue"]
        .sum()
        .nlargest(5)
    )
    for i, (prod, rev) in enumerate(top5.items(), 1):
        print(f"  {i}. {prod[:40]:<40} ₹{rev:>10,.0f}")

    # ── YEARLY GROWTH ────────────────────────────────────────
    print(f"\n{'📅 YEARLY REVENUE GROWTH':}")
    yearly = df.groupby("year")["revenue"].sum().sort_index()
    for i, (yr, rev) in enumerate(yearly.items()):
        if i == 0:
            print(f"  {yr}: ₹{rev:>12,.0f}")
        else:
            prev = yearly.iloc[i - 1]
            g    = (rev - prev) / prev * 100
            print(f"  {yr}: ₹{rev:>12,.0f}  (YoY: {g:+.1f}%)")

    # ── DISCOUNT IMPACT ──────────────────────────────────────
    print(f"\n{'💸 DISCOUNT IMPACT ON PROFIT':}")
    df["disc_bucket"] = pd.cut(
        df["discount"],
        bins=[0, 0.1, 0.2, 0.3, 0.5, 1.01],
        labels=["0–10%", "10–20%", "20–30%", "30–50%", "50%+"],
        right=False
    )
    disc = (
        df.groupby("disc_bucket", observed=True)
        .agg(Avg_Profit=("profit", "mean"), Order_Count=("order_id", "count"))
        .round(2)
    )
    print(disc.to_string())

    # ── SEASONALITY ──────────────────────────────────────────
    print(f"\n{'🗓️  QUARTERLY REVENUE SHARE':}")
    qtr = (
        df.groupby(["year", "quarter"])["revenue"]
        .sum()
        .reset_index()
    )
    for _, row in qtr.iterrows():
        share = row["revenue"] / total_rev * 100
        print(f"  {int(row['year'])} Q{int(row['quarter'])}: "
              f"₹{row['revenue']:>12,.0f}  ({share:.1f}%)")


if __name__ == "__main__":
    df = pd.read_csv(
        "data/processed/sales_cleaned.csv",
        parse_dates=["order_date"]
    )
    run_analysis(df)
