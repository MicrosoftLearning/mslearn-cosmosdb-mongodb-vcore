---
lab:
    title: 'Manage a vCore-based Azure Cosmos DB for MongoDB account'
    module: 'Module 3 - Manage vCore-based Azure Cosmos DB for MongoDB'
---

In this lab, you learn how to manage, scale, monitor, and generate alerts on a vCore-based Azure Cosmos DB for MongoDB account. You use monitoring tools to track operations and scale your account to handle increased or decreased traffic. You learn how to enable diagnostic settings to collect logs and metrics from your Cosmos DB account. You learn how to create alerts to notify you when certain conditions are met. You run a simulated workload to generate some data for your logs and metrics. Finally, you review the logs and metrics that are being generated.

### Objectives

- Scale the Azure Cosmos DB for MongoDB account to meet performance needs by adjusting cluster tier, storage capacity, and enabling high availability.
- Monitor the Azure Cosmos DB account using diagnostic settings to collect and analyze logs and metrics.
- Generate alerts to notify you when certain conditions are met.

### Build your own lab environment

If you need to build your own lab environment, you need the following components and resource access.

- **Visual Studio Code**: Ensure Visual Studio Code is installed on your machine.
- **Azure Subscription**: Have access to an Azure Subscription for creating necessary resources.

## Clone the Repository

- Open **Visual Studio Code**.
- Press **CTRL+SHIFT+P** to open the command palette.
- Run +++**Git: Clone**+++ and clone the repository +++**https://github.com/MicrosoftLearning/mslearn-cosmosdb-mongodb-vcore.git**+++.
- Navigate to the cloned repository directory.
- Right-click on the **03-manage** folder and select **Open in integrated Terminal**.

## Create Azure Resources

You need access to the following Azure resources for this lab:

- vCore-based Azure Cosmos DB for MongoDB account
- Azure storage account
- Log Analytics workspace

You can create these resources via the *Azure portal* or use the ***create-azure-resources.ps1*** PowerShell script with the ***.env** file. Don't use existing production resources for this lab or any lab.

### Use the .env file

*This file must either be populated manually, or by the create-azure-resources.ps1 script before you can run your application, since it contains the connection information to your Azure resources.*

This file is both used to retrieve and store the necessary environment variables for both the PowerShell script and the vector search application APIs. It's the easiest way to prepopulate your resource information. The file is used to store the environment variables for your Azure Cosmos DB and Azure OpenAI account.

If you already have an existing Resource Group or a vCore-based Azure Cosmos DB for MongoDB account that you would like to use, just fill in those values in the **.env** file and set the skip create option for that resource to **true**. By default, the *create-azure-resources.ps1* script uses this file to retrieve the necessary environment variables. The *create-azure-resources.ps1* script populates the environment variables with default values if not specified in the **.env** file.

To learn more about the ***.env*** file and its parameters, review the [***.env*** file documentation](./00-env-file.md).

### Use the create-azure-resources.ps1 script

>[!note]
> You don't need to run the *create-azure-resources.ps1* script and can skip to the next section if you already have the necessary Azure resources created.

If you aren't using existing resources, or you aren't creating them through the Azure portal, this script creates the necessary Azure resources for this lab. It gives you the flexibility to create some or all of the resources required for this lab. You can either run the script as is or modify it to suit your needs. The resources created by the script include:

- Resource Group
- vCore-based Azure Cosmos DB for MongoDB account
- Azure storage account
- Log Analytics workspace

The script has a rich set of parameters to help you customize the resources to be created. It also uses an ***.env*** file to retrieve and store the necessary environment variables for both the PowerShell script and the vector search application APIs.

>[!note]
> While these parameters can be passed directly to the script, *we recommend you use the ***.env*** file to prepopulate your resource information instead of adding the parameters when executing the script. This will make it easier for you to manage your environment variables.*

To learn more about the PowerShell script and its parameters, review the [***create-azure-resources.ps1*** documentation](./00-powershell-script.md).

>[!note]
> Make sure the tenant, location and subscription you use allows for the creation of the necessary resources. Not all locations and subscriptions might allow or support the creation of all the required resources needed for this lab. If you encounter any issues, please reach out to your Azure Administrator.

### Run the create-azure-resources.ps1 script to create the necessary Azure resources

To create the necessary Azure resources for this lab:

