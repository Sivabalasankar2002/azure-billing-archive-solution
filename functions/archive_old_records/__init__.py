import os
import json
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient

def main(timer):
    cosmos_client = CosmosClient(os.environ['COSMOS_ENDPOINT'], os.environ['COSMOS_KEY'])
    db_client = cosmos_client.get_database_client(os.environ['COSMOS_DB'])
    container = db_client.get_container_client(os.environ['COSMOS_CONTAINER'])

    blob_service = BlobServiceClient.from_connection_string(os.environ['BLOB_CONNECTION_STRING'])
    cutoff = datetime.utcnow() - timedelta(days=90)

    for item in container.query_items(
        query=f"SELECT * FROM c WHERE c._ts < {int(cutoff.timestamp())}",
        enable_cross_partition_query=True
    ):
        ts = datetime.utcfromtimestamp(item['_ts'])
        blob_path = f"{ts.year}/{ts.month:02}/{ts.day:02}/{item['id']}.json"
        blob_client = blob_service.get_blob_client(container='billing-archive', blob=blob_path)
        blob_client.upload_blob(json.dumps(item), overwrite=True)
        container.delete_item(item=item['id'], partition_key=item['partitionKey'])
