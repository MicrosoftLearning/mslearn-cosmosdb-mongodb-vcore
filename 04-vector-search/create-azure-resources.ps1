# Add parameters for the language, use of .env file, creation flags, location and subscription
param (
    [Parameter(Mandatory=$false)]
    [bool]$useEnvFile = $true,

    [Parameter(Mandatory=$false)]
    [bool]$updateEnvFile = $true,

    [Parameter(Mandatory=$false)]
    [string]$location,

    [Parameter(Mandatory=$false)]
    [string]$subscriptionName,

    [Parameter(Mandatory=$false)]
    [string]$resourceGroup,

    [Parameter(Mandatory=$false)]
    [bool]$skipCreatingResourceGroup = $false,

    [Parameter(Mandatory=$false)]
    [bool]$skipCreatingCosmosDBCluster = $false,

    [Parameter(Mandatory=$false)]
    [bool]$skipCreatingCosmosDBPublicIPFirewallRule = $false,

    [Parameter(Mandatory=$false)]
    [bool]$skipCreatingAzureOpenAIAccount = $false,

    [Parameter(Mandatory=$false)]
    [bool]$skipCreatingAzureOpenAIDeployment = $false,

    [Parameter(Mandatory=$false)]
    [bool]$skipCreatingAzureOpenAICompletionDeployment = $false,

    [Parameter(Mandatory=$false)]
    [bool]$changeSubscription = $false,

    [Parameter(Mandatory=$false)]
    [string]$cosmosCluster,

    [Parameter(Mandatory=$false)]
    [string]$cosmosClusterAdmin,

    [Parameter(Mandatory=$false)]
    [String]$cosmosClusterPassword,

    [Parameter(Mandatory=$false)]
    [string]$cosmosDatabase,

    [Parameter(Mandatory=$false)]
    [string]$OpenAIAccount,

    [Parameter(Mandatory=$false)]
    [string]$OpenAIDeploymentName,

    [Parameter(Mandatory=$false)]
    [string]$OpenAIDeploymentModel,

    [Parameter(Mandatory=$false)]
    [string]$OpenAIDeploymentModelVersion,

    [Parameter(Mandatory=$false)]
    [string]$OpenAICompletionDeploymentName,

    [Parameter(Mandatory=$false)]
    [string]$OpenAICompletionDeploymentModel,

    [Parameter(Mandatory=$false)]
    [string]$OpenAICompletionDeploymentModelVersion
)

# Determine the .env file path based on the language
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
# Use the values from the parameters if they exist, otherwise use the values from the .env file if they exist and $useEnvFile is true, otherwise calculate them
$randomIdentifier = if ($useEnvFile -and $envVars['randomIdentifier']) { $envVars['randomIdentifier'] } else { Get-Random }
$location = if ($location) { $location } elseif ($useEnvFile -and $envVars['location']) { $envVars['location'] } else { "eastus" }

$subscriptionName = if ($subscriptionName) { $subscriptionName } elseif ($useEnvFile -and $envVars['subscriptionName']) { $envVars['subscriptionName'] } elseif ($changeSubscription) { $input = Read-Host "Please enter your Subscription Name or press Enter to use the default"; if ($input) { $input } else { (az account show --query name -o tsv --only-show-errors) } } else { (az account show --query name -o tsv --only-show-errors) }
if ($changeSubscription) {
    az account set --subscription $subscriptionName --only-show-errors
}

# Set the resource group
$resourceGroup = if ($resourceGroup) {$resourceGroup} elseif ($useEnvFile -and $envVars['resourceGroup']) { $envVars['resourceGroup'] } else { "msdocs-cosmosdb-rg-$randomIdentifier" }

# Create a resource group
if (! $skipCreatingResourceGroup) {
    Write-Host "Creating $resourceGroup in $location..."
    Write-Host

    az group create --name $resourceGroup --location $location --only-show-errors
}