1. Run the following command in the integrated terminal. Sign in with the provided credentials.

    ```powershell
    az login
    ```

    | Item | Value |
    |:---------|:---------|
    | Username   | +++**@lab.CloudPortalCredential(User1).Username**+++   |
    | Password   | +++**@lab.CloudPortalCredential(User1).Password**+++   |

1. Run the following command in the integrated terminal to provision the resources.

    ```powershell
    ./create-azure-resources.ps1
    ```

1. Copy and save the environment variables returned by the script in case you need them later. You can verify the resources created in the Azure portal.

1. Make sure that the **.env** file is populated with the resource information.

>[!note]
> The vCore-based Azure Cosmos DB for MongoDB account will need a firewall rule to allow access from your current public IP address.  If your Azure Cosmos DB account was generated by the *create-azure-resources.ps1* script, it should have created the firewall rule for you.  Check the existing firewall rules under the ***Networking*** *Setting* section of the *Azure Cosmos DB Account*.  If you are not sure what your current public IP address is, you can use the following command to find out:
> ```powershell
> Invoke-RestMethod -Uri 'http://ipinfo.io/ip' -Method Get
> ```

Once the resources are created and your **.env** file is populated with the resource information, you can proceed to the next step.

## Scale a vCore-based Azure Cosmos DB for MongoDB account

As your application performance needs changes, you might need to scale your vCore-based Azure Cosmos DB for MongoDB account to handle increased or decreased traffic. You can scale your account by changing the cluster tier (number of vCores and RAM), the storage capacity, and enabling high availability. To do scale your account, let's follow these steps:

1. Open a browser, go to +++**https://portal.azure.com**+++ and sign in with the following credentials:

    | Item | Value |
    |:---------|:---------|
    | Username   | +++**@lab.CloudPortalCredential(User1).Username**+++   |
    | Password   | +++**@lab.CloudPortalCredential(User1).Password**+++   |

1. Navigate to your vCore-based Azure Cosmos DB for MongoDB account.

1. In the left-hand menu, select **Scale** under the *Settings* section.

1. In the *Scale* pane, you can change the cluster tier, storage capacity, and enable high availability.  

    1. Let's try changing the cluster tier to a lower tier. Select the **Cluster tier** pulldown, and select the **M30 tier, 2 vCores 8 GiB RAM**. If you're already using the M30 tier, you can try selecting the **M40 tier, 4 vCore 16 GiB RAM**. Notice how the cost changes.

    1. Let's leave the storage capacity alone, but you can select the pulldown to review the different storage sizes available for that cluster tier.

    1. Let's enable **High availability** and notice how the cost doubles. Go ahead and disable it again.

1. Once you made your changes, select **Save** to apply the changes.

Scaling your account will take a few minutes to complete, but go ahead and continue to the next section of the lab while these changes are performed in the background. Once the changes are applied, your vCore-based Azure Cosmos DB for MongoDB account is scaled to the new settings. The good news is that your application won't go down during this process.

It's important to note that you can only scale up or down the cluster tier and storage capacity. You can't change the number of vCores and RAM independently. Additionally, keeping track on the cost of these changes is important when scaling up or down.

## Monitor a vCore-based Azure Cosmos DB for MongoDB account

Monitoring your vCore-based Azure Cosmos DB for MongoDB account is important to ensure that your application is running smoothly and to identify any potential issues. Azure provides various tools to help you monitor your Azure Cosmos DB account, including Azure Monitor, metrics, and logs. In this section, you focus on using the vCore-based Azure Cosmos DB for MongoDB account logs to monitor the account.

>[!note]
> The *create-azure-resources.ps1* script should have created a Log Analytics workspace and Azure storage account for you, otherwise work with your Azure Administrator to create these resources.  You will use these resources to monitor your vCore-based Azure Cosmos DB for MongoDB account.

### Enable diagnostic settings

One you have your Log Analytics workspace and Azure storage account, it's time to enable diagnostic settings for your vCore-based Azure Cosmos DB for MongoDB account. When you enable diagnostics, allows you to collect logs and metrics from your Cosmos DB account and store them in the Log Analytics workspace. To do enable diagnostics, let's follow these steps:

1. Sign in to the Azure portal.

1. Navigate to your vCore-based Azure Cosmos DB for MongoDB account.

1. In the left-hand menu, select **Diagnostic settings** under the *Monitoring* section.

1. Select **+ Add diagnostic setting**.

