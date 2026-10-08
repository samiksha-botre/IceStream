# IceStream — Real-Time Lakehouse Observability

## 📌 Project Overview

**IceStream** is a real-time data quality and lakehouse observability project designed to process transaction data, validate its quality, detect bad data and schema changes, and store valid transactions for further analysis.

The system uses **Apache Kafka** for real-time transaction streaming and **Apache Flink** for stream processing and data quality validation. Valid transactions are then written to a lakehouse storage layer in JSON Lines (`.jsonl`) format.

---

## 🎯 Objectives

The main objectives of IceStream are:

* Generate real-time transaction data.
* Stream transactions using Apache Kafka.
* Process transactions using Apache Flink.
* Validate transaction data quality.
* Detect missing or invalid data.
* Detect schema drift.
* Store valid transactions in a lakehouse storage layer.
* Provide a foundation for future observability and analytics dashboards.

---

## 🏗️ System Architecture

```text
                 ┌─────────────────────┐
                 │   Transaction       │
                 │     Generator       │
                 │      (Python)       │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Apache Kafka     │
                 │                     │
                 │ icestream-transactions
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Apache Flink     │
                 │  Stream Processing  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  Data Quality       │
                 │    Validation       │
                 ├─────────────────────┤
                 │ VALID               │
                 │ BAD_DATA            │
                 │ SCHEMA_DRIFT        │
                 └──────────┬──────────┘
                            │
                     VALID transactions
                            │
                            ▼
                 ┌─────────────────────┐
                 │     Lakehouse       │
                 │      Storage        │
                 │   transactions.jsonl│
                 └─────────────────────┘
```

---

## 🔄 Data Processing Workflow

1. The Python transaction generator creates transaction records.
2. Transactions are published to the Kafka topic:
   `icestream-transactions`
3. Apache Flink consumes the transactions from Kafka.
4. Each transaction is converted from JSON into a Python object.
5. The transaction is passed through the data quality validator.
6. The validator checks:

   * Required fields
   * NULL values
   * Unexpected fields
   * Schema changes
7. The transaction receives a validation status:

   * `VALID`
   * `BAD_DATA`
   * `SCHEMA_DRIFT`
8. Valid transactions are written to:
   `lakehouse/data/transactions.jsonl`
9. Invalid transactions are reported by the Flink processing job.

---

## ✨ Key Features

### 1. Real-Time Transaction Streaming

Transactions are continuously generated and published to Apache Kafka.

Example fields include:

```text
transaction_id
user_id
product
amount
tax_amount
payment_method
status
timestamp
```

---

### 2. Data Quality Validation

IceStream validates incoming transactions before storing them.

The system can detect:

* Missing required fields
* NULL values
* Invalid JSON
* Unexpected fields
* Schema drift

---

### 3. Bad Data Detection

Example:

```text
Status: BAD_DATA | Message: amount is NULL
```

The system can also detect missing fields such as:

```text
Missing fields: {'transaction_id', 'user_id'}
```

---

### 4. Schema Drift Detection

IceStream detects unexpected fields added to incoming transactions.

Example:

```text
Status: SCHEMA_DRIFT | Message: Unexpected fields: {'discount'}
```

This helps identify changes in the incoming data structure.

---

### 5. Lakehouse Storage

Transactions that pass validation are written to:

```text
lakehouse/data/transactions.jsonl
```

Example:

```json
{
  "transaction_id": "TEST001",
  "user_id": "USER001",
  "product": "Laptop",
  "amount": 50000,
  "tax_amount": 9000,
  "payment_method": "UPI",
  "status": "SUCCESS",
  "timestamp": "2026-09-15T12:00:00"
}
```

---

## 🛠️ Technologies Used

| Technology           | Purpose                               |
| -------------------- | ------------------------------------- |
| Python               | Transaction generation and validation |
| Apache Kafka         | Real-time event streaming             |
| Apache Flink         | Stream processing                     |
| PyFlink              | Python-based Flink processing         |
| Kafka Python Client  | Kafka producer                        |
| JSON / JSONL         | Data format and storage               |
| Git & GitHub         | Version control                       |
| Windows / PowerShell | Development environment               |

---

## 📂 Project Structure

