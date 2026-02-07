import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv
from azure.eventhub import EventHubConsumerClient
from azure.storage.filedatalake import DataLakeServiceClient


# load env
load_dotenv()

# Azure config
EventHub_Connection_str = os.getenv("event_hub_conn_str")
EventHub_name = os.getenv("event_hub_name")
ADLS_conn_str = os.getenv("adls_conn_str")
container_name = "raw-data"
consumer_group = "$Default"

def upload_batch_to_lake(events):
    """Saves a batch of events as a JSON file in ADLS"""
    if not events:
        return

    # Create a unique filename based on time
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"transactions_{timestamp}.json"
    
    # Organize by Date
    folder_path = datetime.now().strftime("transactions/%Y/%m/%d")
    full_path = f"{folder_path}/{file_name}"

    # Prepare data
    data_str = json.dumps(events, indent=2)

    try:
        # Connect to Data Lake
        service_client = DataLakeServiceClient.from_connection_string(ADLS_conn_str)
        file_system_client = service_client.get_file_system_client(file_system=container_name)
        
        # Create directory if not exists
        directory_client = file_system_client.get_directory_client(folder_path)
        if not directory_client.exists():
            directory_client.create_directory()

        # Create and write file
        file_client = directory_client.get_file_client(file_name)
        file_client.upload_data(data_str, overwrite=True)
        
        print(f"💾 Saved {len(events)} events to ADLS: {full_path}")

    except Exception as e:
        print(f"❌ Error uploading to Lake: {e}")

def on_event(partition_context, event):
    # In a real app, we'd batch these. For this demo, we print and simulate a save.
    
    print(f"📥 Received event from partition: {partition_context.partition_id}")
    
    # Extract the JSON body
    body = event.body_as_json()
    
    # For this demo, we'd save ONE file per event (inefficient but proves the point)
    upload_batch_to_lake([body])
    
    # Update checkpoint (mark as read)
    partition_context.update_checkpoint(event)

def main():
    client = EventHubConsumerClient.from_connection_string(
        EventHub_Connection_str,
        consumer_group=consumer_group,
        eventhub_name=EventHub_name,
    )

    print("👂 Listening for events...")
    with client:
        client.receive(
            on_event=on_event, 
            starting_position="-1",  # Read from beginning of stream
        )

if __name__ == "__main__":
    main()