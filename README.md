# Real-Time Stock Market Data Pipeline

## 📌 Overview
This project demonstrates an end-to-end **real-time data engineering pipeline** using **Apache Kafka, Python, and AWS**.  
It simulates stock market data, streams it through Kafka, processes it in real time, stores both raw and processed data in Amazon S3, and visualizes insights using a Streamlit dashboard.

This project mirrors real-world streaming architectures used by data engineers in production environments.

---

## 🏗️ Architecture
<img width="825" height="411" alt="flowchart" src="https://github.com/user-attachments/assets/6e2fd0b5-d279-4496-8b29-9848daa0ec5a" />


---

## 🛠️ Tech Stack
- **Apache Kafka** (EC2, KRaft mode)
- **Python** (kafka-python, pandas, boto3)
- **AWS EC2**
- **AWS S3** (Data Lake: raw & processed layers)
- **Streamlit** (Dashboard & Visualization)

---

## 🔄 Data Flow
1. A Kafka **producer** simulates stock price events.
2. Kafka **broker** ingests events in real time.
3. A Kafka **consumer**:
   - Validates data  
   - Adds ingestion timestamps  
   - Stores raw data in S3  
   - Generates processed datasets  
4. A **Streamlit dashboard** reads from S3 and displays near real-time analytics.

---

## ▶️ How to Run

### 1️⃣ Start Kafka on EC2
```
bin/kafka-server-start.sh config/server.properties
```

2️⃣ Run Kafka Producer
```
python3 producer/kafka_producer.py
```

3️⃣ Run Kafka Consumer
```
python3 consumer/kafka_s3_consumer.py
```

4️⃣ Run Dashboard
```
streamlit run dashboard/app.py
```

📊 Sample Output

Near real-time stock price updates

Raw and processed CSV files stored in Amazon S3

Live charts displayed in Streamlit

Screenshots are available in the screenshots/ folder.

🚀 Key Learnings

Event-driven data pipelines

Real-time data ingestion with Kafka

Cloud-based data lakes using S3

ETL and data transformation

Building analytical dashboards

🔒 Security Notes

IAM Roles used for secure S3 access

No AWS credentials stored in code

Sensitive files excluded via .gitignore

📌 Future Improvements

Deploy Kafka on MSK

Add schema validation with Avro

Implement monitoring (CloudWatch / Prometheus)

Automate pipeline using Airflow

👤 Author

Dhruv Pandey

MSc Data Science & AI



