import os
import time
import json
import random
from dotenv import load_dotenv
from faker import Faker
from azure.eventhub import EventHubProducerClient, EventData
from azure.eventhub.exceptions import EventHubError, ConnectError
import logging

load_dotenv()

#Init Azure
Connection_str = os.getenv("event_hub_conn_str")
EventHub_name = os.getenv("event_hub_name")
# error logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#Init Faker
fake = Faker('en_NG')

def generate_transaction():
    """Generates a realistic Fintech transaction"""
    return {
        "transaction_id": fake.uuid4(),
        "timestamp": fake.iso8601(),
        "customer_id": f"CUST-{random.randint(10000, 99999)}",
        "amount": round(random.uniform(500.00, 150000.00),2),
        "currency": "NGN",
        "narration": random.choice(["Airtime Purchase", "DSTV sub", "Food", "Uber Ride", "Transfer to Opay"]),
        "status": random.choices(["success","failed", "pending"], weights=[80, 10,10]),
        "location": fake.state(),
        "device_os": random.choice(["iOS", "Android", "Web"]),
    }

def send_data():
    while True:  # Outer loop for reconnection
        try:
            logger.info("🔌 Connecting to Azure Event Hub...")
            producer = EventHubProducerClient.from_connection_string(
                conn_str=Connection_str, 
                eventhub_name=EventHub_name
            )

            with producer:
                logger.info("✅ Connected! Starting data stream...")
                
                while True:  # Inner loop for sending data
                    batch = producer.create_batch()
                    
                    # Generate a small batch (e.g., 5 events)
                    for _ in range(5):
                        txn = generate_transaction()
                        json_data = json.dumps(txn)
                        batch.add(EventData(json_data))
                        logger.info(f"💸 Generated: {txn['amount']} NGN | {txn['narration']}")

                    # Send the batch
                    producer.send_batch(batch)
                    logger.info(f"🚀 Batch sent successfully. Sleeping for 2s...")
                    time.sleep(2)
        
        except KeyboardInterrupt:
            logger.info("🛑 Stopping script manually...")
            break  # Exit the script

        except (ConnectError, EventHubError) as e:
            logger.error(f"❌ Azure Connection Error: {e}")
            logger.info("⚠️  Reconnecting in 5 seconds...")
            time.sleep(5)  # Wait before retrying

        except Exception as e:
            logger.error(f"❌ Unexpected Error: {e}")
            logger.info("⚠️  Retrying in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    send_data()