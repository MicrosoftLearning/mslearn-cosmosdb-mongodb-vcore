# Add parameters for the language, use of .env file, creation flags, location and subscription
param (
    [bool]$useEnvFile = $true, # Use the .env file to get the values for the parameters
    [bool]$updateEnvFile = $true, # Update the .env file with the values for the parameters

    [Int32]$randomIdentifier, # A random identifier to make the resource names unique
    [string]$location, # The location for the resources
    [string]$subscriptionName, # The subscription name to use
    [string]$resourceGroup, # The resource group to use

    [bool]$changeSubscription = $false, # Change the subscription to the one specified
    [bool]$skipCreatingResourceGroup = $false, # Skip creating the resource group
    [bool]$skipCreatingCosmosDBCluster = $false, # Skip creating the Cosmos DB cluster
    [bool]$skipCreatingCosmosDBPublicIPFirewallRule = $false, # Skip creating the Cosmos DB public IP firewall rule

    [string]$cosmosCluster, # The name of the Cosmos DB cluster
    [string]$cosmosClusterLocation, # The location for the Cosmos DB cluster
    [string]$cosmosClusterAdmin, # The admin username for the Cosmos DB cluster
    [String]$cosmosClusterPassword, # The admin password for the Cosmos DB cluster
    [string]$cosmosDatabase # The name of the Cosmos DB database
)

# Determine the .env file path
$envFilePath = "./.env"

# Read the .env file
$envFileContent = Get-Content -Path $envFilePath

# Parse the .env file content into a hashtable
$envVars = @{}
foreach ($line in $envFileContent) {
    if ($line -match '^(.*?)=(.*)$') {
        $key = $matches[1].Trim('"')
        $value = $matches[2].Trim('"')
        $envVars[$key] = $value
    }
}

if ($useEnvFile) {
    if ($envVars['changeSubscription'] -eq 'true') { $changeSubscription = $true }
    if ($envVars['skipCreatingResourceGroup'] -eq 'true') { $skipCreatingResourceGroup = $true }
    if ($envVars['skipCreatingCosmosDBCluster'] -eq 'true') { $skipCreatingCosmosDBCluster = $true }
    if ($envVars['skipCreatingCosmosDBPublicIPFirewallRule'] -eq 'true') { $skipCreatingCosmosDBPublicIPFirewallRule = $true }
} 

# Error variable to track if there are any creation errors
$changeSubscriptionError = $null
$CreatingResourceGroupError = $null
$CreatingCosmosDBClusterError = $null

# Use the values from the parameters if they exist, otherwise use the values from the .env file if they exist and $useEnvFile is true, otherwise calculate them
$randomIdentifier = if ($randomIdentifier) { $randomIdentifier } elseif ($useEnvFile -and $envVars['randomIdentifier']) { $envVars['randomIdentifier'] } else { Get-Random }
$location = if ($location) { $location } elseif ($useEnvFile -and $envVars['location']) { $envVars['location'] } else { "eastus" }

$subscriptionName = if ($subscriptionName) { $subscriptionName } elseif ($useEnvFile -and $envVars['subscriptionName']) { $envVars['subscriptionName'] } elseif ($changeSubscription) { $input = Read-Host "Please enter your Subscription Name or press Enter to use the default"; if ($input) { $input } else { (az account show --query name -o tsv --only-show-errors) } } else { (az account show --query name -o tsv --only-show-errors) }

if ($changeSubscription) {
    try {
        $output = az account set --subscription $subscriptionName --only-show-errors
        if ($LASTEXITCODE -ne 0) {
            throw $output
        }
    }
    catch {
        $changeSubscriptionError = $_.Exception.Message
        Write-Host "Error changing the subscription to $subscriptionName - $changeSubscriptionError"
    }
}

# Set the resource group
$resourceGroup = if ($resourceGroup) {$resourceGroup} elseif ($useEnvFile -and $envVars['resourceGroup']) { $envVars['resourceGroup'] } else { "msdocs-cosmosdb-rg-$randomIdentifier" }

