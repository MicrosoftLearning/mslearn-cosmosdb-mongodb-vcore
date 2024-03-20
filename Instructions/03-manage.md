---
lab:
    title: 'Manage a v-Core-based Azure Cosmos DB for MongoDB account'
    module: 'Module 3 - Manage v-Core-based Azure Cosmos DB for MongoDB'
---

## Introduction

In this lab, you will learn how to manage, scale, and monitor a v-Core-based Azure Cosmos DB for MongoDB account. You will use monitoring tools to track operations and scale your account to handle increased or decreased traffic. You will also learn how to enable diagnostic settings to collect logs and metrics from your Cosmos DB account. You will then run a simulated workload to generate some data for your logs and metrics. Finally, you will review the logs and metrics that are being generated.

### Objectives

Scale the Azure Cosmos DB for MongoDB account to meet performance needs by adjusting cluster tier, storage capacity, and enabling high availability.
Monitor the Azure Cosmos DB account using diagnostic settings to collect and analyze logs and metrics.

### Build your own lab environment

If you need to build your own lab environment, you need the following components and resource access.

- **Visual Studio Code**: Ensure Visual Studio Code is installed on your machine.
- **Azure Subscription**: Have access to an Azure Subscription for creating necessary resources.

## Clone the Repository

- Open **Visual Studio Code**.
- Press **CTRL+SHIFT+P** to open the command palette.
- Run **Git: Clone** and clone the repository `https://github.com/MicrosoftLearning/mslearn-cosmosdb-mongodb-vcore.git`.
- Navigate to the cloned repository directory.
- Right-click on the **03-manage** folder and select **Open in integrated Terminal**.

## Create Azure Resources

You need access to the following Azure resources for this lab:

- v-Core-based Azure Cosmos DB for MongoDB account
- Azure storage account
- Log Analytics workspace

You can create these resources via the *Azure portal* or use the ***create-azure-resources.ps1*** PowerShell script with the ***.env** file. Don't use existing production resources for this lab or any lab.

### Use the .env file

*This file must either be populated manually, or by the create-azure-resources.ps1 script before you can run your application, since it contains the connection information to your Azure resources.*

This file is both used to retrieve and store the necessary environment variables for both the PowerShell script and the vector search application APIs. It's the easiest way to prepopulate your resource information. The file is used to store the environment variables for your Azure Cosmos DB and Azure OpenAI account.

If you already have an existing Resource Group or a v-Core-based Azure Cosmos DB for MongoDB account that you would like to use, just fill in those values in the .env file and set the skip create option for that resource to **true**. By default, the *create-azure-resources.ps1* script uses this file to retrieve the necessary environment variables. Note that the *create-azure-resources.ps1* script will populate the environment variables with default values if not specified in the .env file.

To learn more about the ***.env*** file and its parameters, review the [***.env*** file documentation](./00-env-file.md).

### Use the create-azure-resources.ps1 script

This script creates the necessary Azure resources for this lab. It gives you the flexibility to create some or all of the resources required for this lab. You can either run the script as is or modify it to suit your needs. The resources created by the script include:

- Resource Group
- v-Core-based Azure Cosmos DB for MongoDB account
- Azure storage account
- Log Analytics workspace

The script has a rich set of parameters to help you customize the resources to be created. It also uses an ***.env*** file to retrieve and store the necessary environment variables for both the PowerShell script and the vector search application APIs.

> [!NOTE]
> While these parameters can be passed directly to the script, *we recommend you use the ***.env*** file to prepopulate your resource information instead of adding the parameters when executing the script. This will make it easier for you to manage your environment variables.*

To learn more about the PowerShell script and its parameters, review the [***create-azure-resources.ps1*** documentation](./00-powershell-script.md).

> [!NOTE]
> Make sure the tenant, location and subscription you use allows for the creation of the necessary resources. Not all locations and subscriptions might allow or support the creation of all the required resources needed for this lab. If you encounter any issues, please reach out to your Azure Administrator.

To create the necessary Azure resources for this lab:

1. Run the following command in the integrated terminal.

    ```powershell
    az login
    ./create-azure-resources.ps1
    ```

1. Copy and save the environment variables returned by the script in case you need them later. You can verify the resources created in the Azure portal. 

1. Make sure that the **.env** file is populated with the resource information.

