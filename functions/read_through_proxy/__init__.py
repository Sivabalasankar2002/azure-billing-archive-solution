import os
import json
import azure.functions as func
from azure.cosmos import CosmosClient, exceptions
from azure.storage.blob import BlobServiceClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    record_id = req.params.get('id')
    if not record_id:
        return func.HttpResponse("Record ID required", status_code=400)

    cosmos_client = CosmosClient(os.environ['COSMOS_ENDPOINT'], os.environ['COSMOS_KEY'])
    container = cosmos_client.get_database_client(os.environ['COSMOS_DB']) \
        .get_container_client(os.environ['COSMOS_CONTAINER'])

    try:
        record = container.read_item(item=record_id, partition_key=record_id)
        return func.HttpResponse(json.dumps(record), mimetype="application/json")
    except exceptions.CosmosResourceNotFoundError:
        blob_service = BlobServiceClient.from_connection_string(os.environ['BLOB_CONNECTION_STRING'])

        for year in range(2020, 2030):
            for month in range(1, 13):
                for day in range(1, 32):
                    path = f"{year}/{month:02}/{day:02}/{record_id}.json"
                    blob_client = blob_service.get_blob_client(container='billing-archive', blob=path)
                    if blob_client.exists():
                        data = blob_client.download_blob().readall()
                        return func.HttpResponse(data, mimetype="application/json")

    return func.HttpResponse("Record not found", status_code=404)