# Create a resource group
if (! $skipCreatingResourceGroup) {
    Write-Host "Creating $resourceGroup in $location..."
    Write-Host

    try {
        $output = az group create --name $resourceGroup --location $location --only-show-errors
        if ($LASTEXITCODE -ne 0) {
            throw $output
        }
    }
    catch {
        $CreatingResourceGroupError = $_.Exception.Message
        Write-Host "Error creating the resource group $resourceGroup - $CreatingResourceGroupError"
    }
}


# Create MongoDB resources
$cosmosCluster = if ($cosmosCluster) {$cosmosCluster} elseif ($useEnvFile -and $envVars['cosmosCluster']) { $envVars['cosmosCluster'] } else { "msdocs-account-cosmos-cluster-$randomIdentifier" } #needs to be lower case
$cosmosClusterLocation = if ($cosmosClusterLocation) {$cosmosClusterLocation} elseif ($useEnvFile -and $envVars['cosmosClusterLocation']) { $envVars['cosmosClusterLocation'] } else { $location } 
$cosmosClusterAdmin = if ($cosmosClusterAdmin) {$cosmosClusterAdmin} elseif ($useEnvFile -and $envVars['cosmosClusterAdmin']) { $envVars['cosmosClusterAdmin'] } else { "clusteradmin$randomIdentifier" }
$tempPW = -join ((48..57) + (65..90) + (97..122) + (33..33) + (36..38) + (40..47) + (58..64) + (91..95) + (123..126) | Get-Random -Count 16 | % {[char]$_})
$cosmosClusterPassword = if ($cosmosClusterPassword) {$cosmosClusterPassword} elseif ($useEnvFile -and $envVars['cosmosClusterPassword']) { $envVars['cosmosClusterPassword'] } else { $tempPW  }
$cosmosDatabase = if ($cosmosDatabase) {$cosmosDatabase} elseif ($useEnvFile -and $envVars['cosmosDatabase']) { $envVars['cosmosDatabase'] } else { "cosmicworks" }

