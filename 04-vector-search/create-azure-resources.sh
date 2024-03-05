az login

# :::NOTE:::: If your subscription is different from the default, uncomment the next two lines and 
# :::NOTE:::: replace "your-subscription-name" with your subscription name. To list subscriptions, use the following command: az account list --output table.
#subscriptionName="your-subscription-name"
#az account set --subscription $subscriptionName

# Variable block
let "randomIdentifier=$RANDOM*$RANDOM"

# :::NOTE:::: If you want to use a different location, replace "East US" with the location of your choice.
# :::NOTE:::: For a list of available locations, use the following command: az account list-locations --output table
location="eastus"

# :::NOTE:::: If you are using a predefined resource group in your subscription, replace "msdocs-cosmosdb-rg-$randomIdentifier"
# :::NOTE:::: with the name of the resource group (e.g., resourceGroup="myResourceGroup").
resourceGroup="msdocs-cosmosdb-rg-$randomIdentifier"

# Create a resource group
# :::NOTE:::: Comment the following two lines if you are using an existing resource group.
## :::NOTE:::: DO NOT USE A PRODUCTION RESOURCE GROUP.
echo "Creating $resourceGroup in $location..."
az group create --name $resourceGroup --location "$location" --tags $tag



# Create MongoDB resources
# Variable block
tag="create-mongodb-cosmosdb"
cosmosCluster="msdocs-account-cosmos-cluster-$randomIdentifier" #needs to be lower case
cosmosClusterAdmin="clusteradmin$randomIdentifier" 
cosmosClusterPassword=$(< /dev/urandom tr -dc '_A-Z-a-z-0-9!#$%^&*-+=`|(){}[];<>,.?/' | head -c 16)

# Create a Cosmos DB for MongoDB vCore cluster
# This command may take a few minutes to run.
# :::NOTE:::: DO NOT USE A PRODUCTION CLUSTER.
echo "Creating $cosmosCluster cluster, this could take 10+ minutes to create..."
deploymentParameters='{ \"clusterName\": { \"value\": \"'"$cosmosCluster"'\" }, \"adminUsername\": { \"value\": \"'"$cosmosClusterAdmin"'\" }, \"adminPassword\": { \"value\": \"'"$cosmosClusterPassword"'\" }, \"location\": { \"value\": \"'"$location"'\" } }'
az deployment group create --resource-group $resourceGroup --template-file 'create-mongodb-vcore-cluster.bicep' --parameters clusterName=$cosmosCluster adminUsername=$cosmosClusterAdmin adminPassword=$cosmosClusterPassword location=$location



# Create an Azure OpenAI resource

# Variable block
## :::NOTE:::: If you already have an Azure OpenAI account, replace "msdocs-account-openai-$randomIdentifier" with the name of your account.
## :::NOTE:::: DO NOT USE A PRODUCTION ACCOUNT.
OpenAIAccount="msdocs-account-openai2-$randomIdentifier" #needs to be lower case

# Create an Azure OpenAI account
echo "Creating OpenAI account $OpenAIAccount in $location..."
az cognitiveservices account create --name $OpenAIAccount --resource-group $resourceGroup --location $location --kind OpenAI --sku s0


# Return all resource names
subscriptionName=Az account show --query name -o tsv
echo
echo "*************** Resources ***************"
echo
echo "Subscription name: $subscriptionName"
echo "Resource group: $resourceGroup"
echo "Location: $location"
echo
echo "Cosmos Cluster Name: $cosmosCluster"
echo "Cosmos Cluster Admin: $cosmosClusterAdmin"
echo "Cosmos Cluster Admin Password: $cosmosClusterPassword"
echo
echo "OpenAI account: $OpenAIAccount"
echo
echo "*************** Resources ***************"


