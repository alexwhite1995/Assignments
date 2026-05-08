# DATA7201 Facebook Ad Library Project Starter

This starter is for the code/analysis side of the DATA7201 report. It does not invent findings. Run the scripts on the DATA7201 cluster, inspect the generated tables, then write the report from the actual outputs.

## Project Shape

- `scripts/spark_inspect.py`: checks the raw JSON schema and field inventory on HDFS.
- `scripts/spark_preprocess.py`: reads raw JSON, standardises changing API fields, deduplicates repeated snapshots, and writes a clean Parquet table.
- `scripts/spark_analyze.py`: creates report-ready aggregate CSV tables.
- `scripts/make_figures.py`: optional local PNG charts after copying Spark CSV outputs locally.
- `config/keywords.json`: editable keyword groups for topic slices.
- `report/outline.md`: report scaffold with placeholders only.

## Run On The DATA7201 Cluster

Open the cloud environment in VS Code, then use the integrated terminal from this folder.

First confirm that HDFS can see the dataset:

```bash
hdfs dfs -ls /data/ProjectDatasetFacebookAU | head
```

Inspect the schema:

```bash
spark-submit scripts/spark_inspect.py \
  --input /data/ProjectDatasetFacebookAU \
  --output hdfs:///user/$USER/data7201_facebook_outputs/inspection
```

Preprocess and deduplicate:

```bash
spark-submit scripts/spark_preprocess.py \
  --input /data/ProjectDatasetFacebookAU \
  --output hdfs:///user/$USER/data7201_facebook_outputs \
  --keywords config/keywords.json
```

Create aggregate tables:

```bash
spark-submit scripts/spark_analyze.py \
  --input hdfs:///user/$USER/data7201_facebook_outputs/clean_ads \
  --output hdfs:///user/$USER/data7201_facebook_outputs/tables
```

List the outputs:

```bash
hdfs dfs -ls hdfs:///user/$USER/data7201_facebook_outputs/tables
```

## Bring Tables Back For Report Writing

Spark writes each CSV as a folder containing a `part-*.csv` file. To copy everything locally:

```bash
hdfs dfs -get hdfs:///user/$USER/data7201_facebook_outputs/tables outputs/tables
```

Optional draft figures:

```bash
python scripts/make_figures.py --tables-dir outputs/tables --figures-dir figures
```

## Important Reporting Notes

- Treat spend and impressions as Facebook-provided ranges. The scripts keep lower and upper bounds and use midpoint estimates only for summaries/ranking.
- Deduplication is central to the assignment: report that repeated 12-hour snapshots were grouped by `ad_archive_id` where present, with a hash fallback only for records missing that ID.
- Do not claim causal effects from these descriptive tables. Phrase findings as observed patterns in the ad library data.
- If a demographic or region table is empty, the field was missing or not consistently usable in the raw data; mention this as a limitation rather than forcing an analysis.

## Local Checks

The local machine does not need Spark for the small helper tests:

```bash
python -m unittest discover -s tests
```