if (! $skipCreatingCosmosDBPublicIPFirewallRule) {
    # Create a public IP firewall rule for the Cosmos DB account
    $publicIpRuleName = "msdocs-cosmosdb-fw_rule-$randomIdentifier"
    $publicIp = (Invoke-RestMethod -Uri http://ipinfo.io/json).ip
} 
else { 
    $publicIpRuleName = "labMachineIPAccessRule"
    $publicIp = "0.0.0.0"
}
    
# Create a Cosmos DB for MongoDB vCore cluster
if (! $skipCreatingCosmosDBCluster) {
    Write-Host
    Write-Host "Creating $cosmosCluster cluster, this could take 10+ minutes to create..."
    Write-Host

    try {
        $output = az deployment group create --resource-group $resourceGroup --template-file 'create-mongodb-vcore-cluster.bicep' --parameters "clusterName=`"$cosmosCluster`"" "location=`"$cosmosClusterLocation`"" "adminUsername=`"$cosmosClusterAdmin`"" "adminPassword=`"$cosmosClusterPassword`"" "publicIpRuleName=`"$publicIpRuleName`"" "publicIp=`"$publicIp`"" --only-show-errors
        if ($LASTEXITCODE -ne 0) {
            throw $output
        }
    }
    catch {
        $CreatingCosmosDBClusterError = $_.Exception.Message
        Write-Host "Error creating the Cosmos DB cluster $cosmosCluster - $CreatingCosmosDBClusterError"
    }
}

# Get the endpoint for the Cosmos DB account
$cosmosDbEndpoint = if ($useEnvFile -and $envVars['cosmosDbEndpoint']) { $envVars['cosmosDbEndpoint'] } else { "mongodb+srv://<user>:<password>@$cosmosCluster.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000" }

# Write the .env file
if ($updateEnvFile) {
    $envVars = [ordered]@{
        "randomIdentifier" = if ($randomIdentifier) { "$randomIdentifier" } else { "" }
        "location" = if ($location) { "`"$location`"" } else { "" }
        "changeSubscription" = if ($changeSubscription) { "true" } else { "" }
        "subscriptionName" = if ($subscriptionName) { "`"$subscriptionName`"" } else { "" }
        "skipCreatingResourceGroup" = if ($skipCreatingResourceGroup) { "true" } else { "" }
        "resourceGroup" = if ($resourceGroup) { "`"$resourceGroup`"" } else { "" }

        "skipCreatingCosmosDBCluster" = if ($skipCreatingCosmosDBCluster) { "true" } else { "" }
        "skipCreatingCosmosDBPublicIPFirewallRule" = if ($skipCreatingCosmosDBPublicIPFirewallRule) { "true" } else { "" }
        "cosmosCluster" = if ($cosmosCluster) { "`"$cosmosCluster`"" } else { "" }
        "cosmosClusterLocation" = if ($cosmosClusterLocation) { "`"$cosmosClusterLocation`"" } else { "" }
        "cosmosDbEndpoint" = if ($cosmosDbEndpoint) { "`"$cosmosDbEndpoint`"" } else { "" }
        "cosmosClusterAdmin" = if ($cosmosClusterAdmin) { "`"$cosmosClusterAdmin`"" } else { "" }
        "cosmosClusterPassword" = if ($cosmosClusterPassword) { "`"$cosmosClusterPassword`"" } else { "" }
        "cosmosDatabase" = if ($cosmosDatabase) { "`"$cosmosDatabase`"" } else { "`"cosmicworks`"" }
    }

    # We group the environment variables to improve readability and organization.
    # Each group represents a different service or component of your application.
    # This makes it easier to manage and update the variables related to each component.

    $group1 = $envVars.Keys[0..5]  # Variables related to Azure subscription and resource group
    $group2 = $envVars.Keys[6..13]  # Variables related to Cosmos DB
    
    $groups = @($group1, $group2)
    
    $output = $groups | ForEach-Object {
        $group = $_
        $group | ForEach-Object {
            "$($_)=$($envVars[$_])"
        }
        ""  # Add a blank line for the component group separation
    }
    
    $output | Out-File -FilePath $envFilePath -Encoding utf8
}

# Output the resources
Write-Host
Write-Host "*************** Resources ***************"
Write-Host
write-host "Random Identifier: $randomIdentifier"
write-host 
Write-Host "Change subscription status (skipped by default): " -NoNewline
if (! $changeSubscription) { Write-Host "Skipped" -ForegroundColor Yellow } elseif (  $null -ne $changeSubscriptionError ){ Write-Host "Failed" -ForegroundColor Red } else { Write-Host "Success" -ForegroundColor Green }
if ($null -ne $changeSubscriptionError) { Write-Host "Change subscription error: "  -NoNewline  } if ($null -ne $changeSubscriptionError) { Write-Host $changeSubscriptionError -ForegroundColor Red}
Write-Host "Subscription name: $subscriptionName"
Write-Host
Write-Host "Resource group creation status: " -NoNewline
if ($skipCreatingResourceGroup) { Write-Host "Skipped" -ForegroundColor Yellow } elseif (  $null -ne $CreatingResourceGroupError ){ Write-Host "Failed" -ForegroundColor Red } else { Write-Host "Success" -ForegroundColor Green }
if ($null -ne $CreatingResourceGroupError) { Write-Host "Resource group creation error: "  -NoNewline  } if ($null -ne $CreatingResourceGroupError) { Write-Host $CreatingResourceGroupError -ForegroundColor Red}
Write-Host "Resource group: $resourceGroup"
Write-Host "Location: $location"
Write-Host
Write-Host "Cosmos DB creation status: " -NoNewline
if ($skipCreatingCosmosDBCluster) { Write-Host "Skipped" -ForegroundColor Yellow } elseif (  $null -ne $CreatingCosmosDBClusterError ){ Write-Host "Failed" -ForegroundColor Red } else { Write-Host "Success" -ForegroundColor Green }
if ($null -ne $CreatingCosmosDBClusterError) { Write-Host "Cosmos DB creation error: "  -NoNewline  } if ($null -ne $CreatingCosmosDBClusterError) { Write-Host $CreatingCosmosDBClusterError -ForegroundColor Red}
Write-Host "Cosmos Cluster Name: $cosmosCluster"
Write-Host "Cosmos Cluster Location: $cosmosClusterLocation"
Write-Host "Cosmos Cluster Admin: $cosmosClusterAdmin"
Write-Host "Cosmos Cluster Admin Password: $cosmosClusterPassword"
Write-Host "Cosmos DB Endpoint: $cosmosDbEndpoint"
Write-Host "Cosmos Database: $cosmosDatabase"
Write-Host
Write-Host "*************** Resources ***************"