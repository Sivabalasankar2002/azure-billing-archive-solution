# Azure Billing Records Cost Optimization

This project implements a serverless cost-optimized architecture for managing billing records in Azure. Recent records are stored in Cosmos DB, while older records are archived to Azure Blob Storage.

## Key Features

- ✅ Cosmos DB for hot data (last 3 months)
- ✅ Blob Storage archive for cold data (older than 90 days)
- ✅ Azure Functions for archival + read-through fallback
- ✅ No API contract change
- ✅ No downtime, no data loss
- ✅ Cost savings from Cosmos DB storage reduction

## Architecture

![Architecture](docs/architecture-diagram.png)

## Deployment

See `infrastructure/` for Bicep templates. Deploy using:

```bash
az deployment group create \
  --resource-group <your-rg> \
  --template-file infrastructure/main.bicep \
  --parameters @infrastructure/parameters.json
