# .env File Configuration Guide

This guide outlines the structure and purpose of the **.env** file used for configuring your lab environment and applications. The **.env** file stores environment variables that are crucial for customizing the lab application's behavior, particularly for resource deployment and API interactions.

## Structure of the .env File

The **.env** file contains key-value pairs, each defining a specific configuration aspect. The following table lists the variables included in the **.env** file and their intended use:

| Variable Name | Description | Example Value |
|---------------|-------------|---------------|
| **randomIdentifier** | A unique identifier for distinguishing resources. | **504305484** |
| **location** | The deployment location for cloud resources. | **eastus** |
| **subscriptionName** | The name of the cloud subscription under which resources are deployed. | **YourSubscriptionName** |
| **resourceGroup** | The name of the resource group containing all related resources. | **example-rg** |
| **cosmosCluster** | The name of the Cosmos DB cluster. | **example-cosmos-cluster** |
| **cosmosClusterLocation** | The location for the Cosmos DB cluster. | **eastus** |
| **cosmosDbEndpoint** | The endpoint URL for the Cosmos DB cluster. | **https://example.documents.azure.com:443/** |
| **cosmosClusterAdmin** | The admin username for the Cosmos DB cluster. | **adminUser** |
| **cosmosClusterPassword** | The password for the Cosmos DB cluster. | **SecurePassword!** |
| **cosmosdbDatabase** | The name of the Cosmos DB database. Defaults to **cosmicworks**. | **cosmicworks** |
| **OpenAIAccount** | The name of the Azure OpenAI account. | **example-openai-account** |
| **OpenAIAccountLocation** | The location for the Azure OpenAI account. | **eastus** |
| **OpenAIAccountSKU** | The SKU for the Azure OpenAI account. Defaults to **"s0"** | **"s0"** |
| **OpenAIEndpoint** | The endpoint URL for the Azure OpenAI account. | **https://example.openai.azure.com/** |
| **OpenAIKey1** | The first key for accessing the Azure OpenAI service. | **YourKeyHere** |
| **OpenAIVersion** | The version of the Azure OpenAI API to use. Defaults to **"2023-05-15"**. | **"2023-05-15"** |
| **OpenAIDeploymentModelVersion** | The model version for the Azure OpenAI deployment. | **2** |
| **OpenAICompletionDeploymentModelVersion** | The model version for the Azure OpenAI completion deployment. | **0301** |
| **OpenAIDeploymentModel** | The model name for the Azure OpenAI deployment. | **text-embedding-ada-002** |
| **OpenAICompletionDeploymentModel** | The model name for the Azure OpenAI completion deployment. | **gpt-3.5-turbo** |
| **OpenAIDeploymentName** | The name of the Azure OpenAI deployment. | **example-deployment** |
| **OpenAICompletionDeploymentName** | The name of the Azure OpenAI completion deployment. | **example-completion-deployment** |
| **OpenAIDeploymentSKU** | The SKU for the Azure OpenAI deployment. Defaults to **"Standard"**. | **"Standard"** |
| **OpenAIDeploymentSKUCapacity** | The SKU capacity for the Azure OpenAI deployment. Defaults to **100** | **100** |
| **OpenAICompletionDeploymentSKU** | The SKU for the Azure OpenAI completion deployment. Defaults to **"Standard"**. | **"Standard"** |
| **OpenAICompletionDeploymentSKUCapacity** | The SKU capacity for the Azure OpenAI completion deployment. Defaults to **100** | **100** |

## How to Use

1. This file is used for the *create-azure-resources.ps1* PowerShell script, and the Lab's Python and Node.js applications. The values in the .env file are used to configure the applications and scripts to interact with the Azure resources.
lab.
1. If you're using the .env file to populate the *create-azure-resources.ps1* PowerShell script variables, you need to set the **-useEnvFile** parameter when running the script. By default the *create-azure-resources.ps1* PowerShell script also populates the **.env** file with those resources it creates.
1. Fill in the variables with your specific values, making sure all values are inside double quotes. Leave values blank for those value pairs that a lab doesn't need. For example, if you aren't using the Azure OpenAI service for a lab, you can leave the **OpenAIAccount**, **OpenAIKey1**, and all other OpenAI variables blank.

This guide should help you utilize your **.env** file to configure the lab's resource deployments and settings.
