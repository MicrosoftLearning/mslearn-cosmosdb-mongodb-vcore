---
lab:
    title: 'PowerShell script usage reference'
    module: 'Reference Guide'
---

This document provides a comprehensive reference for the ***create-azure-resources.ps1*** PowerShell script designed to automate the lab deployment and configuration of the Azure resources, specifically for the Azure Cosmos DB and Azure OpenAI services.

## Parameters reference

The script accepts several parameters to customize the deployment process. The following table lists details each parameter, including their default values when not explicitly provided (note that each lab's resource PowerShell creation script will have a sub-set of these variables):

### Environment file, Azure subscription and resource group

| Parameter Name | Data Type | Mandatory | Default Value | Description |
|----------------|-----------|-----------|---------------|-------------|
| **useEnvFile** | bool | No | *true* | If true, determines whether to use a **.env** file for configuration values. |
| **updateEnvFile** | bool | No | *true* | If true, updates the **.env** file with new or changed values. |
| **randomIdentifier** | Int32 | No | Get-Random | A random identifier to make the resource names unique. |
| **location** | string | No | "eastus" | The location for the deployment. Defaults to "eastus" if not specified. |
| **subscriptionName** | string | No | Output of **(az account show --query name -o tsv)** | The name of the Azure subscription for the deployment. Defaults to the current Azure subscription name. |
| **resourceGroup** | string | No | "msdocs-cosmosdb-rg-$randomIdentifier" | The name of the resource group. Generated using a random identifier if not specified. |

### Skip resource creation

| Parameter Name | Data Type | Mandatory | Default Value | Description |
|----------------|-----------|-----------|---------------|-------------|
| **changeSubscription** | bool | No | *false* | If true, allows changing the Azure subscription. |
| **skipCreatingResourceGroup** | bool | No | *false* | If true, skips the creation of a new resource group. |
| **skipCreatingCosmosDBCluster** | bool | No | *false* | If true, skips the creation of the Cosmos DB cluster. |
| **skipCreatingCosmosDBPublicIPFirewallRule** | bool | No | *false* | If true, skips creating a public IP firewall rule for Cosmos DB. |
| **skipCreatingAzureOpenAIAccount** | bool | No | *false* | If true, skips creating an Azure OpenAI account. |
| **skipCreatingAzureOpenAIDeployment** | bool | No | *false* | If true, skips creating an Azure OpenAI deployment. |
| **skipCreatingAzureOpenAICompletionDeployment** | bool | No | *false* | If true, skips creating an Azure OpenAI completion deployment. |
| **skipCreatingStorageAccount** | bool | No | *false* | If true, skips creating a storage account. |
| **skipCreatingLogAnalyticsWorkspace** | bool | No | *false* | If true, skips creating a Log Analytics workspace. |

### Azure Cosmos DB account

| Parameter Name | Data Type | Mandatory | Default Value | Description |
|----------------|-----------|-----------|---------------|-------------|
| **cosmosCluster** | string | No | "msdocs-account-cosmos-cluster-$randomIdentifier" | The name of the Cosmos DB cluster. Generated using a random identifier if not specified. |
| **cosmosClusterLocation** | string | No | **location** | The location for the Cosmos DB cluster. |
| **cosmosClusterAdmin** | string | No | "clusteradmin$randomIdentifier" | The admin username for the Cosmos DB cluster. Generated using a random identifier if not specified. |
| **cosmosClusterPassword** | SecureString | No | Randomly generated 16-character password | The password for the Cosmos DB cluster. Generated if not specified. |
| **cosmosDatabase** | string | No | "cosmicworks" | The name of the Cosmos DB database. Generated using a random identifier if not specified. |

### Azure OpenAI account

| Parameter Name | Data Type | Mandatory | Default Value | Description |
|----------------|-----------|-----------|---------------|-------------|
| **OpenAIAccount** | string | No | "msdocs-account-openai-$randomIdentifier" | The name of the Azure OpenAI account. Generated using a random identifier if not specified. |
| **OpenAIAccountLocation** | string | No | **location** | The location for the Azure OpenAI account. |
| **OpenAIAccountSKU** | string | No | "s0" | The SKU for the Azure OpenAI account. |

### Azure OpenAI deployment

| Parameter Name | Data Type | Mandatory | Default Value | Description |
|----------------|-----------|-----------|---------------|-------------|
| **OpenAIDeploymentName** | string | No | "msdocs-account-openai-deployment-$randomIdentifier" | The name of the Azure OpenAI deployment. Generated using a random identifier if not specified. |
| **OpenAIDeploymentModel** | string | No | "text-embedding-ada-002" | The model name for the Azure OpenAI deployment. Defaults to "text-embedding-ada-002" if not specified. |
| **OpenAIDeploymentModelVersion** | string | No | "2" | The model version for the Azure OpenAI deployment. Defaults to "2" if not specified. |
| **OpenAIDeploymentSKU** | String | No | "Standard" | The SKU for the Azure OpenAI deployment. |
| **OpenAIDeploymentSKUCapacity** | Int32 | No | 100 | The SKU capacity for the Azure OpenAI deployment. |

### Azure OpenAI completion deployment

| Parameter Name | Data Type | Mandatory | Default Value | Description |
|----------------|-----------|-----------|---------------|-------------|
| **OpenAICompletionDeploymentName** | string | No | "msdocs-account-openai-completion-$randomIdentifier" | The name of the Azure OpenAI completion deployment. Generated using a random identifier if not specified. |
| **OpenAICompletionDeploymentModel** | string | No | "gpt-3.5-turbo" | The model name for the Azure OpenAI completion deployment. Defaults to "gpt-3.5-turbo" if not specified. |
| **OpenAICompletionDeploymentModelVersion** | string | No | "0301" | The model version for the Azure OpenAI completion deployment. Defaults to "0301" if not specified. |
| **OpenAICompletionDeploymentSKU** | String | No | "Standard" | The SKU for the Azure OpenAI completion deployment. |
| **OpenAICompletionDeploymentSKUCapacity** | Int32 | No | 100 | The SKU capacity for the Azure OpenAI completion deployment. |

### Azure storage account

| Parameter Name | Data Type | Mandatory | Default Value | Description |
|----------------|-----------|-----------|---------------|-------------|
| **storageAccountName** | string | No | "msdocsstorage$randomIdentifier" | The name of the storage account. Generated using a random identifier if not specified. |
| **storageAccountLocation** | string | No | **location** | The location for the storage account. |
| **storageAccountSKU** | string | No | "Standard_LRS" | The SKU for the storage account. |
| **storageAccountKind** | string | No | "StorageV2" | The kind of storage account. |

### Azure Log Analytics workspace

| Parameter Name | Data Type | Mandatory | Default Value | Description |
|----------------|-----------|-----------|---------------|-------------|
| **logAnalyticsWorkspaceName** | string | No | "msdocs-log-analytics-workspace-$randomIdentifier" | The name of the Log Analytics workspace. Generated using a random identifier if not specified. |
| **logAnalyticsWorkspaceLocation** | string | No | **location** | The location for the Log Analytics workspace. |

## Determinate variable value precedence

When determining the value to assign to each variable within the script, the following order of precedence is observed:

1. Explicit Parameters: The highest priority is given to values explicitly passed as parameters when the script is invoked. If a parameter is specified in the command, this value overrides any others. Boolean parameters are set to **$true** if specified.

1. .env File Variables: If an explicit parameter isn't provided for a particular setting, the script checks if the -useEnvFile flag is set to $true, and looks for the variable value in the .env file. It ignores the variable if it has an empty value. The .env file allows for easy management of settings without changing the script or the command invocation, assuming the .env file is correctly populated.

1. Default Values: Lastly, if an explicit parameter is provided isn't provided, or a suitable value is found in the .env file, the script uses its predefined default values for the variable. The default values ensure that the script has sensible, working defaults for all settings, facilitating its execution even with minimal input.

This structure ensures each variable within the script is assigned a value in a predictable manner. The variable-value pair allows for flexible yet controlled configuration based on the user's input, environment setup, and the script's internal logic.

## Script operations

When a parameter is added to the script execution, the parameter performs several key operations based on the parameter's function:

1. **Read and Parse the .env File**: If using an **.env** file, reads it and parses its content. By default, the script uses the **.env** file for configuration values, but this setting can be overridden by setting the *-useEnvFile* parameter to *False*.
1. **Conditional Resource Creation and Configuration**: Conditionally creates Azure resources and configures network rules.
    1. **Resource Group Creation**: Creates a new resource group. By default, a Resource Group is created, but this setting can be skipped by setting the *-skipCreatingResourceGroup* parameter to *True*.
    1. **Deployment and Configuration of Azure Cosmos DB resources**: Deploys v-Core-based Azure Cosmos DB for MongoDB resources. By default, a Cosmos DB cluster is created, but this setting can be skipped by setting the *-skipCreatingCosmosDBCluster* parameter to *True*.
    1. **Deployment and Configuration of Azure OpenAI Resources**: Deploys Azure OpenAI models and setups. By default, an Azure OpenAI account, deployment, and completion deployment are created, but these settings can be skipped by setting the respective parameters to *True*.
1. **Update the .env File**: Updates the **.env** file with the latest configurations. Updating the **.env** file is done by default unless the parameter *-updateEnvFile* is set to *False*.
1. **Output Resource Information**: Outputs detailed information about the created or configured resources.

## Usage Examples

### Basic Usage with Mandatory Parameters Only

******PowerShell
.\create-azure-resources.ps1.ps1
******

This example runs the script without any parameters. Since no parameters were provided, the script then uses the .env file variables or, if they're empty, all the parameters' default values. When no parameters were provided, this script creates all resources.

### Advanced Usage with Multiple Parameters

******PowerShell
.\create-azure-resources.ps1.ps1 -skipCreatingResourceGroup -skipCreatingCosmosDBCluster -OpenAIAccount "custom-openai-account" -location "westus2"
******

This example demonstrates the use of multiple parameters to customize the deployment process. It uses an **.env** file for configuration, skips creating a new resource group, skips creating a Cosmos DB cluster, sets the Azure OpenAI account name to "custom-openai-account", and sets the deployment location to "westus2".

## Wrapping Up

This guide covered the *create-azure-resources.ps1* PowerShell script for the lab's Azure resource deployment, giving you the details on parameters, usage, and value logic. Armed with this knowledge, you can now confidently deploy and configure Azure resources for the lab, tailoring the process to your specific needs and environment.
