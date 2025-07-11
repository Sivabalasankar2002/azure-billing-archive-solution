# Solution Description

This architecture uses Cosmos DB for recent data and Azure Blob Storage for archived billing records.

- Azure Functions archive records older than 90 days
- API function first queries Cosmos DB, then checks Blob Storage if not found
- Minimal changes, no downtime, easy cost optimization
