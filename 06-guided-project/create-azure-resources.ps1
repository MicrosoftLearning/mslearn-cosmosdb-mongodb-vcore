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
    [bool]$skipCreatingAzureOpenAIAccount = $false, # Skip creating the Azure OpenAI account
    [bool]$skipCreatingAzureOpenAIDeployment = $false, # Skip creating the Azure OpenAI deployment
    [bool]$skipCreatingAzureOpenAICompletionDeployment = $false, # Skip creating the Azure OpenAI completion deployment

    [string]$cosmosCluster, # The name of the Cosmos DB cluster
    [string]$cosmosClusterLocation, # The location for the Cosmos DB cluster
    [string]$cosmosClusterAdmin, # The admin username for the Cosmos DB cluster
    [String]$cosmosClusterPassword, # The admin password for the Cosmos DB cluster
    [string]$cosmosdbDatabase, # The name of the Cosmos DB database

    [string]$OpenAIAccount, # The name of the Azure OpenAI account
    [string]$OpenAIAccountLocation, # The location for the Azure OpenAI account
    [string]$OpenAIAccountSKU, # The SKU for the Azure OpenAI account

    [string]$OpenAIDeploymentName, # The name of the Azure OpenAI deployment
    [string]$OpenAIDeploymentModel, # The model for the Azure OpenAI deployment
    [string]$OpenAIDeploymentModelVersion, # The model version for the Azure OpenAI deployment
    [string]$OpenAIDeploymentSKU, # The SKU for the Azure OpenAI deployment
    [Int32]$OpenAIDeploymentSKUCapacity, # The SKU capacity for the Azure OpenAI deployment

    [string]$OpenAICompletionDeploymentName, # The name of the Azure OpenAI completion deployment
    [string]$OpenAICompletionDeploymentModel, # The model for the Azure OpenAI completion deployment
    [string]$OpenAICompletionDeploymentModelVersion, # The model version for the Azure OpenAI completion deployment
    [string]$OpenAICompletionDeploymentSKU, # The SKU for the Azure OpenAI completion deployment
    [Int32]$OpenAICompletionDeploymentSKUCapacity # The SKU capacity for the Azure OpenAI completion deployment
)

# Determine the .env file path
$envFilePath = "./node.js/.env"

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
    if ($envVars['skipCreatingAzureOpenAIAccount'] -eq 'true') { $skipCreatingAzureOpenAIAccount = $true }
    if ($envVars['skipCreatingAzureOpenAIDeployment'] -eq 'true') { $skipCreatingAzureOpenAIDeployment = $true }
    if ($envVars['skipCreatingAzureOpenAICompletionDeployment'] -eq 'true') { $skipCreatingAzureOpenAICompletionDeployment = $true }
} 

# Error variable to track if there are any creation errors
$changeSubscriptionError = $null
$CreatingResourceGroupError = $null
$CreatingCosmosDBClusterError = $null
$CreatingAzureOpenAIAccountError = $null
$CreatingAzureOpenAIDeploymentError = $null
$CreatingAzureOpenAICompletionDeploymentError = $null

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
$cosmosdbDatabase = if ($cosmosdbDatabase) {$cosmosdbDatabase} elseif ($useEnvFile -and $envVars['cosmosdbDatabase']) { $envVars['cosmosdbDatabase'] } else { "cosmicworks" }

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

# Create an Azure OpenAI resource
$cognitiveServicesKind = if ($useEnvFile -and $envVars['cognitiveServicesKind']) { $envVars['cognitiveServicesKind'] } else { "OpenAI" }
$OpenAIAccount = if ($OpenAIAccount) {$OpenAIAccount} elseif ($useEnvFile -and $envVars['OpenAIAccount']) { $envVars['OpenAIAccount'] } else { "msdocs-account-openai-$randomIdentifier" } #needs to be lower case
$OpenAIAccountLocation = if ($OpenAIAccountLocation) {$OpenAIAccountLocation} elseif ($useEnvFile -and $envVars['OpenAIAccountLocation']) { $envVars['OpenAIAccountLocation'] } else { $location } 
$OpenAIAccountSKU = if ($OpenAIAccountSKU) {$OpenAIAccountSKU} elseif ($useEnvFile -and $envVars['OpenAIAccountSKU']) { $envVars['OpenAIAccountSKU'] } else { "s0" }

# Create an Azure OpenAI account
if (! $skipCreatingAzureOpenAIAccount) {
    Write-Host
    Write-Host "Creating OpenAI account $OpenAIAccount in $OpenAIAccountLocation..."
    Write-Host

    try {
        $output = az cognitiveservices account create --name $OpenAIAccount --resource-group $resourceGroup --location $OpenAIAccountLocation --kind $cognitiveServicesKind --sku $OpenAIAccountSKU --custom-domain $OpenAIAccount --only-show-errors
        if ($LASTEXITCODE -ne 0) {
            throw $output
        }
    }
    catch {
        $CreatingAzureOpenAIAccountError = $_.Exception.Message
        Write-Host "Error creating the OpenAI account $OpenAIAccount - $CreatingAzureOpenAIAccountError"
    }
}

