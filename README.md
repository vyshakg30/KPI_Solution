# Analytics pipeline

## Overview

This project implements a Medallion Architecture data pipeline that processes raw data through multiple layers of
refinement, culminating in calculated metrics served via REST API.

## Architecture

### ETL Approach
We employ a "Best Effort Load" approach for loading raw data, ignoring invalid or redundant points in favor of
"Error Quarantining" over an "All or Nothing" method. During testing, invalid entries are easily identified.

Strict data integrity constraints are maintained for all KPI and Alert data stores.

### System Design

The pipeline follows a three-layer Medallion Architecture pattern:

- **Bronze Layer**: Raw data ingestion from external sources
- **Silver Layer**: Cleaned and validated data with proper constraints
- **Gold Layer**: Calculated KPIs and business metrics
- **API Layer**: Calculated metrics are served through a REST API

## Data Flow

Bronze Layer → Raw data is ingested as-is from external sources into the database

Silver Layer → Data from payments, loans, and quotes tables is cleaned and validated with proper data constraints

Gold Layer → KPIs and alerts are calculated from silver layer data and populated back into the database with strict schemas



#### Flow Chart

![Flow_chart](https://github.com/user-attachments/assets/b8f4a889-8b14-454a-bb80-c812b13503d0)

## Data Modeling

- Common Date format 'YYYY-MM-DD' is used.
- Although For Primary key fields like 'loan_id','quote_id','payment_id' integer appears to be natural choice, varchar, 
  is chosen here in order to keep it open for alpha numeric type as well.

### Broze Layer Schema
Same Table Structure as silver layer with all the fields having datatype varchar to support every kind of data

### Silver Layer Schema

#### Loans Table
| Field        | Data Type | Description                  |
|--------------|-----------|------------------------------|
| loan_id      | varchar   | Loan identifier              |
| quote_id     | varchar   | Related quote identifier     |
| funded_at    | date      | Parsed funding date          |
| principal    | integer   | Loan principal amount        |
| apr          | double    | Annual percentage rate       |
| term_months  | integer   | Loan term in months          |
| status       | varchar   | Loan status                  |

---

#### Quotes Table
| Field          | Data Type | Description                  |
|----------------|-----------|------------------------------|
| quote_id       | varchar   | Quote identifier             |
| created_at     | date      | Parsed creation date         |
| system_size_kw | integer   | System size in kilowatts     |
| down_payment   | integer   | Down payment amount          |
| system_price   | integer   | Total system price           |
| email          | varchar   | Customer email               |

---

#### Payments Table
| Field      | Data Type | Description                  |
|------------|-----------|------------------------------|
| payment_id | varchar   | Payment identifier           |
| loan_id    | varchar   | Related loan identifier      |
| payment_dt | date      | Parsed payment date          |
| amount     | double    | Payment amount               |
| status     | varchar   | Payment status               |

---

### Gold Layer Schema

#### KPIs Table
| Field                    | Data Type | Description                                                 |
|---------------------------|-----------|-------------------------------------------------------------|
| funded_ar                 | date      | Date for which KPIs are calculated                          |
| funded_count              | bigint    | Number of loans funded                                      |
| avg_apr                   | double    | Average Annual Percentage Rate: Upto 2 Decimal places       |
| principal_weighted_margin | double    | Margin weighted by principal amount : Upto 4 Decimal places |
| default_rate_D90          | double    | 90-day default rate : Upto 2 Decimal places                                        |

#### Alerts Table
| Field          | Data Type | Description                               |
|----------------|-----------|-------------------------------------------|
| alert_date     | date      | Date when alert was triggered             |
| default_spiked | boolean   | Indicates if default rate spiked          |
| volume_dropped | boolean   | Indicates if loan volume dropped significantly |

### Key Features
- Data Integrity: Silver layer enforces proper data types and constraints
- Structured Processing: Clear separation of raw, cleaned, and business data
- Metrics Serving: REST API provides access to calculated KPIs and alerts
- Schema Enforcement: Gold layer maintains strict schemas for reliable analytics
- Data Validation: Automated data quality checks at each layer
- Audit Trail: Full traceability from raw source to business metrics

### System Requirements

- Docker

### Installation Steps and running

### 1. Build and run containers

Build the images and start the containers:

```bash
docker-compose build --no-cache
docker-compose up -d
```
**Results Are immediately available for viewing jump to last section** 

****

### 2. View logs of a running container

```bash
docker logs -f fastapi_app
```

### 3. One encompassing command that does everything: Can be rerun.

```bash
docker exec -it fastapi_app bash -c "cd transformation_dbt && mkdir -p db && rm -f db/dev.duckdb || true && dbt clean && dbt run --select 'models/'"
```

### 4. Optional : Move local seed files into container.

```bash
docker cp /<change_accordingly>/seeds/. fastapi_app:/app/transformation_dbt/seeds/
```
- Copies all files from your local `seeds/` folder into the container.
- Overwrites files with the same name.
- **Rerun the 3rd command after doing this.**
---

### 5. Run DBT Tests

```bash
docker exec -it fastapi_app bash -c "cd transformation_dbt && dbt test"
```

### REST End Points with example for result viewing:
- For All API docs :
  http://127.0.0.1:8000/docs
- For KPI on date : 2024-01-15 ->
  http://127.0.0.1:8000/api/kpis?date=2024-01-15
- For Alerts from data : 2024-01-15 to data : 2024-01-21 ->
  http://127.0.0.1:8000/api/alerts?date_from=2024-01-15&date_to=2024-01-21
- HTML Based from data : 2024-01-15 to data : 2024-01-21 ->
  http://127.0.0.1:8000/api/report?date_from=2024-01-15&date_to=2024-01-21