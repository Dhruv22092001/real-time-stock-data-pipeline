
import streamlit as st
import pandas as pd
import boto3
import plotly.express as px

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
BUCKET_NAME = 'stock-market-stream-data'   # S3 bucket name
DATA_PREFIX = 'processed/'                 # Read processed data only

# Create S3 client (uses EC2 IAM Role)
s3 = boto3.client('s3')

# ---------------------------------------------------------
# STREAMLIT UI
# ---------------------------------------------------------
st.title("📈 Stock Market Real-Time Dashboard")
st.write("Visualizing Kafka streaming data stored in Amazon S3")

# ---------------------------------------------------------
# LIST FILES FROM S3
# ---------------------------------------------------------
objects = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=DATA_PREFIX)

if 'Contents' in objects:
    # Get all processed files
    files = [obj['Key'] for obj in objects['Contents']]

    # Select the most recent file
    latest_file = sorted(files)[-1]
    st.success(f"Showing latest data file: {latest_file}")

    # ---------------------------------------------------------
    # LOAD CSV DATA FROM S3
    # ---------------------------------------------------------
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=latest_file)
    df = pd.read_csv(obj['Body'])

    # Display last few records
    st.subheader("Latest Streaming Records")
    st.dataframe(df.tail(10), use_container_width=True)

    # ---------------------------------------------------------
    # PRICE TIME SERIES PLOT
    # ---------------------------------------------------------
    st.subheader("Stock Price Over Time")
    fig = px.line(
        df,
        x='ingestion_time',
        y='price',
        title='Stock Prices Over Time',
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

    # ---------------------------------------------------------
    # MOVING AVERAGE PLOT (IF AVAILABLE)
    # ---------------------------------------------------------
    if 'moving_avg_3' in df.columns:
        st.subheader("3-Point Moving Average")
        fig2 = px.line(
            df,
            x='ingestion_time',
            y='moving_avg_3',
            title='Moving Average (Window = 3)',
            markers=True
        )
        st.plotly_chart(fig2, use_container_width=True)

else:
    st.warning("No processed data found in S3 yet.")
