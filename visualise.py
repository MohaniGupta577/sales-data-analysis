# ================================================================
# Sales Data Analysis — visualise.py
# Author  : Mohani Gupta | mohanigupta279@gmail.com
# Purpose : Generate and save all analysis charts
# ================================================================

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

sns.set_theme(style="darkgrid", palette="muted", font_scale=1.1)
COLORS = ["#4f8ef7", "#34d399", "#f59e0b", "#ef4444", "#a78bfa"]


def _save(fig: plt.Figure, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ Saved → {path}")


def plot_all(df: pd.DataFrame, out_dir: str = "outputs/charts") -> None:
    """Generate 6 analysis charts and save to out_dir."""

    print("\n📊 Generating charts...")

    # ── 1. Monthly Revenue Trend ──────────────────────────────
    monthly = (
        df.groupby(["year", "month"])["revenue"]
        .sum()
        .reset_index()
    )
    monthly["date"] = pd.to_datetime(
        monthly[["year", "month"]].assign(day=1)
    )
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(monthly["date"], monthly["revenue"],
            marker="o", linewidth=2.2, color=COLORS[0])
    ax.fill_between(monthly["date"], monthly["revenue"],
                    alpha=0.12, color=COLORS[0])
    ax.set_title("Monthly Revenue Trend", fontsize=16, fontweight="bold", pad=14)
    ax.set_xlabel("Month"); ax.set_ylabel("Revenue (₹)")
    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f"₹{x/1e3:.0f}K")
    )
    _save(fig, f"{out_dir}/01_monthly_trend.png")

    # ── 2. Revenue by Region ──────────────────────────────────
    reg = df.groupby("region")["revenue"].sum().sort_values()
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(reg.index, reg.values, color=COLORS[:len(reg)])
    ax.bar_label(bars, fmt="₹%.0f", padding=6, fontsize=10)
    ax.set_title("Revenue by Region", fontsize=14, fontweight="bold")
    ax.set_xlabel("Revenue (₹)")
    _save(fig, f"{out_dir}/02_revenue_by_region.png")

    # ── 3. Category Revenue vs Profit Margin ─────────────────
    cat = df.groupby("category").agg(
        Revenue=("revenue", "sum"),
        Profit=("profit", "sum")
    ).reset_index()
    cat["Margin"] = (cat["Profit"] / cat["Revenue"] * 100).round(1)

    fig, ax = plt.subplots(figsize=(9, 6))
    scatter = ax.scatter(
        cat["Revenue"], cat["Margin"],
        s=[r / 500 for r in cat["Revenue"]],
        c=COLORS[:len(cat)], alpha=0.85, edgecolors="white", linewidth=1.5
    )
    for _, row in cat.iterrows():
        ax.annotate(
            f"{row['category']}\n({row['Margin']:.1f}%)",
            (row["Revenue"], row["Margin"]),
            textcoords="offset points", xytext=(10, 5),
            fontsize=10, color="#333"
        )
    ax.axhline(0, color="red", linestyle="--", alpha=0.5, linewidth=1)
    ax.set_title("Revenue vs Profit Margin by Category",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Revenue (₹)"); ax.set_ylabel("Profit Margin (%)")
    _save(fig, f"{out_dir}/03_category_margin.png")

    # ── 4. Discount Impact on Profit (Box Plot) ───────────────
    df2 = df.copy()
    df2["disc_bucket"] = pd.cut(
        df2["discount"],
        bins=[0, 0.1, 0.2, 0.3, 0.5, 1.01],
        labels=["0–10%", "10–20%", "20–30%", "30–50%", "50%+"],
        right=False
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    df2.boxplot(column="profit", by="disc_bucket",
                ax=ax, patch_artist=True,
                boxprops=dict(facecolor="#4f8ef7", alpha=0.5))
    ax.set_title("Profit Distribution by Discount Level",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Discount Range"); ax.set_ylabel("Profit (₹)")
    plt.suptitle("")
    _save(fig, f"{out_dir}/04_discount_impact.png")

    # ── 5. Top 10 Products (Horizontal Bar) ───────────────────
    top10 = df.groupby("product_name")["revenue"].sum().nlargest(10)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.barh(range(len(top10)), top10.values, color=COLORS[0], alpha=0.85)
    ax.set_yticks(range(len(top10)))
    ax.set_yticklabels([p[:40] for p in top10.index], fontsize=9)
    ax.set_title("Top 10 Products by Revenue",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Revenue (₹)")
    ax.invert_yaxis()
    _save(fig, f"{out_dir}/05_top_products.png")

    # ── 6. Quarterly Revenue Heatmap ─────────────────────────
    pivot = (
        df.groupby(["year", "quarter"])["revenue"]
        .sum()
        .unstack("quarter")
        .fillna(0)
    )
    fig, ax = plt.subplots(figsize=(9, 4))
    sns.heatmap(
        pivot / 1e3, annot=True, fmt=".0f",
        cmap="YlGnBu", linewidths=0.5, ax=ax,
        cbar_kws={"label": "Revenue (₹K)"}
    )
    ax.set_title("Quarterly Revenue Heatmap (₹K)",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Quarter"); ax.set_ylabel("Year")
    _save(fig, f"{out_dir}/06_quarterly_heatmap.png")

    print(f"\n✅ All 6 charts saved to '{out_dir}/'")


if __name__ == "__main__":
    df = pd.read_csv(
        "data/processed/sales_cleaned.csv",
        parse_dates=["order_date"]
    )
    plot_all(df)
