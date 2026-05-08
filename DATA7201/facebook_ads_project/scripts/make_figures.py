#!/usr/bin/env python3
"""Make a few draft PNG figures from Spark CSV output copied locally."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt


def find_csv(table_path: Path) -> Path | None:
    if table_path.is_file():
        return table_path
    matches = sorted(table_path.glob("part-*.csv"))
    return matches[0] if matches else None


def read_table(tables_dir: Path, table_name: str) -> list[dict[str, str]]:
    csv_path = find_csv(tables_dir / table_name)
    if csv_path is None:
        return []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def as_float(value: str | None) -> float:
    if value in (None, ""):
        return 0.0
    return float(value)


def plot_monthly(rows: list[dict[str, str]], figures_dir: Path) -> None:
    if not rows:
        return
    rows = sorted(rows, key=lambda row: row["delivery_month"])
    months = [row["delivery_month"] for row in rows]
    ad_counts = [as_float(row.get("ads_count")) for row in rows]
    spend = [as_float(row.get("spend_midpoint_total")) for row in rows]

    fig, ax1 = plt.subplots(figsize=(11, 5))
    ax1.plot(months, ad_counts, color="#1f77b4", linewidth=2, label="Ads")
    ax1.set_ylabel("Deduplicated ads")
    ax1.tick_params(axis="x", rotation=60)
    ax1.grid(axis="y", alpha=0.25)

    ax2 = ax1.twinx()
    ax2.plot(months, spend, color="#d62728", linewidth=2, label="Estimated spend midpoint")
    ax2.set_ylabel("Estimated spend midpoint")

    fig.suptitle("Political Facebook ads over time")
    fig.tight_layout()
    fig.savefig(figures_dir / "monthly_volume_spend.png", dpi=180)
    plt.close(fig)


def plot_top_advertisers(rows: list[dict[str, str]], figures_dir: Path) -> None:
    if not rows:
        return
    top = rows[:15]
    labels = [row["advertiser"][:55] for row in reversed(top)]
    spend = [as_float(row.get("spend_midpoint_total")) for row in reversed(top)]

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh(labels, spend, color="#4c78a8")
    ax.set_xlabel("Estimated spend midpoint")
    ax.set_title("Top advertisers by estimated spend")
    fig.tight_layout()
    fig.savefig(figures_dir / "top_advertisers_by_spend.png", dpi=180)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tables-dir", default="outputs/tables")
    parser.add_argument("--figures-dir", default="figures")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = Path(args.tables_dir)
    figures_dir = Path(args.figures_dir)
    figures_dir.mkdir(parents=True, exist_ok=True)

    plot_monthly(read_table(tables_dir, "monthly_volume_spend"), figures_dir)
    plot_top_advertisers(read_table(tables_dir, "top_advertisers"), figures_dir)


if __name__ == "__main__":
    main()
