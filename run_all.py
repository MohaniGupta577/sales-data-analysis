"""
Sales Data Analysis — run_all.py
Author  : Mohani Gupta | mohanigupta279@gmail.com
Purpose : Single entry-point to run the full analysis pipeline
Usage   : python run_all.py
"""

import os
import sys
import time

def section(title: str) -> None:
    print(f"\n{'='*58}")
    print(f"  {title}")
    print(f"{'='*58}")


def main():
    section("SALES DATA ANALYSIS PIPELINE  — Mohani Gupta")

    # ── Step 1: Clean ─────────────────────────────────────────
    section("STEP 1 / 3  —  Data Cleaning")
    t0 = time.time()
    from src.clean import load_and_clean
    df = load_and_clean(
        raw_path  = "data/raw/sales_data.csv",
        save_path = "data/processed/sales_cleaned.csv"
    )
    print(f"  ✓ Done in {time.time()-t0:.1f}s  |  Shape: {df.shape}")

    # ── Step 2: Analyse ───────────────────────────────────────
    section("STEP 2 / 3  —  Statistical Analysis")
    t0 = time.time()
    from src.analyse import run_analysis
    run_analysis(df)
    print(f"\n  ✓ Done in {time.time()-t0:.1f}s")

    # ── Step 3: Visualise ─────────────────────────────────────
    section("STEP 3 / 3  —  Chart Generation")
    t0 = time.time()
    os.makedirs("outputs/charts", exist_ok=True)
    from src.visualise import plot_all
    plot_all(df, out_dir="outputs/charts")
    print(f"  ✓ Done in {time.time()-t0:.1f}s")

    section("ALL STEPS COMPLETE")
    print("  📊 Charts   → outputs/charts/")
    print("  📄 Clean CSV → data/processed/sales_cleaned.csv")
    print("\n  Open the charts folder to explore the visuals!")


if __name__ == "__main__":
    main()