```text
IceStream/
│
├── dashboard/
│
├── data_generator/
│   └── generator.py
│
├── data_quality/
│   └── validator.py
│
├── docs/
│
├── flink/
│   └── transaction_quality_job.py
│
├── kafka/
│
├── lakehouse/
│   ├── config.py
│   ├── config.env
│   ├── writer.py
│   ├── README.md
│   └── data/
│       └── transactions.jsonl
│
├── tests/
│   ├── sample_transaction.json
│   ├── invalid_transaction.json
│   └── schema_drift_transaction.json
│
└── README.md
```

---

## ⚙️ Requirements

Before running IceStream, install/configure:

* Python 3.12
* Apache Kafka 4.3.1
* Apache Flink 2.2.1
* Java 17
* PyFlink 2.2.1
* Kafka Python client

---

## 🚀 Setup and Execution

### Step 1 — Start Kafka

Start the Kafka server using the Kafka installation.

Verify that Kafka is running on:

```text
localhost:9092
```

---

### Step 2 — Start Flink

Start the Flink cluster.

The Flink dashboard is available at:

```text
http://localhost:8081
```

---

### Step 3 — Start the Transaction Generator

Run:

```powershell
python data_generator/generator.py
```

The generator publishes transaction records to:

```text
icestream-transactions
```

---

### Step 4 — Run the Flink Validation Job

Run the Flink transaction quality job using the configured PyFlink environment.

The job consumes transactions from Kafka and performs validation.

---

### Step 5 — Check Validation Results

Flink produces validation results such as:

```text
Status: VALID
```

```text
Status: BAD_DATA
```

```text
Status: SCHEMA_DRIFT
```

---

### Step 6 — Check Lakehouse Data

Valid transactions are stored in:

```text
lakehouse/data/transactions.jsonl
```

---

## 🧪 Data Quality Examples

### Valid Transaction

```text
Status: VALID
Message: Transaction passed all quality checks
```

### NULL Amount

```text
Status: BAD_DATA
Message: amount is NULL
```

### NULL Tax Amount

```text
Status: BAD_DATA
Message: tax_amount is NULL
```

### Missing Fields

```text
Status: BAD_DATA
Message: Missing fields: {'transaction_id', 'user_id'}
```

### Schema Drift

```text
Status: SCHEMA_DRIFT
Message: Unexpected fields: {'discount'}
```

### Invalid JSON

```text
Status: BAD_DATA
Message: Invalid JSON
```

---

## 🔐 Data Quality Rules

The validation layer checks whether transactions contain the expected structure and valid values.

The main validation categories are:

| Validation                  | Result       |
| --------------------------- | ------------ |
| All required fields present | VALID        |
| Required field is NULL      | BAD_DATA     |
| Required field missing      | BAD_DATA     |
| Invalid JSON                | BAD_DATA     |
| Unexpected field detected   | SCHEMA_DRIFT |

---

## 📊 Current Implementation

The currently implemented pipeline is:

```text
Python Transaction Generator
          ↓
Apache Kafka
          ↓
Apache Flink / PyFlink
          ↓
Data Quality Validator
          ↓
Validation Result
          ↓
Lakehouse JSONL Storage
```

The core real-time processing and validation pipeline has been implemented and tested successfully.

---

## 🔮 Future Scope

The project can be extended with the following technologies and features:

### Apache Iceberg

Use Apache Iceberg as the table format for scalable lakehouse storage instead of basic JSONL storage.

### Great Expectations

Integrate Great Expectations for advanced data quality expectations and reporting.

### React Dashboard

Develop a React/React Flow dashboard to visualize:

* Transaction volume
* Valid vs invalid transactions
* Schema drift
* Data quality statistics
* Processing status

### Advanced Observability

Future versions can include:

* Data quality metrics
* Alerts
* Historical trends
* Monitoring dashboards
* Data quality reports

---

## 🎓 Project Outcome

IceStream demonstrates how a real-time transaction stream can be processed and validated using modern data engineering technologies.

The project successfully demonstrates:

**Real-time streaming + stream processing + data quality validation + schema drift detection + lakehouse-oriented storage.**

---

## 👩‍💻 Author

**Samiksha Botre**

BBA – Computer Applications

GitHub:
https://github.com/samiksha-botre/IceStream

---

## 📜 License

This project is developed for educational and academic purposes.
