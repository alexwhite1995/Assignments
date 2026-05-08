#!/usr/bin/env python3
"""Create report-ready aggregate tables from the cleaned ad table."""

from __future__ import annotations

import argparse
import os
from functools import reduce

from pyspark.sql import DataFrame, SparkSession, functions as F
from pyspark.sql.types import ArrayType, MapType, StructType


EVENT_WINDOWS = [
    ("federal_election_2022_leadup", "2022-03-01", "2022-05-21"),
    ("federal_election_2022_month", "2022-05-01", "2022-05-31"),
    ("voice_referendum_2023_campaign", "2023-08-01", "2023-10-14"),
    ("voice_referendum_2023_month", "2023-10-01", "2023-10-31"),
]


def field_exists(schema: StructType, dotted_path: str) -> bool:
    data_type = schema
    for part in dotted_path.split("."):
        if not isinstance(data_type, StructType):
            return False
        match = next((field for field in data_type.fields if field.name == part), None)
        if match is None:
            return False
        data_type = match.dataType
    return True


def top_level_field_type(schema: StructType, name: str):
    for field in schema.fields:
        if field.name == name:
            return field.dataType
    return None


def col_path(dotted_path: str):
    return F.col(".".join(f"`{part}`" for part in dotted_path.split(".")))


def first_existing(df: DataFrame, candidates: list[str], default=None):
    for candidate in candidates:
        if field_exists(df.schema, candidate):
            return col_path(candidate)
    return F.lit(default)


def numeric_from(column):
    cleaned = F.regexp_replace(column.cast("string"), r"[^0-9.]", "")
    return F.when(F.length(cleaned) > 0, cleaned.cast("double"))


def percentage_fraction(column):
    numeric = numeric_from(column)
    return F.when(numeric > 1.0, numeric / F.lit(100.0)).otherwise(numeric)


def write_csv(df: DataFrame, path: str) -> None:
    df.coalesce(1).write.mode("overwrite").option("header", True).csv(path)


def aggregate_base(df: DataFrame):
    return [
        F.countDistinct("canonical_ad_id").alias("ads_count"),
        F.sum("snapshot_count").alias("snapshot_rows_count"),
        F.sum("spend_lower").alias("spend_lower_total"),
        F.sum("spend_upper").alias("spend_upper_total"),
        F.sum("spend_midpoint").alias("spend_midpoint_total"),
        F.sum("impressions_lower").alias("impressions_lower_total"),
        F.sum("impressions_upper").alias("impressions_upper_total"),
        F.sum("impressions_midpoint").alias("impressions_midpoint_total"),
    ]


def union_frames(frames: list[DataFrame]) -> DataFrame | None:
    if not frames:
        return None
    return reduce(lambda left, right: left.unionByName(right), frames)


def create_core_tables(df: DataFrame, output: str) -> None:
    base = df.withColumn(
        "activity_date", F.coalesce(F.col("delivery_start_date"), F.to_date("ad_creation_ts"))
    )

    monthly = (
        base.where(F.col("delivery_month").isNotNull())
        .groupBy("delivery_month")
        .agg(*aggregate_base(base))
        .orderBy("delivery_month")
    )
    write_csv(monthly, output + "/monthly_volume_spend")

    event_frames = []
    for event_name, start_date, end_date in EVENT_WINDOWS:
        event_frames.append(
            base.where(
                (F.col("activity_date") >= F.to_date(F.lit(start_date)))
                & (F.col("activity_date") <= F.to_date(F.lit(end_date)))
            )
            .agg(*aggregate_base(base))
            .withColumn("event_window", F.lit(event_name))
            .withColumn("start_date", F.lit(start_date))
            .withColumn("end_date", F.lit(end_date))
            .select("event_window", "start_date", "end_date", *[column for column in monthly.columns if column != "delivery_month"])
        )
    events = union_frames(event_frames)
    if events is not None:
        write_csv(events, output + "/event_windows")

    top_advertisers = (
        base.withColumn("advertiser", F.coalesce("funding_entity", "byline", "page_name"))
        .where(F.col("advertiser").isNotNull())
        .groupBy("advertiser")
        .agg(*aggregate_base(base))
        .orderBy(F.desc("spend_midpoint_total"), F.desc("ads_count"))
        .limit(50)
    )
    write_csv(top_advertisers, output + "/top_advertisers")

    top_pages = (
        base.where(F.col("page_name").isNotNull())
        .groupBy("page_id", "page_name")
        .agg(*aggregate_base(base))
        .orderBy(F.desc("ads_count"), F.desc("spend_midpoint_total"))
        .limit(50)
    )
    write_csv(top_pages, output + "/top_pages")

    domains = (
        base.select(
            "canonical_ad_id",
            "spend_midpoint",
            "impressions_midpoint",
            F.explode_outer("domains").alias("domain"),
        )
        .where(F.col("domain").isNotNull() & (F.length("domain") > 0))
        .groupBy("domain")
        .agg(
            F.countDistinct("canonical_ad_id").alias("ads_count"),
            F.sum("spend_midpoint").alias("spend_midpoint_total"),
            F.sum("impressions_midpoint").alias("impressions_midpoint_total"),
        )
        .orderBy(F.desc("ads_count"), F.desc("spend_midpoint_total"))
        .limit(100)
    )
    write_csv(domains, output + "/top_domains")


