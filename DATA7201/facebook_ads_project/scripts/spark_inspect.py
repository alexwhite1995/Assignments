#!/usr/bin/env python3
"""Inspect the raw Facebook Ad Library JSON on HDFS.

Run this first on the DATA7201 cluster to confirm the available fields before
you write the report. It does not modify the raw data.
"""

from __future__ import annotations

import argparse

from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import ArrayType, StructType


def field_type(schema: StructType, name: str):
    for field in schema.fields:
        if field.name == name:
            return field.dataType
    return None


def load_raw_ads(spark: SparkSession, input_path: str):
    raw = (
        spark.read.option("multiLine", "true")
        .option("recursiveFileLookup", "true")
        .option("mode", "PERMISSIVE")
        .option("columnNameOfCorruptRecord", "_corrupt_record")
        .json(input_path)
        .withColumn("_source_file", F.input_file_name())
    )

    data_type = field_type(raw.schema, "data")
    if isinstance(data_type, ArrayType):
        return raw.select("_source_file", F.explode_outer("data").alias("_ad")).select(
            "_source_file", "_ad.*"
        )
    if isinstance(data_type, StructType):
        return raw.select("_source_file", "data.*")
    return raw


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="/data/ProjectDatasetFacebookAU")
    parser.add_argument(
        "--output",
        default=None,
        help="Optional HDFS/local folder for schema and column inventory CSVs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    spark = SparkSession.builder.appName("data7201-facebook-inspect").getOrCreate()

    ads = load_raw_ads(spark, args.input)
    print("Raw ad-level schema")
    ads.printSchema()
    print("Ad-level row count:", ads.count())
    print("Columns:", ", ".join(ads.columns))

    if args.output:
        output = args.output.rstrip("/")
        columns = spark.createDataFrame(ads.dtypes, ["column", "spark_type"])
        columns.coalesce(1).write.mode("overwrite").option("header", True).csv(
            output + "/column_inventory"
        )
        spark.createDataFrame([(ads.schema.json(),)], ["schema_json"]).coalesce(1).write.mode(
            "overwrite"
        ).option("header", True).csv(output + "/schema_json")

    spark.stop()


if __name__ == "__main__":
    main()