> [!NOTE]
> The v-Core-based Azure Cosmos DB for MongoDB account will need a firewall rule to allow access from your current public IP address.  If your Azure Cosmos DB account was generated by the *create-azure-resources.ps1* script, it should have created the firewall rule for you.  Check the existing firewall rules under the ***Networking*** *Setting* section of the *Azure Cosmos DB Account*.  If you are not sure what your current public IP address is, you can use the following command to find out:
> ```powershell
> Invoke-RestMethod -Uri 'http://ipinfo.io/ip' -Method Get
> ```

Once the resources are created and your **.env** file is populated with the resource information, you can proceed to the next step.

## Scale a v-Core-based Azure Cosmos DB for MongoDB account

As your application performance needs changes, you might need to scale your v-Core-based Azure Cosmos DB for MongoDB account to handle increased or decreased traffic. You can scale your account by changing the cluster tier (number of vCores and RAM), the storage capacity, and enabling high availability.  To do this, let's follow these steps:

1. log in to the [Azure portal](https://portal.azure.com).

1. Navigate to your v-Core-based Azure Cosmos DB for MongoDB account.

1. In the left-hand menu, select **Scale** under the and *Settings* section.

1. In the *Scale* pane, you can change the cluster tier, storage capacity, and enable high availability.  

    1. Let's try changing the cluster tier to a lower tier. Select the **Cluster tier** pulldown, and select the **M30 tier, 2 vCores 8 GiB RAM**. If you were already using the M30 tier, you can try selecting the **M40 tier, 4 vCore 16 GiB RAM**. Notice how the cost changes.

    1. Let's leave the storage capacity alone, but you can select the pulldown to review the different storage sizes available for that cluster tier.

    1. Let's enable **High availability** and notice how the cost doubles. Go ahead and disable it again.

1. Once you have made your changes, select **Save** to apply the changes.

This will take a few minutes to complete, but go ahead and continue to the next section of the lab while these changes are performed in the background. Once the changes are applied, your v-Core-based Azure Cosmos DB for MongoDB account will be scaled to the new settings. The good news is that your application will not experience any downtime during this process.

It is important to note that you can only scale up or down the cluster tier and storage capacity. You cannot change the number of vCores and RAM independently. Additionally, keeping track on the cost of of these changes is important when scaling up or down.

## Monitor a v-Core-based Azure Cosmos DB for MongoDB account

Monitoring your v-Core-based Azure Cosmos DB for MongoDB account is important to ensure that your application is running smoothly and to identify any potential issues. Azure provides a variety of tools to help you monitor your Azure Cosmos DB account, including Azure Monitor, metrics, and logs. In this section, you will focus on using the v-Core-based Azure Cosmos DB for MongoDB account logs to monitor the account.

> [!NOTE]
> The *create-azure-resources.ps1* script should have created a Log Analytics workspace and Azure storage account for you, otherwise work with your Azure Administrator to create these resources.  You will use these resources to monitor your v-Core-based Azure Cosmos DB for MongoDB account.

### Enable diagnostic settings

One you have your Log Analytics workspace and Azure storage account, it's time to enable diagnostic settings for your v-Core-based Azure Cosmos DB for MongoDB account. This will allow you to collect logs and metrics from your Cosmos DB account and store them in the Log Analytics workspace. To do this, let's follow these steps:

1. log in to the [Azure portal](https://portal.azure.com).

1. Navigate to your v-Core-based Azure Cosmos DB for MongoDB account.

1. In the left-hand menu, select **Diagnostic settings** under the *Monitoring* section.

1. Select **+ Add diagnostic setting**.

1. In the *Diagnostic settings* pane, use the following settings:

    | Setting | Value |
    | --- | --- |
    | **Diagnostic setting name** | ***cosmosdb-mongodb-diag-settings*** |
    | *Logs* - **Category groups** | Select **audit** and **allLogs** |
    | *Logs* - **Categories** | Select **vCoreMongoRequest** if not already selected. |
    | **Metrics** | Select **AllMetrics** |
    | **Destination details** | Select **Send to Log Analytics** and select the Log Analytics workspace you created earlier. Select the **Resource specific** *destination table* |
    | **Destination details** | Select **Archive to storage account** and select the Azure storage account you created earlier. |

1. Select **Save** to apply the changes.

Your v-Core-based Azure Cosmos DB for MongoDB account is now configured to send logs and metrics to the Log Analytics workspace and the Azure storage account. To see it in action, let's run some queries against your Cosmos DB account.

### Run a simulated workload

To generate some data for your logs and metrics, let's run some queries against your v-Core-based Azure Cosmos DB for MongoDB account.

> [!NOTE]
> Make sure you have the necessary Cosmos DB environment variables in your **.env** file before running the workload application.  

> [!NOTE]
> Make sure you have the v-Core-based Azure Cosmos DB for MongoDB account firewall rules set to allow access from your current public IP address.  

1. Right-click on the **03-manage** folder and select **Open in integrated Terminal**.

1. **Launch the Application**: To start the application, enter the following commands.

    <details>
    <summary>Python</summary>
    
    ```powershell
    cd ./python
    pip install -v "pymongo==4.6.2"
    pip install -v "Faker==8.10.0"
    pip install -v "pynput==1.0.3"
    py load-data-run-workload.py
    ```

    </details>
    
    <details>
    <summary>Node.js</summary>
    
    ```powershell
    cd ./node.js
    npm install
    npm install @azure/openai
    npm start
    ```

    </details>

1. **Load local data into MongoDB**: Choose **option 1** to load data into the database. This step will setup your database and collections.

1. **Run workload on Database**: Choose **option 2** to run a simulated workload on the database. This step will run a series of queries against your database to emulate a workload.

You will come back a little later to stop the workload.  In the meantime, let's review the logs and metrics that are being generated.

### Review logs and metrics

1. log in to the [Azure portal](https://portal.azure.com).

1. Navigate to your v-Core-based Azure Cosmos DB for MongoDB account.

1. In the left-hand menu, Under *Monitoring*, select the **Logs** section.

1. In the *Logs* pane, by default you will see a set of queries already prepared for you.  You can run these queries to view the logs generated by your v-Core-based Azure Cosmos DB for MongoDB account or x out of the queries and run your own. for now, *let's X out of the **Queries** dialog*.

1. In the *Logs* pane, you can run a query to view the logs generated by your v-Core-based Azure Cosmos DB for MongoDB account.  Use the following query to view the logs:

    ```kql
    AzureDiagnostics
    | where ResourceProvider == "MICROSOFT.DOCUMENTDB"
    | where Resource == "<your-cosmosdb-account-name>"
    | project TimeGenerated, Resource, Category, Level, OperationName, ResultType, ResultSignature, ResultDescription, ResourceId, ResourceGroup, SubscriptionId
    | order by TimeGenerated desc
    ```

    Replace **<your-cosmosdb-account-name>** with the name of your v-Core-based Azure Cosmos DB for MongoDB account.

### Stop the simulated workload

Now that you have reviewed the logs and metrics, let's stop the simulated workload to avoid incurring unnecessary costs.

1. Return to the terminal where the workload application is running.
 
1. **Stop the workload**: Press **q** or **esc** to stop the workload.
 
1. Return to the workload application and choose **option 0** to exit the application.

There are many ways to monitor your v-Core-based Azure Cosmos DB for MongoDB account, we just scratched the surface. You can also use Azure Monitor to create alerts, view metrics, and more. You can also use the Azure Monitor API to integrate with your own monitoring solutions. Learn more about [Azure Monitor](https://docs.microsoft.com/en-us/azure/azure-monitor/).

## Clean Up

After completing the lab exercises, it's important to clean up any resources you created to avoid incurring unnecessary costs. Here's how:

1. **Azure Portal**: Sign in to the [Azure portal](https://portal.azure.com).

1. **Delete Resource Group**: If you created a new resource group for this lab, navigate to *Resource groups*, find your group, and delete it. This action removes all the resources contained within it, including your Azure Cosmos DB instance and any Azure OpenAI resources.

1. **Manually Delete Individual Resources**: If you added resources to an existing group, you need to delete each resource individually. Navigate to each resource created for this lab (for example, Azure Cosmos DB for MongoDB, Azure OpenAI account) and delete them.

1. **Verify Deletion**: Confirm all resources you no longer need were successfully removed and are no longer listed in your Azure portal.

1. **Review Billing**: Check your Azure billing section to ensure no unexpected charges are incurred, verifying that all unwanted resources were successfully deleted.

This cleanup process helps maintain your Azure account organized and free from unnecessary charges, ensuring you only pay for resources you actively use.

# Conclusion

In this lab, you learned to manage, scale, and monitor a v-Core-based Azure Cosmos DB for MongoDB account. You used monitoring tools to track operations. You also learned how to scale your account to handle increased or decreased traffic. You can now apply these skills to your own applications and databases.