$OpenAIDeploymentName = if ($OpenAIDeploymentName) {$OpenAIDeploymentName} elseif ($useEnvFile -and $envVars['OpenAIDeploymentName']) { $envVars['OpenAIDeploymentName'] } else { "msdocs-account-openai-deployment-$randomIdentifier" }
$OpenAIDeploymentModel = if ($OpenAIDeploymentModel) {$OpenAIDeploymentModel} elseif ($useEnvFile -and $envVars['OpenAIDeploymentModel']) { $envVars['OpenAIDeploymentModel'] } else { "text-embedding-ada-002" }
$OpenAIDeploymentModelFormat = if ($useEnvFile -and $envVars['OpenAIDeploymentModelFormat']) { $envVars['OpenAIDeploymentModelFormat'] } else { "OpenAI" }
$OpenAIDeploymentModelVersion = if ($OpenAIDeploymentModelVersion) {$OpenAIDeploymentModelVersion} elseif ($useEnvFile -and $envVars['OpenAIDeploymentModelVersion']) { $envVars['OpenAIDeploymentModelVersion'] } else { "2" }
$OpenAIDeploymentSKU = if ($OpenAIDeploymentSKU) {$OpenAIDeploymentSKU} elseif ($useEnvFile -and $envVars['OpenAIDeploymentSKU']) { $envVars['OpenAIDeploymentSKU'] } else { "Standard" }
$OpenAIDeploymentSKUCapacity = if ($OpenAIDeploymentSKUCapacity) {$OpenAIDeploymentSKUCapacity} elseif ($useEnvFile -and $envVars['OpenAIDeploymentSKUCapacity']) { $envVars['OpenAIDeploymentSKUCapacity'] } else { 100 }

# Create a new deployment for the Azure OpenAI account
if (! $skipCreatingAzureOpenAIDeployment) {
    Write-Host
    Write-Host "Creating OpenAI deployment $OpenAIDeploymentName in $OpenAIAccountLocation..."
    Write-Host

    try {
        $output = az cognitiveservices account deployment create --name $OpenAIAccount --resource-group $resourceGroup --deployment-name $OpenAIDeploymentName --model-name $OpenAIDeploymentModel --model-version $OpenAIDeploymentModelVersion --model-format $OpenAIDeploymentModelFormat --sku-capacity $OpenAIDeploymentSKUCapacity --sku-name $OpenAIDeploymentSKU --only-show-errors 
        if ($LASTEXITCODE -ne 0) {
            throw $output
        }
    }
    catch {
        $CreatingAzureOpenAIDeploymentError = $_.Exception.Message
        Write-Host "Error creating the OpenAI deployment $OpenAIDeploymentName - $CreatingAzureOpenAIDeploymentError"
    }
}

$OpenAICompletionDeploymentName = if ($OpenAICompletionDeploymentName) {$OpenAICompletionDeploymentName} elseif ($useEnvFile -and $envVars['OpenAICompletionDeploymentName']) { $envVars['OpenAICompletionDeploymentName'] } else { "msdocs-account-openai-completion-$randomIdentifier" }
$OpenAICompletionDeploymentModel = if ($OpenAICompletionDeploymentModel) {$OpenAICompletionDeploymentModel} elseif ($useEnvFile -and $envVars['OpenAICompletionDeploymentModel']) { $envVars['OpenAICompletionDeploymentModel'] } else { "gpt-35-turbo" }
$OpenAICompletionDeploymentModelFormat = if ($useEnvFile -and $envVars['OpenAICompletionDeploymentModelFormat']) { $envVars['OpenAICompletionDeploymentModelFormat'] } else { "OpenAI" }
$OpenAICompletionDeploymentModelVersion = if ($OpenAICompletionDeploymentModelVersion) {$OpenAICompletionDeploymentModelVersion} elseif ($useEnvFile -and $envVars['OpenAICompletionDeploymentModelVersion']) { $envVars['OpenAICompletionDeploymentModelVersion'] } else { "0301" }
$OpenAICompletionDeploymentSKU = if ($OpenAICompletionDeploymentSKU) {$OpenAICompletionDeploymentSKU} elseif ($useEnvFile -and $envVars['OpenAICompletionDeploymentSKU']) { $envVars['OpenAICompletionDeploymentSKU'] } else { "Standard" }
$OpenAICompletionDeploymentSKUCapacity = if ($OpenAICompletionDeploymentSKUCapacity) {$OpenAICompletionDeploymentSKUCapacity} elseif ($useEnvFile -and $envVars['OpenAICompletionDeploymentSKUCapacity']) { $envVars['OpenAICompletionDeploymentSKUCapacity'] } else { 100 }

