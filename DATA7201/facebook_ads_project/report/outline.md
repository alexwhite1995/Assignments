# DATA7201 Project Report Outline

Working title: Australian political Facebook advertising, 2020-2024

Word count: TODO

## Structured Abstract

Background: TODO

Objective: TODO

Methods: PySpark on the DATA7201 cluster was used to load Facebook Ad Library JSON snapshots from HDFS, normalise selected fields, and deduplicate repeated active-ad snapshots. TODO: add final analysis focus.

Results: TODO after running the aggregate tables.

Conclusion: TODO after interpreting the aggregate tables.

## Table of Contents

TODO in final document.

## 1. Introduction

TODO: motivate why distributed data processing is appropriate when API snapshots create many semi-structured JSON records with repeated campaign observations and changing nested fields.

Possible literature angles:
- Big data volume/variety and distributed processing.
- Semi-structured JSON analytics with Spark SQL/DataFrames.
- Political advertising transparency and platform ad libraries.

## 2. Dataset Analytics

Dataset:
- Facebook Ad Library API snapshots for Australian political ads.
- Period: March 2020 to February 2024.
- Source on DATA7201 HDFS: `/data/ProjectDatasetFacebookAU`.

Pre-processing to report:
- Read JSON snapshots from HDFS using Spark.
- Exploded the API `data` array when present.
- Standardised core fields: ad ID, page, funding entity, delivery dates, spend bounds, impression bounds, creative text, URLs/domains, demographics, and region distributions where available.
- Deduplicated repeated snapshots by `ad_archive_id` where available; otherwise used a stable hash from page, funding entity, delivery start, and creative text.
- Preserved `snapshot_count` so duplicate intensity can still be discussed.
- Kept Facebook lower/upper spend and impression bounds; used midpoint estimates only for ranking and aggregate summaries.

Analysis tables to use:
- `preprocess_summary`
- `monthly_volume_spend`
- `event_windows`
- `top_advertisers`
- `top_pages`
- `top_domains`
- `topic_monthly_volume_spend`
- `topic_top_advertisers`
- `topic_campaign_duration`
- `demographic_distribution`, if populated
- `regional_distribution`, if populated

## 3. Discussion And Conclusions

TODO:
- State the main observed pattern from the tables.
- Discuss whether the event windows show concentration around the 2022 federal election or 2023 Voice referendum.
- Discuss limitations: API field changes, spend/impression ranges rather than exact values, topic keyword false positives/negatives, and active-ad snapshot duplication.
- Explain why Spark/HDFS was useful for full-dataset preprocessing even if final visualisation was done locally.

## Appendix

Include commands used:

```bash
spark-submit scripts/spark_inspect.py --input /data/ProjectDatasetFacebookAU --output hdfs:///user/$USER/data7201_facebook_outputs/inspection
spark-submit scripts/spark_preprocess.py --input /data/ProjectDatasetFacebookAU --output hdfs:///user/$USER/data7201_facebook_outputs --keywords config/keywords.json
spark-submit scripts/spark_analyze.py --input hdfs:///user/$USER/data7201_facebook_outputs/clean_ads --output hdfs:///user/$USER/data7201_facebook_outputs/tables
```

Include final code snippets or reference the submitted script files, depending on submission instructions.
