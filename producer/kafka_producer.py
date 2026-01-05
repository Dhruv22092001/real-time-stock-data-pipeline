
from kafka import KafkaProducer
from json import dumps
import time

# ---------------------------------------------------------
# Kafka Producer Configuration
# ---------------------------------------------------------
# - Connects to Kafka broker running on localhost:9092
# - Serializes Python dictionaries into JSON bytes
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

# ---------------------------------------------------------
# Continuous data streaming loop
# ---------------------------------------------------------
# This simulates a real-time stock price feed
# A new stock price message is sent every 2 seconds
while True:
    # Send a message to the 'stock-prices' Kafka topic
    producer.send(
        'stock-prices',
        {
            'price': 123,        # Simulated stock price
            'symbol': 'AAPL'     # Stock ticker symbol
        }
    )

    # Ensure all buffered messages are sent to Kafka
    producer.flush()

    # Log message delivery to the console
    print("Message sent")

    # Pause for 2 seconds before sending the next message
    time.sleep(2)