# Create a new completion deployment for the Azure OpenAI account
if (! $skipCreatingAzureOpenAICompletionDeployment) {
    Write-Host
    Write-Host "Creating OpenAI completetion deployment $OpenAICompletionDeploymentName in $OpenAIAccountLocation..."
    Write-Host

    try {
        $output = az cognitiveservices account deployment create --name $OpenAIAccount --resource-group $resourceGroup --deployment-name $OpenAICompletionDeploymentName --model-name $OpenAICompletionDeploymentModel --model-version $OpenAICompletionDeploymentModelVersion --model-format $OpenAICompletionDeploymentModelFormat --sku-capacity $OpenAICompletionDeploymentSKUCapacity --sku-name $OpenAICompletionDeploymentSKU --only-show-errors 
        if ($LASTEXITCODE -ne 0) {
            throw $output
        }
    }
    catch {
        $CreatingAzureOpenAICompletionDeploymentError = $_.Exception.Message
        Write-Host "Error creating the OpenAI completion deployment $OpenAICompletionDeploymentName - $CreatingAzureOpenAICompletionDeploymentError"
    }
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

$key1, $key2 = $OpenAIkeys -split "`t"

$OpenAIKeys1 = if ($useEnvFile -and $envVars['OpenAIKey1']) { $envVars['OpenAIKey1'] } else { $key1 }
$OpenAIKeys2 = $key2

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
        "cosmosdbDatabase" = if ($cosmosdbDatabase) { "`"$cosmosdbDatabase`"" } else { "`"cosmicworks`"" }

        "skipCreatingAzureOpenAIAccount" = if ($skipCreatingAzureOpenAIAccount) { "true" } else { "" }
        "cognitiveServicesKind" = if ($cognitiveServicesKind) { "`"$cognitiveServicesKind`"" } else { "OpenAI" }
        "OpenAIAccount" = if ($OpenAIAccount) { "`"$OpenAIAccount`"" } else { "" }
        "OpenAIAccountLocation" = if ($OpenAIAccountLocation) { "`"$OpenAIAccountLocation`"" } else { "" }
        "OpenAIAccountSKU" = if ($OpenAIAccountSKU) { "`"$OpenAIAccountSKU`"" } else { "`"s0`"" }
        "OpenAIEndpoint" = if ($OpenAIEndpoint) { "`"$OpenAIEndpoint`"" } else { "" }
        "OpenAIKey1" = if ($OpenAIKeys1) { "`"$OpenAIKeys1`"" } else { "" }
        "OpenAIVersion" = if ($OpenAIVersion) { "`"$OpenAIVersion`"" } else { "`"2023-05-15`"" }

        "skipCreatingAzureOpenAIDeployment" = if ($skipCreatingAzureOpenAIDeployment) { "true" } else { "" }
        "OpenAIDeploymentName" = if ($OpenAIDeploymentName) { "`"$OpenAIDeploymentName`"" } else { "" }
        "OpenAIDeploymentModel" = if ($OpenAIDeploymentModel) { "`"$OpenAIDeploymentModel`"" } else { "" }
        "OpenAIDeploymentModelFormat" = if ($OpenAIDeploymentModelFormat) { "`"$OpenAIDeploymentModelFormat`"" } else { "OpenAI" }
        "OpenAIDeploymentModelVersion" = if ($OpenAIDeploymentModelVersion) { "`"$OpenAIDeploymentModelVersion`"" } else { "" }
        "OpenAIDeploymentSKU" = if ($OpenAIDeploymentSKU) { "`"$OpenAIDeploymentSKU`"" } else { "`"Standard`"" }
        "OpenAIDeploymentSKUCapacity" = if ($OpenAIDeploymentSKUCapacity) { "$OpenAIDeploymentSKUCapacity" } else { "100" }

        "skipCreatingAzureOpenAICompletionDeployment" = if ($skipCreatingAzureOpenAICompletionDeployment) { "true" } else { "" }
        "OpenAICompletionDeploymentName" = if ($OpenAICompletionDeploymentName) { "`"$OpenAICompletionDeploymentName`"" } else { "" }
        "OpenAICompletionDeploymentModel" = if ($OpenAICompletionDeploymentModel) { "`"$OpenAICompletionDeploymentModel`"" } else { "" }
        "OpenAICompletionDeploymentModelFormat" = if ($OpenAICompletionDeploymentModelFormat) { "`"$OpenAICompletionDeploymentModelFormat`"" } else { "OpenAI" }
        "OpenAICompletionDeploymentModelVersion" = if ($OpenAICompletionDeploymentModelVersion) { "`"$OpenAICompletionDeploymentModelVersion`"" } else { "" }
        "OpenAICompletionDeploymentSKU" = if ($OpenAICompletionDeploymentSKU) { "`"$OpenAICompletionDeploymentSKU`"" } else { "`"Standard`"" }
        "OpenAICompletionDeploymentSKUCapacity" = if ($OpenAICompletionDeploymentSKUCapacity) { "$OpenAICompletionDeploymentSKUCapacity" } else { "100" }
    }

    # We group the environment variables to improve readability and organization.
    # Each group represents a different service or component of your application.
    # This makes it easier to manage and update the variables related to each component.

    $group1 = $envVars.Keys[0..5]  # Variables related to Azure subscription and resource group
    $group2 = $envVars.Keys[6..13]  # Variables related to Cosmos DB
    $group3 = $envVars.Keys[14..21]  # Variables related to OpenAI account and endpoint
    $group4 = $envVars.Keys[22..28]  # Variables related to OpenAI deployment
    $group5 = $envVars.Keys[29..35]  # Variables related to OpenAI completion deployment

    $groups = @($group1, $group2, $group3, $group4, $group5)

    $output = $groups | ForEach-Object {
        $group = $_
        $group | ForEach-Object {
            "$($_)=$($envVars[$_])"
        }
        ""  # Add a blank line for the component group separation
    }
    
    $output | Out-File -FilePath $envFilePath -Encoding utf8}

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
Write-Host "Cosmos Database: $cosmosdbDatabase"
Write-Host
Write-Host "OpenAI account creation status: " -NoNewline
if ($skipCreatingAzureOpenAIAccount) { Write-Host "Skipped" -ForegroundColor Yellow } elseif (  $null -ne $CreatingAzureOpenAIAccountError ){ Write-Host "Failed" -ForegroundColor Red } else { Write-Host "Success" -ForegroundColor Green }
if ($null -ne $CreatingAzureOpenAIAccountError) { Write-Host "OpenAI account creation error: "  -NoNewline  } if ($null -ne $CreatingAzureOpenAIAccountError) { Write-Host $CreatingAzureOpenAIAccountError -ForegroundColor Red}
Write-Host "Cognitive Services Kind: $cognitiveServicesKind"
Write-Host "OpenAI account: $OpenAIAccount"
Write-Host "OpenAI account Location: $OpenAIAccountLocation"
Write-Host "OpenAI account SKU: $OpenAIAccountSKU"
Write-Host "OpenAI Endpoint: $OpenAIEndpoint"
Write-Host "OpenAI Key1: $OpenAIKeys1"
Write-Host "OpenAI Key2: $OpenAIKeys2"
write-host
Write-Host "Open AI deployment creation status: " -NoNewline
if ($skipCreatingAzureOpenAIDeployment) { Write-Host "Skipped" -ForegroundColor Yellow } elseif (  $null -ne $CreatingAzureOpenAIDeploymentError ){ Write-Host "Failed" -ForegroundColor Red } else { Write-Host "Success" -ForegroundColor Green }
if ($null -ne $CreatingAzureOpenAIDeploymentError) { Write-Host "OpenAI deployment creation error - $CreatingAzureOpenAIDeploymentError" }
Write-Host "OpenAI deployment name: $OpenAIDeploymentName"
write-host "OpenAI deployment model: $OpenAIDeploymentModel"
Write-host "OpenAI deployment model format: $OpenAIDeploymentModelFormat"
write-host "OpenAI deployment model version: $OpenAIDeploymentModelVersion"
Write-Host "OpenAI deployment SKU: $OpenAIDeploymentSKU"
Write-Host "OpenAI deployment SKU Capacity: $OpenAIDeploymentSKUCapacity"
write-host
Write-Host "Open AI completion deployment creation status: " -NoNewline
if ($skipCreatingAzureOpenAICompletionDeployment) { Write-Host "Skipped" -ForegroundColor Yellow } elseif (  $null -ne $CreatingAzureOpenAICompletionDeploymentError ){ Write-Host "Failed" -ForegroundColor Red } else { Write-Host "Success" -ForegroundColor Green }
if ($null -ne $CreatingAzureOpenAICompletionDeploymentError) { Write-Host "OpenAI completion deployment creation error - $CreatingAzureOpenAICompletionDeploymentError" }
Write-Host "OpenAI completion deployment name: $OpenAICompletionDeploymentName"
write-host "OpenAI completion deployment model: $OpenAICompletionDeploymentModel"
write-host "OpenAI completion deployment model format: $OpenAICompletionDeploymentModelFormat"
write-host "OpenAI completion deployment model version: $OpenAICompletionDeploymentModelVersion"
Write-Host "OpenAI completion deployment SKU: $OpenAICompletionDeploymentSKU"
Write-Host "OpenAI completion deployment SKU Capacity: $OpenAICompletionDeploymentSKUCapacity"
Write-Host
Write-Host "*************** Resources ***************"