# Create MongoDB resources
$cosmosCluster = if ($cosmosCluster) {$cosmosCluster} elseif ($useEnvFile -and $envVars['cosmosCluster']) { $envVars['cosmosCluster'] } else { "msdocs-account-cosmos-cluster-$randomIdentifier" } #needs to be lower case
$cosmosClusterAdmin = if ($cosmosClusterAdmin) {$cosmosClusterAdmin} elseif ($useEnvFile -and $envVars['cosmosClusterAdmin']) { $envVars['cosmosClusterAdmin'] } else { "clusteradmin$randomIdentifier" }
$tempPW = -join ((48..57) + (65..90) + (97..122) + (33..33) + (36..38) + (40..47) + (58..64) + (91..95) + (123..126) | Get-Random -Count 16 | % {[char]$_})
$cosmosClusterPassword = if ($cosmosClusterPassword) {$cosmosClusterPassword} elseif ($useEnvFile -and $envVars['cosmosClusterPassword']) { $envVars['cosmosClusterPassword'] } else { $tempPW  }
$cosmosDatabase = if ($cosmosDatabase) {$cosmosDatabase} elseif ($useEnvFile -and $envVars['cosmosDatabase']) { $envVars['cosmosDatabase'] } else { "cosmicworks" }

# Get the public IP address
$publicIp = Invoke-RestMethod -Uri 'http://ipinfo.io/ip' -Method Get
$publicIpRuleName = "msdocs-cosmosdb-fw_rule-$randomIdentifier"

# Create a Cosmos DB for MongoDB vCore cluster
if (! $skipCreatingCosmosDBCluster) {
    Write-Host
    Write-Host "Creating $cosmosCluster cluster, this could take 10+ minutes to create..."
    Write-Host

    az deployment group create --resource-group $resourceGroup --template-file 'create-mongodb-vcore-cluster.bicep' --parameters "clusterName=`"$cosmosCluster`"" "location=`"$location`"" "adminUsername=`"$cosmosClusterAdmin`"" "adminPassword=`"$cosmosClusterPassword`"" "publicIpRuleName=`"$publicIpRuleName`"" "publicIp=`"$publicIp`"" --only-show-errors
}

# Get the endpoint for the Cosmos DB account
$cosmosDbEndpoint = if ($useEnvFile -and $envVars['cosmosDbEndpoint']) { $envVars['cosmosDbEndpoint'] } else { "mongodb+srv://<user>:<password>@$cosmosCluster.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000" }


# Create an Azure OpenAI resource
$OpenAIAccount = if ($OpenAIAccount) {$OpenAIAccount} elseif ($useEnvFile -and $envVars['OpenAIAccount']) { $envVars['OpenAIAccount'] } else { "msdocs-account-openai-$randomIdentifier" } #needs to be lower case

# Create an Azure OpenAI account
if (! $skipCreatingAzureOpenAIAccount) {
    Write-Host
    Write-Host "Creating OpenAI account $OpenAIAccount in $location..."
    Write-Host

    az cognitiveservices account create --name $OpenAIAccount --resource-group $resourceGroup --location $location --kind OpenAI --sku s0 --custom-domain $OpenAIAccount --only-show-errors
}

$OpenAIDeploymentName = if ($OpenAIDeploymentName) {$OpenAIDeploymentName} elseif ($useEnvFile -and $envVars['OpenAIDeploymentName']) { $envVars['OpenAIDeploymentName'] } else { "msdocs-account-openai-deployment-$randomIdentifier" }
$OpenAIDeploymentModel = if ($OpenAIDeploymentModel) {$OpenAIDeploymentModel} elseif ($useEnvFile -and $envVars['OpenAIDeploymentModel']) { $envVars['OpenAIDeploymentModel'] } else { "text-embedding-ada-002" }
$OpenAIDeploymentModelVersion = if ($OpenAIDeploymentModelVersion) {$OpenAIDeploymentModelVersion} elseif ($useEnvFile -and $envVars['OpenAIDeploymentModelVersion']) { $envVars['OpenAIDeploymentModelVersion'] } else { "2" }

# Create a new deployment for the Azure OpenAI account
if (! $skipCreatingAzureOpenAIDeployment) {
    Write-Host
    Write-Host "Creating OpenAI deployment $OpenAIDeploymentName in $location..."
    Write-Host

    az cognitiveservices account deployment create --name $OpenAIAccount --resource-group $resourceGroup --deployment-name $OpenAIDeploymentName --model-name $OpenAIDeploymentModel --model-version $OpenAIDeploymentModelVersion --model-format OpenAI --sku-capacity 100 --sku-name "Standard" --only-show-errors 
}