1. In the *Diagnostic settings* pane, use the following settings:

    | Setting | Value |
    | --- | --- |
    | **Diagnostic setting name** | +++***cosmosdb-mongodb-diag-settings***+++ |
    | *Logs* - **Category groups** | Select **audit** and **allLogs** |
    | *Logs* - **Categories** | Select **vCoreMongoRequest** if not already selected. |
    | **Metrics** | Select **AllMetrics** |
    | **Destination details** | Select **Send to Log Analytics** and select the Log Analytics workspace you created earlier. Select the **Resource specific** *destination table* |
    | **Destination details** | Select **Archive to storage account** and select the Azure storage account you created earlier. |

1. Select **Save** to apply the changes.

Your vCore-based Azure Cosmos DB for MongoDB account is now configured to send logs and metrics to the Log Analytics workspace and the Azure storage account. To see it in action, let's run some queries against your Cosmos DB account.

### Run a simulated workload

To generate some data for your logs and metrics, let's run some queries against your vCore-based Azure Cosmos DB for MongoDB account.

>[!note]
> Make sure you have the necessary Cosmos DB environment variables in your **.env** file before running the workload application.  

>[!note]
> Make sure you have the vCore-based Azure Cosmos DB for MongoDB account firewall rules set to allow access from your current public IP address.  

1. Right-click on the **03-manage** folder and select **Open in integrated Terminal**.

1. **Launch the Application**: To start the application, enter the following commands.

    <details>
    <summary>Python</summary>
    
    ```powershell
    cd ./python
    pip install -v "pymongo==4.6.2"
    pip install -v "Faker==8.10.0"
    pip install -v "keyboard==0.13.5"
    py load-data-run-workload.py
    ```

    </details>
    
    <details>
    <summary>Node.js</summary>
    
    ```powershell
    cd ./node.js
    npm install
    npm start
    ```

    </details>

1. **Load local data into MongoDB**: Choose **option 1** to load data into the database. This step sets up your database and collections.

1. **Run workload on Database**: Choose **option 2** to run a simulated workload on the database. This step runs a series of queries against your database to emulate a workload.

You come back a little later to stop the workload. In the meantime, let's review the logs and metrics that are being generated.

### Review the logs

1. Sign in to the Azure portal.

1. Navigate to your vCore-based Azure Cosmos DB for MongoDB account.

1. In the left-hand menu, Under *Monitoring*, select the **Logs** section.

1. In the *Logs* pane, by default, a set of queries already prepared for you're displayed. You can run these queries to view the logs generated by your vCore-based Azure Cosmos DB for MongoDB account or ***X*** out of the queries and run your own. for now, *let's ***X*** out of the **Queries** dialog*.

1. Let's get familiar with the **Query** pane.

    1. If you select the Table tab, you can see the different tables that are available to query. In this case, you should see a table called **VCoreMongoRequests** under the *Azure Cosmos DB for MongoDB (vCore)* section. This table contains the logs generated by your vCore-based Azure Cosmos DB for MongoDB account.
    1. Under the **Queries** tab, you see some sample queries that you can run to view the logs. You can also write your own queries here.
    1. On the right-hand side, you're able to write and edit your queries. You can select to **Run**, **Save, and define a **Time range** for your queries. Let's go ahead and write and run some queries.

1. In the *Logs* pane, you can run a query to view the logs generated by your vCore-based Azure Cosmos DB for MongoDB account. These queries are written in KQL (Kusto Query Language). You can use the **Run** button to run the query and view the results.

    1. Let's try the following query to view the number of requests made per minute to your Cosmos DB account over the last 24 hours. Change the local time zone formula to match your local time zone if necessary:

        ```kql
        VCoreMongoRequests
        // Time range filter:  | where TimeGenerated between (StartTime .. EndTime)
        | extend LocalTimeGenerated = TimeGenerated - 6h
        | project LocalTimeGenerated, DurationBin=tostring(bin(DurationMs, 5))
        | summarize count() by bin(LocalTimeGenerated, 1m), tostring(DurationBin)
        ```

    1. Let's find out what commands ran in the last 20 minutes (note that the timezone use is UTC):

        ```kql
        VCoreMongoRequests
        | where TimeGenerated > ago(20m)
        | project TimeGenerated, DatabaseName, CollectionName, DurationMs, PiiCommandText
        ```

KQL is a powerful query language allows you to create complex queries to get better insight on your logs. To learn more about running KQL queries, review the [Kusto Query Language (KQL) documentation](https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/).

