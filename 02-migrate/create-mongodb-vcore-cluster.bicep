
@description('Azure Cosmos DB MongoDB vCore cluster name')
@maxLength(40)
param clusterName string = '' //= 'msdocs-${uniqueString(resourceGroup().id)}'

@description('Location for the cluster.')
param location string = '' //= resourceGroup().location

@description('Username for admin user')
param adminUsername string = ''

@description('Public IP address to allow access to the cluster')
param publicIp string = '0.0.0.0'

@description('Public IP address rule name for local access to the cluster')
param publicIpRuleName string = 'labMachineIPAccessRule'

@secure()
@description('Password for admin user')
//@minLength(8)
@maxLength(128)
param adminPassword string = ''

resource cluster 'Microsoft.DocumentDB/mongoClusters@2023-03-01-preview' = {
  name: clusterName
  location: location
  properties: {
    administratorLogin: adminUsername
    administratorLoginPassword: adminPassword
    nodeGroupSpecs: [
        {
            kind: 'Shard'
            nodeCount: 1
            sku: 'M30'
            diskSizeGB: 128
            enableHa: false
        }
    ]
  }
}



resource firewallRules 'Microsoft.DocumentDB/mongoClusters/firewallRules@2023-03-01-preview' = {
  parent: cluster
  name: 'AllowAllAzureServices'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0'
  }
}

resource firewallRules_local_access 'Microsoft.DocumentDB/mongoClusters/firewallRules@2023-03-01-preview' = {
  parent: cluster
  name: publicIpRuleName
  properties: {
    startIpAddress: publicIp
    endIpAddress: publicIp
  }
}