$OpenAICompletionDeploymentName = if ($OpenAICompletionDeploymentName) {$OpenAICompletionDeploymentName} elseif ($useEnvFile -and $envVars['OpenAICompletionDeploymentName']) { $envVars['OpenAICompletionDeploymentName'] } else { "msdocs-account-openai-completion-$randomIdentifier" }
$OpenAICompletionDeploymentModel = if ($OpenAICompletionDeploymentModel) {$OpenAICompletionDeploymentModel} elseif ($useEnvFile -and $envVars['OpenAICompletionDeploymentModel']) { $envVars['OpenAICompletionDeploymentModel'] } else { "gpt-35-turbo" }
$OpenAICompletionDeploymentModelVersion = if ($OpenAICompletionDeploymentModelVersion) {$OpenAICompletionDeploymentModelVersion} elseif ($useEnvFile -and $envVars['OpenAICompletionDeploymentModelVersion']) { $envVars['OpenAICompletionDeploymentModelVersion'] } else { "0301" }

# Create a new completion deployment for the Azure OpenAI account
if (! $skipCreatingAzureOpenAICompletionDeployment) {
    Write-Host
    Write-Host "Creating OpenAI completetion deployment $OpenAICompletionDeploymentName in $location..."
    Write-Host

    az cognitiveservices account deployment create --name $OpenAIAccount --resource-group $resourceGroup --deployment-name $OpenAICompletionDeploymentName --model-name $OpenAICompletionDeploymentModel --model-version $OpenAICompletionDeploymentModelVersion --model-format OpenAI --sku-capacity 100 --sku-name "Standard" --only-show-errors 
}

# Get the keys and endpoint for the OpenAI accountIn case there's a delay in the deployment creation. 
# We'll retry a few times to get the keys and endpoint, waiting 30 seconds at a time for up to 5 minutes
$OpenAIEndpoint = if ($useEnvFile -and $envVars['OpenAIEndpoint']) { $envVars['OpenAIEndpoint'] } else { az cognitiveservices account show --name $OpenAIAccount --resource-group $resourceGroup --query "endpoint" -o tsv  --only-show-errors }
$OpenAIKeys = $null
$retries = 0

while (($null -eq $OpenAIEndpoint   -or $null -eq $OpenAIKeys) -and $retries -lt 10) {
    if ($null -eq $OpenAIEndpoint) {
        $OpenAIEndpoint = az cognitiveservices account show --name $OpenAIAccount --resource-group $resourceGroup --query "properties.endpoint" -o tsv --only-show-errors
    }

    if ($null -eq $OpenAIKeys) {
        $OpenAIKeys = az cognitiveservices account keys list --name $OpenAIAccount --resource-group $resourceGroup --query "{key1:key1, key2:key2}" -o tsv --only-show-errors
    }

    if (($null -eq $OpenAIEndpoint -or $null -eq $OpenAIKeys) -and $retries -eq 0) {
        Write-Host
        Write-Host "Waiting up to 5 minutes for OpenAI account to provide keys and endpoint..."
        Write-Host
    }

    Start-Sleep -Seconds 30
    $retries++
}

if ($null -eq $OpenAIEndpoint -or $null -eq $OpenAIKeys) {
    Write-Host
    Write-Host "Failed to retrieve OpenAI endpoint or keys after 5 minutes, please retrieve them manually from the Azure portal and update the .env file"
    Write-Host
}

$OpenAIKeys1 = if ($useEnvFile -and $envVars['OpenAIKey1']) { $envVars['OpenAIKey1'] } else { $OpenAIKeys.key1 }
$OpenAIKeys2 = $OpenAIKeys.key2

