# ================================================================
# Sales Data Analysis — clean.py
# Author  : Mohani Gupta | mohanigupta279@gmail.com
# Purpose : Ingest raw CSV and apply full cleaning pipeline
# ================================================================

import pandas as pd
import numpy as np
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(message)s")


def load_and_clean(raw_path: str, save_path: str | None = None) -> pd.DataFrame:
    """
    Load raw sales CSV, apply cleaning pipeline, optionally save.

    Steps:
        1. Load CSV with dtype hints
        2. Drop duplicates
        3. Parse & enrich dates
        4. Handle nulls
        5. Standardise string columns
        6. Validate numeric ranges
        7. Engineer basic features
    """
    logging.info(f"Loading: {raw_path}")
    df = pd.read_csv(raw_path, dtype={"order_id": str, "customer_id": str})
    logging.info(f"Raw shape: {df.shape}")

    # ── 1. Drop duplicates ────────────────────────────────────
    before = len(df)
    df.drop_duplicates(subset="order_id", keep="first", inplace=True)
    logging.info(f"Removed {before - len(df)} duplicate rows")

    # ── 2. Parse dates ────────────────────────────────────────
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["ship_date"]  = pd.to_datetime(df.get("ship_date"), errors="coerce")
    df.dropna(subset=["order_date"], inplace=True)

    # ── 3. Date feature engineering ───────────────────────────
    df["year"]       = df["order_date"].dt.year
    df["month"]      = df["order_date"].dt.month
    df["quarter"]    = df["order_date"].dt.quarter
    df["month_name"] = df["order_date"].dt.strftime("%b")
    df["weekday"]    = df["order_date"].dt.day_name()

    # ── 4. Handle nulls ───────────────────────────────────────
    df["discount"].fillna(0, inplace=True)
    df["profit"].fillna(0, inplace=True)
    df.dropna(subset=["sales", "category", "region"], inplace=True)

    # ── 5. Standardise strings ────────────────────────────────
    for col in ["region", "category", "sub_category", "ship_mode"]:
        if col in df.columns:
            df[col] = df[col].str.strip().str.title()

    # ── 6. Validate numeric ranges ────────────────────────────
    df = df[df["sales"] > 0]
    df = df[df["quantity"] > 0]
    df["discount"] = df["discount"].clip(0, 1)

    # ── 7. Derived columns ────────────────────────────────────
    df["revenue"]       = df["sales"] * df["quantity"]
    df["profit_margin"] = np.where(
        df["revenue"] > 0,
        (df["profit"] / df["revenue"] * 100).round(2),
        0
    )
    df["is_profitable"] = df["profit"] > 0

    logging.info(f"Clean shape: {df.shape}")

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df.to_csv(save_path, index=False)
        logging.info(f"Saved cleaned data → {save_path}")

    return df


if __name__ == "__main__":
    df = load_and_clean(
        raw_path="data/raw/sales_data.csv",
        save_path="data/processed/sales_cleaned.csv"
    )
    print(df.head())
