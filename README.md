# Sales CRM Source API

A deliberately designed REST API that simulates a Sales CRM source system for an end-to-end Cloud Data Engineering pipeline.

The API is built with **FastAPI** and deployed to **Azure App Service**. It acts as the operational/source system for a larger data platform that will use Azure Data Factory, ADLS Gen2, Databricks, Azure SQL, and Power BI.

The project is designed not only to demonstrate API development, but also to demonstrate practical Data Engineering concepts such as:

- REST API ingestion
- Incremental data extraction
- Pagination
- Data validation
- Data quality issues
- Duplicate records
- Late/updated records
- Pipeline idempotency
- Bronze / Silver / Gold architecture
- ETL / ELT design
- Error handling
- Data grain
- SQL transformations
- Pipeline orchestration

---

## 1. Project Purpose

The goal of this project is to simulate a realistic source system and build an end-to-end data pipeline around it.

Instead of using a public API, this project uses a custom Sales CRM API so that the source data and its behavior can be intentionally controlled.

This allows the pipeline to be tested against realistic Data Engineering problems rather than only clean sample data.

The planned architecture is:

```text
                    SOURCE SYSTEM
                         │
                         ▼
                ┌─────────────────┐
                │   Sales CRM API │
                │    FastAPI      │
                └────────┬────────┘
                         │
                         │ HTTPS / REST
                         ▼
                ┌─────────────────┐
                │ Azure Data      │
                │ Factory (ADF)   │
                └────────┬────────┘
                         │
                         │ Raw JSON
                         ▼
                ┌─────────────────┐
                │ ADLS Gen2       │
                │ Bronze / Raw    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   Databricks    │
                │                 │
                │ Bronze          │
                │ Silver          │
                │ Gold            │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   Azure SQL     │
                │                 │
                │ Facts / Dims    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │    Power BI     │
                └─────────────────┘