# Write the .env file
if ($updateEnvFile) {
    $envVars = @{
        "randomIdentifier" = if ($randomIdentifier) { "`"$randomIdentifier`"" } else { "" }
        "location" = if ($location) { "`"$location`"" } else { "" }
        "subscriptionName" = if ($subscriptionName) { "`"$subscriptionName`"" } else { "" }
        "resourceGroup" = if ($resourceGroup) { "`"$resourceGroup`"" } else { "" }
        "cosmosCluster" = if ($cosmosCluster) { "`"$cosmosCluster`"" } else { "" }
        "cosmosDbEndpoint" = if ($cosmosDbEndpoint) { "`"$cosmosDbEndpoint`"" } else { "" }
        "cosmosClusterAdmin" = if ($cosmosClusterAdmin) { "`"$cosmosClusterAdmin`"" } else { "" }
        "cosmosClusterPassword" = if ($cosmosClusterPassword) { "`"$cosmosClusterPassword`"" } else { "" }
        "cosmosDatabase" = if ($cosmosDatabase) { "`"$cosmosDatabase`"" } else { "cosmicworks" }
        "OpenAIAccount" = if ($OpenAIAccount) { "`"$OpenAIAccount`"" } else { "" }
        "OpenAIEndpoint" = if ($OpenAIEndpoint) { "`"$OpenAIEndpoint`"" } else { "" }
        "OpenAIKey1" = if ($OpenAIKey1) { "`"$OpenAIKey1`"" } else { "" }
        "OpenAIVersion" = if ($OpenAIVersion) { "`"$OpenAIVersion`"" } else { "2023-05-15" }
        "OpenAIDeploymentModelVersion" = if ($OpenAIDeploymentModelVersion) { "`"$OpenAIDeploymentModelVersion`"" } else { "" }
        "OpenAICompletionDeploymentModelVersion" = if ($OpenAICompletionDeploymentModelVersion) { "`"$OpenAICompletionDeploymentModelVersion`"" } else { "" }
        "OpenAIDeploymentModel" = if ($OpenAIDeploymentModel) { "`"$OpenAIDeploymentModel`"" } else { "" }
        "OpenAICompletionDeploymentModel" = if ($OpenAICompletionDeploymentModel) { "`"$OpenAICompletionDeploymentModel`"" } else { "" }
        "OpenAIDeploymentName" = if ($OpenAIDeploymentName) { "`"$OpenAIDeploymentName`"" } else { "" }
        "OpenAICompletionDeploymentName" = if ($OpenAICompletionDeploymentName) { "`"$OpenAICompletionDeploymentName`"" } else { "" }
    }

    $envVars.GetEnumerator() | ForEach-Object {
        "$($_.Key)=$($_.Value)"
    } | Out-File -FilePath $envFilePath -Encoding utf8
}

# Output the resources
Write-Host
Write-Host "*************** Resources ***************"
Write-Host
write-host "Random Identifier: $randomIdentifier"
write-host 
Write-Host "Subscription name: $subscriptionName"
Write-Host "Resource group: $resourceGroup"
Write-Host "Location: $location"
Write-Host
Write-Host "Cosmos Cluster Name: $cosmosCluster"
Write-Host "Cosmos Cluster Admin: $cosmosClusterAdmin"
Write-Host "Cosmos Cluster Admin Password: $cosmosClusterPassword"
Write-Host "Cosmos DB Endpoint: $cosmosDbEndpoint"
Write-Host "Cosmos Database: $cosmosDatabase"
Write-Host
Write-Host "OpenAI account: $OpenAIAccount"
Write-Host "OpenAI Endpoint: $OpenAIEndpoint"
Write-Host "OpenAI Key1: $OpenAIKeys1"
Write-Host "OpenAI Key2: $OpenAIKeys2"
write-host 
Write-Host "OpenAI deployment name: $OpenAIDeploymentName"
write-host "OpenAI deployment model: $OpenAIDeploymentModel"
write-host "OpenAI deployment model version: $OpenAIDeploymentModelVersion"
write-host
Write-Host "OpenAI completion name: $OpenAICompletionDeploymentName"
write-host "OpenAI completion model: $OpenAICompletionDeploymentModel"
write-host "OpenAI completion model version: $OpenAICompletionDeploymentModelVersion"
Write-Host
Write-Host "*************** Resources ***************"