There are several ways to monitor your vCore-based Azure Cosmos DB for MongoDB account, we scratched the surface. You can also use Azure Monitor to create alerts, view metrics, and more. Learn more about [Azure Monitor](https://docs.microsoft.com/en-us/azure/azure-monitor/).

### Create an alert rule

You can also create alerts to notify you when certain conditions are met. For example, you can create an alert to notify you when the number of requests to your Cosmos DB account exceeds a certain threshold. To do generate an alert rule, let's follow these steps:

1. In the *Monitoring* section, select the **Alerts** button.

1. Select the **Create alert rule** button or **Alert rule** under the **+ Create** pulldown.

1. On the *Created rule* pane, use the following settings:

    1. **Scope** tab: Select your vCore-based Azure Cosmos DB for MongoDB account.

    1. **Condition** tab:
        1. Enter the following settings: 
            - **Signal name**: Select **Custom log search**.
            - *Logs pane*: Enter +++**VCoreMongoRequest**+++ as your query, run the query, and select **Continue Editing Alert**.
            - **Measure**: Select **Table rows**.
            - **Aggregation type**: Select **Count**.
            - **Aggregation granularity**: Select **5 Minutes**.
            - **Operator**: Select **Greater than**.
            - **Threshold**: Enter +++**500**+++ as the threshold.
            - **Frequency of evaluation**: Select **Every 5 minutes**.

            The alert calculates how much it costs you monthly to run this alert.

        1. On the Preview section, change the **Time range** to **Over the last 6 hours** and review the graph to compare the current execution numbers against the chose.

        1. Select the **Next: Actions >** button.

    1. **Actions** tab:
        1. Select the **Use quick actions** radio button.

        1. Fill in the **Use quick actions** pane.
            - **Action group name**: +++**Notify DBAs**+++.
            - **Display name**: +++**High number of transactions detected**+++.
            - **Email**: Selected and enter your email address.

        1. Select the **Review + create** button.

            1. Select the **Use quick actions** radio button.

            1. Fill in the **Use quick actions** pane.
                - **Action group name**: +++**Notify DBAs**+++.
                - **Display name**: +++**High number of transactions detected**+++.
                - **Email**: Selected and enter your email address.

        1. Select the **Next: Details >** button.

    1. **Details** tab:
        1. Enter the following settings:
            - **Severity**: **2 - Warning**
            - **Alert rule name**: +++**High number of transactions**+++
            - **Description**: +++**Alert when the number of transactions exceeds 500 every 5 minutes.**+++

        1. Select the **Review + create** button.

    1. Select the **Create** button.

Once your alert is created, the portal displays a dashboard with the status of all your alerts. Your workload doesn't generate enough data to trigger the alert.

### Stop the simulated workload

Now that you reviewed the logs and created an alert, let's stop the simulated workload to avoid incurring unnecessary costs.

1. Return to the terminal where the workload application is running.

1. **Stop the workload**: Press **q** or **Esc** to stop the workload.

1. Return to the workload application and choose **option 0** to exit the application.

Monitoring and creating alerts for your vCore-based Azure Cosmos DB for MongoDB account is important to ensure that your application is running smoothly and to identify any potential issues. Monitoring and alerting are integral parts of managing your vCore-based Azure Cosmos DB for MongoDB account.

## Clean Up

After completing the lab exercises, it's important to clean up any resources you created to avoid incurring unnecessary costs. Here's how:

1. **Azure Portal**: Sign in to the Azure portal.

1. **Delete Resource Group**: If you created a new resource group for this lab, navigate to *Resource groups*, find your group, and delete it. This action removes all the resources contained within it, including your Azure Cosmos DB instance and any Azure OpenAI resources.

1. **Manually Delete Individual Resources**: If you added resources to an existing group, you need to delete each resource individually. Navigate to each resource created for this lab (for example, Azure Cosmos DB for MongoDB, Azure OpenAI account) and delete them.

1. **Verify Deletion**: Confirm all resources you no longer need were successfully removed and are no longer listed in your Azure portal.

1. **Review Billing**: Check your Azure billing section to ensure no unexpected charges are incurred, verifying that all unwanted resources were successfully deleted.

This cleanup process helps maintain your Azure account organized and free from unnecessary charges, ensuring you only pay for resources you actively use.

# Conclusion

In this lab, you learned to manage, scale, monitor, and generate alerts on a vCore-based Azure Cosmos DB for MongoDB account. You used monitoring tools to track operations and generate alerts. You also learned how to scale your account to handle increased or decreased traffic. You can now apply these skills to your own applications and databases.
