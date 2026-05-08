#!/usr/bin/env python3
"""Pre-process Facebook Ad Library JSON into one deduplicated ad table.

The API snapshots contain repeated ads because the same active campaign can be
returned every 12 hours. This script keeps one row per canonical ad and records
how many snapshots contributed to it.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from urllib.parse import urlsplit

from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import ArrayType, StringType, StructType


URL_RE = re.compile(
    r"(?i)\b((?:https?://|www\.)[^\s<>'\"()]+|[a-z0-9.-]+\.[a-z]{2,}(?:/[^\s<>'\"()]*)?)"
)


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


def first_existing(df, candidates: list[str], default=None):
    for candidate in candidates:
        if field_exists(df.schema, candidate):
            return col_path(candidate)
    return F.lit(default)


def first_existing_name(df, candidates: list[str]) -> str | None:
    for candidate in candidates:
        if field_exists(df.schema, candidate):
            return candidate
    return None


def numeric_from(column):
    cleaned = F.regexp_replace(column.cast("string"), r"[^0-9.]", "")
    return F.when(F.length(cleaned) > 0, cleaned.cast("double"))


def timestamp_from(column):
    as_string = column.cast("string")
    return F.coalesce(
        column.cast("timestamp"),
        F.to_timestamp(as_string),
        F.to_timestamp(as_string, "yyyy-MM-dd'T'HH:mm:ssX"),
        F.to_timestamp(as_string, "yyyy-MM-dd'T'HH:mm:ssXX"),
        F.to_timestamp(as_string, "yyyy-MM-dd'T'HH:mm:ssXXX"),
        F.to_timestamp(as_string, "yyyy-MM-dd'T'HH:mm:ss.SSSX"),
        F.to_timestamp(as_string, "yyyy-MM-dd"),
    )


def normalise_domain(value: str | None) -> str | None:
    if not value:
        return None
    candidate = value.strip().strip(".,;:!?)(")
    if not candidate:
        return None
    if "://" not in candidate:
        candidate = "https://" + candidate
    host = urlsplit(candidate).netloc.lower()
    if "@" in host:
        host = host.rsplit("@", 1)[-1]
    if ":" in host:
        host = host.split(":", 1)[0]
    if host.startswith("www."):
        host = host[4:]
    return host or None


def extract_domains(text: str | None) -> list[str]:
    if not text:
        return []
    domains = []
    seen = set()
    for match in URL_RE.finditer(text):
        domain = normalise_domain(match.group(1))
        if domain and domain not in seen:
            seen.add(domain)
            domains.append(domain)
    return domains


def keyword_pattern(keywords: list[str]) -> str:
    escaped = []
    for keyword in keywords:
        token = str(keyword).strip().lower()
        if token:
            escaped.append(re.escape(token).replace(r"\ ", r"\s+"))
    if not escaped:
        return r"a^"
    return r"(?:^|[^a-z0-9])(" + "|".join(escaped) + r")(?:[^a-z0-9]|$)"


def safe_topic_name(name: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    return cleaned or "topic"


def load_keywords(path: str | None) -> dict[str, list[str]]:
    if not path:
        return {}
    with open(path, "r", encoding="utf-8") as handle:
        loaded = json.load(handle)
    return {str(key): [str(item) for item in value] for key, value in loaded.items()}


def load_raw_ads(spark: SparkSession, input_path: str):
    raw = (
        spark.read.option("multiLine", "true")
        .option("recursiveFileLookup", "true")
        .option("mode", "PERMISSIVE")
        .option("columnNameOfCorruptRecord", "_corrupt_record")
        .json(input_path)
        .withColumn("_source_file", F.input_file_name())
    )

    data_type = top_level_field_type(raw.schema, "data")
    if isinstance(data_type, ArrayType):
        return raw.select("_source_file", F.explode_outer("data").alias("_ad")).select(
            "_source_file", "_ad.*"
        )
    if isinstance(data_type, StructType):
        return raw.select("_source_file", "data.*")
    return raw


def standardise_snapshots(ads, keywords: dict[str, list[str]]):
    text_candidates = [
        "ad_creative_bodies",
        "ad_creative_body",
        "ad_creative_link_titles",
        "ad_creative_link_title",
        "ad_creative_link_captions",
        "ad_creative_link_caption",
        "ad_creative_link_descriptions",
        "ad_creative_link_description",
        "body",
        "title",
        "page_name",
        "funding_entity",
        "bylines",
    ]
    url_candidates = [
        "ad_creative_link_urls",
        "ad_creative_link_url",
        "link_url",
        "ad_snapshot_url",
    ]

    text_columns = [
        col_path(candidate).cast("string")
        for candidate in text_candidates
        if field_exists(ads.schema, candidate)
    ]
    url_columns = [
        col_path(candidate).cast("string")
        for candidate in url_candidates
        if field_exists(ads.schema, candidate)
    ]

    full_text = F.concat_ws(" ", *(text_columns + url_columns)) if text_columns or url_columns else F.lit("")
    delivery_start_raw = first_existing(
        ads, ["ad_delivery_start_time", "delivery_start_time", "start_time"]
    )
    delivery_stop_raw = first_existing(
        ads, ["ad_delivery_stop_time", "delivery_stop_time", "stop_time"]
    )
    creation_raw = first_existing(ads, ["ad_creation_time", "creation_time", "created_time"])

    select_exprs = [
        F.col("_source_file"),
        first_existing(ads, ["ad_archive_id", "ad_id", "id"]).cast("string").alias("ad_id"),
        first_existing(ads, ["page_id", "page.id"]).cast("string").alias("page_id"),
        first_existing(ads, ["page_name", "page.name"]).cast("string").alias("page_name"),
        first_existing(ads, ["funding_entity", "paid_for_by"]).cast("string").alias("funding_entity"),
        first_existing(ads, ["bylines", "byline"]).cast("string").alias("byline"),
        first_existing(ads, ["currency"]).cast("string").alias("currency"),
        creation_raw.cast("string").alias("ad_creation_time"),
        delivery_start_raw.cast("string").alias("delivery_start_time"),
        delivery_stop_raw.cast("string").alias("delivery_stop_time"),
        timestamp_from(creation_raw).alias("ad_creation_ts"),
        timestamp_from(delivery_start_raw).alias("delivery_start_ts"),
        timestamp_from(delivery_stop_raw).alias("delivery_stop_ts"),
        numeric_from(
            first_existing(
                ads,
                ["spend.lower_bound", "spend_lower_bound", "spend.lower", "spend_min", "spend_minimum"],
            )
        ).alias("spend_lower"),
        numeric_from(
            first_existing(
                ads,
                ["spend.upper_bound", "spend_upper_bound", "spend.upper", "spend_max", "spend_maximum"],
            )
        ).alias("spend_upper"),
        numeric_from(
            first_existing(
                ads,
                [
                    "impressions.lower_bound",
                    "impressions_lower_bound",
                    "impressions.lower",
                    "impressions_min",
                    "impressions_minimum",
                ],
            )
        ).alias("impressions_lower"),
        numeric_from(
            first_existing(
                ads,
                [
                    "impressions.upper_bound",
                    "impressions_upper_bound",
                    "impressions.upper",
                    "impressions_max",
                    "impressions_maximum",
                ],
            )
        ).alias("impressions_upper"),
        first_existing(ads, ["ad_snapshot_url"]).cast("string").alias("ad_snapshot_url"),
        first_existing(ads, ["publisher_platforms"]).cast("string").alias("publisher_platforms"),
        first_existing(ads, ["languages"]).cast("string").alias("languages"),
        full_text.alias("full_text"),
    ]
    demographic_name = first_existing_name(
        ads, ["demographic_distribution", "age_country_gender_reach_breakdown"]
    )
    if demographic_name:
        select_exprs.append(col_path(demographic_name).alias("demographic_distribution"))
    region_name = first_existing_name(ads, ["delivery_by_region", "region_distribution"])
    if region_name:
        select_exprs.append(col_path(region_name).alias("delivery_by_region"))

    selected = ads.select(*select_exprs)

    extract_domains_udf = F.udf(extract_domains, ArrayType(StringType()))
    selected = selected.withColumn("domains", extract_domains_udf(F.col("full_text"))).withColumn(
        "_full_text_lower", F.lower(F.col("full_text"))
    )

    for topic, topic_keywords in keywords.items():
        selected = selected.withColumn(
            "topic_" + safe_topic_name(topic),
            F.col("_full_text_lower").rlike(keyword_pattern(topic_keywords)),
        )

    return selected


def first_non_null(column_name: str):
    return F.first(F.col(column_name), ignorenulls=True).alias(column_name)


def deduplicate(standardised):
    identity_text = F.concat_ws(
        "||",
        F.coalesce(F.col("page_id"), F.lit("")),
        F.coalesce(F.col("page_name"), F.lit("")),
        F.coalesce(F.col("funding_entity"), F.lit("")),
        F.coalesce(F.col("delivery_start_time"), F.lit("")),
        F.coalesce(F.col("full_text"), F.lit("")),
    )
    keyed = standardised.withColumn(
        "canonical_ad_id",
        F.when(F.length(F.coalesce(F.col("ad_id"), F.lit(""))) > 0, F.col("ad_id")).otherwise(
            F.concat(F.lit("hash_"), F.sha2(identity_text, 256))
        ),
    )

    topic_columns = [column for column in keyed.columns if column.startswith("topic_")]
    aggregations = [
        first_non_null("ad_id"),
        first_non_null("page_id"),
        first_non_null("page_name"),
        first_non_null("funding_entity"),
        first_non_null("byline"),
        first_non_null("currency"),
        first_non_null("ad_creation_time"),
        first_non_null("delivery_start_time"),
        first_non_null("delivery_stop_time"),
        F.min("ad_creation_ts").alias("ad_creation_ts"),
        F.min("delivery_start_ts").alias("delivery_start_ts"),
        F.max("delivery_stop_ts").alias("delivery_stop_ts"),
        F.max("spend_lower").alias("spend_lower"),
        F.max("spend_upper").alias("spend_upper"),
        F.max("impressions_lower").alias("impressions_lower"),
        F.max("impressions_upper").alias("impressions_upper"),
        first_non_null("ad_snapshot_url"),
        first_non_null("publisher_platforms"),
        first_non_null("languages"),
        first_non_null("full_text"),
        F.array_distinct(F.flatten(F.collect_list("domains"))).alias("domains"),
        F.count(F.lit(1)).alias("snapshot_count"),
        F.countDistinct("_source_file").alias("source_file_count"),
        F.min("_source_file").alias("first_source_file"),
        F.max("_source_file").alias("last_source_file"),
    ]
    if "demographic_distribution" in keyed.columns:
        aggregations.append(first_non_null("demographic_distribution"))
    if "delivery_by_region" in keyed.columns:
        aggregations.append(first_non_null("delivery_by_region"))
    aggregations.extend(
        F.max(F.col(column).cast("int")).cast("boolean").alias(column) for column in topic_columns
    )

    deduped = keyed.groupBy("canonical_ad_id").agg(*aggregations)
    deduped = (
        deduped.withColumn("delivery_start_date", F.to_date("delivery_start_ts"))
        .withColumn("delivery_stop_date", F.to_date("delivery_stop_ts"))
        .withColumn(
            "delivery_month",
            F.date_format(F.coalesce(F.col("delivery_start_ts"), F.col("ad_creation_ts")), "yyyy-MM"),
        )
        .withColumn(
            "campaign_duration_days",
            F.when(
                F.col("delivery_start_date").isNotNull() & F.col("delivery_stop_date").isNotNull(),
                F.datediff(F.col("delivery_stop_date"), F.col("delivery_start_date")) + F.lit(1),
            ),
        )
        .withColumn(
            "spend_midpoint",
            F.when(
                F.col("spend_lower").isNotNull() & F.col("spend_upper").isNotNull(),
                (F.col("spend_lower") + F.col("spend_upper")) / F.lit(2.0),
            ).otherwise(F.coalesce(F.col("spend_lower"), F.col("spend_upper"))),
        )
        .withColumn(
            "impressions_midpoint",
            F.when(
                F.col("impressions_lower").isNotNull() & F.col("impressions_upper").isNotNull(),
                (F.col("impressions_lower") + F.col("impressions_upper")) / F.lit(2.0),
            ).otherwise(F.coalesce(F.col("impressions_lower"), F.col("impressions_upper"))),
        )
    )
    return deduped


def write_csv(df, path: str) -> None:
    df.coalesce(1).write.mode("overwrite").option("header", True).csv(path)


def parse_args() -> argparse.Namespace:
    user = os.environ.get("USER") or os.environ.get("USERNAME") or "unknown"
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="/data/ProjectDatasetFacebookAU")
    parser.add_argument(
        "--output",
        default=f"hdfs:///user/{user}/data7201_facebook_outputs",
        help="Output folder. Use an HDFS path on the cluster.",
    )
    parser.add_argument("--keywords", default="config/keywords.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    spark = SparkSession.builder.appName("data7201-facebook-preprocess").getOrCreate()
    output = args.output.rstrip("/")

    keywords = load_keywords(args.keywords)
    raw_ads = load_raw_ads(spark, args.input)
    standardised = standardise_snapshots(raw_ads, keywords)
    deduped = deduplicate(standardised)

    deduped.write.mode("overwrite").parquet(output + "/clean_ads")
    write_csv(deduped.limit(200), output + "/samples/clean_ads_sample")

    raw_count = standardised.count()
    clean_count = deduped.count()
    duplicate_rows_removed = raw_count - clean_count
    summary = spark.createDataFrame(
        [
            ("raw_snapshot_rows", str(raw_count)),
            ("deduplicated_ads", str(clean_count)),
            ("duplicate_snapshot_rows_removed", str(duplicate_rows_removed)),
            ("duplicate_handling", "grouped by ad_archive_id when present, otherwise stable hash"),
            ("spend_impression_handling", "kept lower/upper bounds and calculated midpoint estimates"),
        ],
        ["metric", "value"],
    )
    write_csv(summary, output + "/tables/preprocess_summary")

    spark.stop()


if __name__ == "__main__":
    main()
