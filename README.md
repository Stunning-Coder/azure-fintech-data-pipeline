# NairaFlow: High-Velocity Fintech Transaction Simulator

![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

## 🚀 Overview
**NairaFlow** is a cloud-native data ingestion pipeline designed to simulate and process high-volume fintech transaction streams in the Nigerian market. 

Built on **Microsoft Azure**, this project demonstrates a scalable **Real-Time ELT architecture** capable of ingesting thousands of concurrent transaction events (Transfers, Airtime, Bill Payments) and landing them into a Data Lake for downstream analytics.

## 🏗️ Architecture
**Producer (Python/Faker)** ➡️ **Azure Event Hubs** ➡️ **Consumer Service** ➡️ **ADLS Gen2 (Bronze Layer)**

1.  **Data Generation:** A custom Python script simulates realistic Nigerian fintech transactions (currency: NGN, local banks, failure rates).
2.  **Ingestion:** Events are streamed to **Azure Event Hubs** (Standard Tier) to handle high-throughput concurrency.
3.  **Processing:** A consumer service captures the stream and batches data.
4.  **Storage:** Data is partitioned by time (`/year/month/day`) and stored as JSON blobs in **Azure Data Lake Storage Gen2**.

## 🛠️ Tech Stack
* **Cloud Provider:** Microsoft Azure
* **Ingestion:** Azure Event Hubs
* **Storage:** Azure Data Lake Storage (ADLS) Gen2
* **Language:** Python 3.12 (SDKs: `azure-eventhub`, `azure-storage-file-datalake`)
* **Security:** `python-dotenv` for environment variable management.

## ⚡ Key Features
* **Realistic Simulation:** Generates localized data (Lagos/Abuja locations, Nigerian phone formats, specific failure modes).
* **Fault Tolerance:** Implements automatic reconnection logic for network resilience.
* **Structured Storage:** Writes data to ADLS using a hierarchical namespace for optimized query performance.

## 📂 Project Structure
```bash
├── consumer_lake_loader.py  # The Ingestion Service (Event Hub -> ADLS)
├── data_generator.py        # The Transaction Simulator (Python -> Event Hub)
├── .env                     # Secrets (Not committed)
└── README.md                # Documentation
```
## 🚀 Getting Started
1. **Clone the repo:**
    ```bash
    git clone [https://github.com/Stunning-Coder/azure-fintech-data-pipeline.git](https://github.com/Stunning-Coder/azure-fintech-data-pipeline.git)

2. **Install dependencies:**

    ```bash
    pip install azure-eventhub azure-storage-file-datalake faker python-dotenv

3. **Configure `.env`: Add your Azure Connection Strings (Event Hub & ADLS).**

4. **Run the Pipeline:**

- Terminal 1: `python data_generator.py`
- Terminal 2: `python consumer_lake_loader.py`

5. **📈 Future Improvements**
- Implement Spark Structured Streaming (Databricks) for Silver/Gold transformation.
- Add Great Expectations for data quality validation on the raw stream.


**How to push this:**
```bash
# In your terminal
git add README.md
git commit -m "docs: Add project documentation"
git push