def create_topic_tables(df: DataFrame, output: str) -> None:
    topic_columns = [column for column in df.columns if column.startswith("topic_")]
    topic_frames = [
        df.where(F.col(column) == F.lit(True)).withColumn("topic", F.lit(column.replace("topic_", "")))
        for column in topic_columns
    ]
    topics = union_frames(topic_frames)
    if topics is None:
        return

    topic_monthly = (
        topics.where(F.col("delivery_month").isNotNull())
        .groupBy("topic", "delivery_month")
        .agg(*aggregate_base(topics))
        .orderBy("topic", "delivery_month")
    )
    write_csv(topic_monthly, output + "/topic_monthly_volume_spend")

    topic_advertisers = (
        topics.withColumn("advertiser", F.coalesce("funding_entity", "byline", "page_name"))
        .where(F.col("advertiser").isNotNull())
        .groupBy("topic", "advertiser")
        .agg(*aggregate_base(topics))
        .orderBy("topic", F.desc("spend_midpoint_total"), F.desc("ads_count"))
    )
    write_csv(topic_advertisers, output + "/topic_top_advertisers")

    topic_duration = (
        topics.where(F.col("campaign_duration_days").isNotNull())
        .groupBy("topic")
        .agg(
            F.countDistinct("canonical_ad_id").alias("ads_count"),
            F.avg("campaign_duration_days").alias("duration_days_mean"),
            F.expr("percentile_approx(campaign_duration_days, 0.5)").alias("duration_days_median"),
            F.max("campaign_duration_days").alias("duration_days_max"),
        )
        .orderBy("topic")
    )
    write_csv(topic_duration, output + "/topic_campaign_duration")


def create_demographic_table(df: DataFrame, output: str) -> None:
    if "demographic_distribution" not in df.columns:
        return
    if not isinstance(top_level_field_type(df.schema, "demographic_distribution"), (ArrayType, MapType)):
        return

    exploded = df.select(
        "canonical_ad_id",
        "spend_midpoint",
        "impressions_midpoint",
        F.explode_outer("demographic_distribution").alias("demo"),
    ).where(F.col("demo").isNotNull())
    age = first_existing(exploded, ["demo.age", "demo.age_range"])
    gender = first_existing(exploded, ["demo.gender"])
    pct = percentage_fraction(first_existing(exploded, ["demo.percentage", "demo.percent"]))

    demo = (
        exploded.select(
            age.cast("string").alias("age"),
            gender.cast("string").alias("gender"),
            pct.alias("percentage"),
            "spend_midpoint",
            "impressions_midpoint",
        )
        .where(F.col("age").isNotNull() | F.col("gender").isNotNull())
        .groupBy("age", "gender")
        .agg(
            F.count(F.lit(1)).alias("ads_with_distribution_rows"),
            F.avg("percentage").alias("mean_percentage"),
            F.sum(F.col("spend_midpoint") * F.col("percentage")).alias("estimated_spend_midpoint"),
            F.sum(F.col("impressions_midpoint") * F.col("percentage")).alias(
                "estimated_impressions_midpoint"
            ),
        )
        .orderBy("age", "gender")
    )
    write_csv(demo, output + "/demographic_distribution")


def create_region_table(df: DataFrame, output: str) -> None:
    if "delivery_by_region" not in df.columns:
        return
    if not isinstance(top_level_field_type(df.schema, "delivery_by_region"), (ArrayType, MapType)):
        return

    exploded = df.select(
        "canonical_ad_id",
        "spend_midpoint",
        "impressions_midpoint",
        F.explode_outer("delivery_by_region").alias("region_info"),
    ).where(F.col("region_info").isNotNull())
    region = first_existing(exploded, ["region_info.region", "region_info.name"])
    pct = percentage_fraction(first_existing(exploded, ["region_info.percentage", "region_info.percent"]))

    regions = (
        exploded.select(
            region.cast("string").alias("region"),
            pct.alias("percentage"),
            "spend_midpoint",
            "impressions_midpoint",
        )
        .where(F.col("region").isNotNull())
        .groupBy("region")
        .agg(
            F.count(F.lit(1)).alias("ads_with_region_rows"),
            F.avg("percentage").alias("mean_percentage"),
            F.sum(F.col("spend_midpoint") * F.col("percentage")).alias("estimated_spend_midpoint"),
            F.sum(F.col("impressions_midpoint") * F.col("percentage")).alias(
                "estimated_impressions_midpoint"
            ),
        )
        .orderBy(F.desc("estimated_spend_midpoint"))
    )
    write_csv(regions, output + "/regional_distribution")


def parse_args() -> argparse.Namespace:
    user = os.environ.get("USER") or os.environ.get("USERNAME") or "unknown"
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default=f"hdfs:///user/{user}/data7201_facebook_outputs/clean_ads",
        help="Clean Parquet folder created by spark_preprocess.py.",
    )
    parser.add_argument(
        "--output",
        default=f"hdfs:///user/{user}/data7201_facebook_outputs/tables",
        help="Folder for report-ready aggregate CSV tables.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    spark = SparkSession.builder.appName("data7201-facebook-analyze").getOrCreate()
    output = args.output.rstrip("/")
    clean = spark.read.parquet(args.input)

    create_core_tables(clean, output)
    create_topic_tables(clean, output)
    create_demographic_table(clean, output)
    create_region_table(clean, output)

    spark.stop()


if __name__ == "__main__":
    main()
