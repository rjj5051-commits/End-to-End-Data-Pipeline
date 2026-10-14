# End-to-End-Data-Pipeline
End-to-end data pipeline: API → S3 → Snowflake → dbt, orchestrated with Airflow

An end-to-end data engineering project, built in stages.

## Planned architecture
Public API → Python ingestion → Amazon S3 (Parquet) → Snowflake (bronze) → dbt (silver, gold) → dashboard
Orchestrated with Airflow.

## Stack
Python · SQL · Snowflake · dbt · AWS S3 · Airflow · Docker