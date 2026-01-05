
from kafka import KafkaConsumer
import json
import boto3
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
TOPIC = 'stock-prices'                     # Kafka topic to consume from
BOOTSTRAP_SERVERS = 'localhost:9092'       # Kafka broker address
BUCKET_NAME = 'stock-market-stream-data'   # S3 bucket for storing data
BATCH_SIZE = 10                            # Number of messages per batch upload

# ---------------------------------------------------------
# KAFKA CONSUMER SETUP
# ---------------------------------------------------------
# - Reads messages from Kafka topic
# - Automatically commits offsets
# - Deserializes JSON messages into Python dictionaries
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    auto_offset_reset='latest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# ---------------------------------------------------------
# S3 CLIENT (IAM ROLE BASED AUTH)
# ---------------------------------------------------------
# Uses EC2 IAM role for secure access (no hardcoded keys)
s3 = boto3.client('s3')

print("Kafka consumer started...")

# ---------------------------------------------------------
# IN-MEMORY BUFFER FOR BATCH PROCESSING
# ---------------------------------------------------------
data_buffer = []

# ---------------------------------------------------------
# CONSUME STREAMING DATA
# ---------------------------------------------------------
for message in consumer:
    # Extract message value
    record = message.value

    # Add ingestion timestamp (data engineering best practice)
    record['ingestion_time'] = datetime.utcnow().isoformat()
    data_buffer.append(record)

    print("Consumed:", record)

    # ---------------------------------------------------------
    # BATCH UPLOAD TO S3 (RAW + PROCESSED)
    # ---------------------------------------------------------
    if len(data_buffer) >= BATCH_SIZE:
        # ---------------- RAW DATA ----------------
        df_raw = pd.DataFrame(data_buffer)
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')

        file_raw = f"stock_data_raw_{timestamp}.csv"
        df_raw.to_csv(file_raw, index=False)

        # Upload raw data to S3
        s3.upload_file(file_raw, BUCKET_NAME, f"raw/{file_raw}")
        print(f"Uploaded raw data to S3: raw/{file_raw}")

        # ---------------- PROCESSED DATA ----------------
        df_processed = df_raw.copy()

        # Feature engineering
        df_processed['price_change'] = df_processed['price'].pct_change()
        df_processed['moving_avg_3'] = df_processed['price'].rolling(window=3).mean()

        # Basic data quality filter
        df_processed = df_processed[df_processed['price'] > 0]

        file_processed = f"stock_data_processed_{timestamp}.csv"
        df_processed.to_csv(file_processed, index=False)

        # Upload processed data to S3
        s3.upload_file(file_processed, BUCKET_NAME, f"processed/{file_processed}")
        print(f"Uploaded processed data to S3: processed/{file_processed}")

        # Clear buffer for next batch
        data_buffer.clear()
