resource cosmos 'Microsoft.DocumentDB/databaseAccounts@2021-06-15' = {
  name: 'billing-cosmos'
  location: resourceGroup().location
  kind: 'GlobalDocumentDB'
  properties: {
    databaseAccountOfferType: 'Standard'
  }
}

resource storage 'Microsoft.Storage/storageAccounts@2022-09-01' = {
  name: 'billingarchive'
  location: resourceGroup().location
  kind: 'StorageV2'
  sku: {
    name: 'Standard_GRS'
  }
}
