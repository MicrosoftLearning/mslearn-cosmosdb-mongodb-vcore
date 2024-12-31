---
lab:
    title: 'Create a vCore-based Azure Cosmos DB for MongoDB account using the Azure portal'
    module: 'Module 1 - Get Started with vCore-based Azure Cosmos DB for MongoDB'
---

In this lab, we guide you through the process of creating a vCore-based Azure Cosmos DB for MongoDB account using the Azure portal. We walk you through the steps of setting up the Cosmos DB account, configuring the necessary settings, and preparing it for use. The focus is on understanding the different configuration options and how they affect the behavior and performance of the Cosmos DB. By the end of this lab, you have a fully configured Cosmos DB for MongoDB ready for data storage and retrieval.

### Objectives

- Understand the process of creating a new resource in Azure portal.
- Learn how to set up a vCore-based Azure Cosmos DB for MongoDB account.
- Familiarize with the different configuration options available during the setup.
- Understand the process of reviewing and finalizing the setup of the Cosmos DB account.
- Learn how to connect to the newly created Cosmos DB account using the Azure portal's Mongo Shell.

## Create your vCore-based Azure Cosmos DB for MongoDB account

Let's go ahead and learn how easy is to create your vCore-based Azure Cosmos DB for MongoDB account using the Azure portal. To create this account, follow these steps:

1. Open a browser, go to +++https://portal.azure.com+++ and sign in with the following credentials:

    | Item | Value |
    |:---------|:---------|
    | Username   | +++**@lab.CloudPortalCredential(User1).Username**+++   |
    | Password   | +++**@lab.CloudPortalCredential(User1).Password**+++   |

1. In the left-hand menu, select on the **Create a resource** option.

1. In the **Create a resource** window, search for **Azure Cosmos DB**.

1. In the **Marketplace** window, select **Azure Cosmos DB** and select the **Create** button.

1. In the **Azure Cosmos DB** window, select the **Create** button.

1. In the **Create Azure Cosmos DB Account** window, select **Azure Cosmos DB for MongoDB**, and select the **Create** button.

1. In the **Create Azure Cosmos DB Account - Choose Architecture** window, select **vCore cluster (Recommended)** and select the **Create** button.

1. In the **Create Azure Cosmos DB for MongoDB cluster** window, fill in the details (leave other's blank):

    1. Basics tab:

        | Field | Action |
        | --- | --- |
        | Subscription | Choose the Azure subscription that you want to use for this Cosmos DB account. |
        | Resource group | If your Azure account is allowed, create a new resource group, if not, select a nonproduction resource group.  |
        | Cluster name | Enter a unique name to identify your Cosmos DB cluster. This name must be unique across all Azure clusters. |
        | Location | Select a geographic location. Depending on your subscriptions, some regions might not allow you to create the cluster. Contact your Azure Administrator if you have any issues. |
        | Cluster tier | Select **Configure**. Familiarize yourself with all the settings on the **Scale** window. Select **Free tier** and **Save**.|
        | MongoDB version | **6.0** |
        | Admin username | +++**cosmosClusterAdmin**+++ |
        | Password | ***Enter a strong password***. |
        | Confirm password | ***Enter the same password***. Copy that password somewhere safe, you need it later. |

        >[!note]
        > When you select **Free tier** under the **Cluster tier** section, you'll notice that *Free tier* checkbox is now also selected under the *Basics* tab. While you could have selected that checkbox on the *Basics* tab, we wanted you to familiarize yourself with the *cluster tier* options.
        >
        > Also note that you can only have one *Free tier* cluster per Azure account. If you already used your free account, just select the **M25 tier, 2 (Burstable) vCores** cluster tier to reduce cost since you don't need anything stronger for this lab.
        >
        > Another option you'll notice on the **Cluster tier** is the **High Availability** checkbox. On a production environment, while this option will incur additional cost, you should strongly consider if preventing possible downtime is worth that cost.

    1. Networking tab:

        | Field | Action |
        | --- | --- |
        | Connectivity method | **Public access (allowed IP addresses)** |
        | Firewall rules | Select the **Allow public access from Azure services and resources within Azure to this cluster** checkbox. This will allow you to use the Azure portal Mongo Shell.  |
        | Firewall rules | Manually add all the IP ranges that you would like to grant access to your Cosmos DB account by selecting a *Rule Name*, a *Start IP address* and an *End IP address.* |

        >[!note]
        > On a production environment, you would likely select **Private Access** for your *conectivity method* and use a *virtual network* and a *subnet* provided by your Azure network administrator. You will also most likely set private endpoints for access to the vCore-based Azure Cosmos DB for MongoDB account.
        >
        > Under the **Firewall rules** section is where you can add specific IP addresses that are allowed to access the Cosmos DB account. This is useful for restricting access to only specific IP addresses, such as your organization's IP addresses. You will notice there are two options: **+ Add current client IP address (your current public IP address)** and **+ Add 0.0.0.0 - 255.255.255.255**. The first option will add your current IP address to the list of allowed IP addresses, which could be benign if your public IP from your client never changes. The second option will allow you to add the range of ***ALL*** IP addresses in the internet. Be very careful of ever selecting that second option, since it opens your cluster to the whole internet.

1. Select on the **Review + create** button at the bottom.

1. In the **Review + create** tab, review your account settings, and then select the **Create** button.

>[!alert] It takes 5+ minutes for the vCore-based Azure Cosmos DB for MongoDB account to be created. Once the account is created, you can use the Azure portal to access your account.

## Connect to your vCore-based Azure Cosmos DB for MongoDB account using the Azure portal

Time to connect to your vCore-based Azure Cosmos DB for MongoDB account using the Azure portal. To do connect to the account, follow these steps:

1. If you aren't signed in, sign in to the Azure portal.

1. In the search bar at the top of the portal, type **Azure Cosmos DB** and select it from the search results.

1. In the **Azure Cosmos DB** window, select your newly created vCore-based Azure Cosmos DB for MongoDB account.

Let's get familiar with a couple of options available to you in the *Azure Cosmos DB for MongoDB (vCore)* window. You notice that there are several options available to you in the menu, including **Overview**, **Quit start**, **Networking**, **Connection string**, among others. For this lab, you focus on those four options you listed.

1. **Overview**: the Overview option provides you with a quick overview of your vCore-based Azure Cosmos DB for MongoDB account. The overview includes the account's name, status, subscription, resource group, and location. This overview also includes the MongoDB version, admin username, cluster tier, shard count, disk size, connectivity method, and high availability. One interesting option available is to **Reset password**.

    1. **Reset password**: On the top of the overview page, select **Reset password**. You're prompted to enter a new password and to confirm it. This option is useful if you ever need to change the password for the admin user.

    1. Unless you want to change the password, just select **X discard**. If you do change the password, make sure to update your records with the new password.

1. **Quick start**: You'll skip this one for now and revisit it in the next section of the lab.

1. **Networking**: This tab provides you with the options to configure the network settings for your vCore-based Azure Cosmos DB for MongoDB account. This option includes the ability to add IP addresses to the firewall rules, private endpoint connections and allow public access from Azure services and resources within Azure to this cluster.

1. **Connection string**: This option should list the connection string your application needs to connect to this cluster. Remember that just knowing the connection string isn't enough to connect to the cluster. Remember that you also need to ensure that the IP address from where you're connecting is allowed in the firewall rules.

    1. **Connection String**: Select on the **Copy** button to copy the connection string to your clipboard. You use this connection string to connect to your vCore-based Azure Cosmos DB for MongoDB account.

    1. Copy the connection string to your application's configuration file or to a secure location for later use in your application.

### Connect to your vCore-based Azure Cosmos DB for MongoDB account using the Azure portal's Mongo Shell

Now that you have your vCore-based Azure Cosmos DB for MongoDB account created, let's connect to it using the Azure portal's Mongo Shell. To connect, follow these steps:

1. In the **Azure Cosmos DB for MongoDB (vCore)** window, select **Quick start**.

    >[!note]
    > If you see the warning ***The Network settings for this account are preventing access from Data Explorer. Please allow access from Azure Portal to proceed.***, you will need to go back to the **Networking** tab and allow public access from Azure services and resources within Azure to this cluster.

1. In the **Quick start** window, select **Launch quick start**. This option creates a sample database for you to test on. In a production environment, you would most likely not use the **Launch quick start** option, since you would be creating your own databases and collections.

    1. Enter the password for the admin user you created when you created the vCore-based Azure Cosmos DB for MongoDB account in the Mongo Shell window. Select **Next**.

    1. Select the **Create new database and collection** button. On the Mongo Shell screen, you notice that the MongoDB commands to create the new database and collection were run. Select **Next**.

    1. Select the **Load data** button. On the Mongo Shell screen, notice that the MongoDB ***insertMany*** command with a set of JSON docs runs to load the sample data into the collection. Select **Next**.

    1. There are three queries you can run to test the data. Select the **Try query** button for each of the three queries. On the Mongo Shell screen, notice that the MongoDB ***find*** command runs to retrieve the data. Select **Next**.

    1. Select the **Done** button to exit the ***Launch quick start*** window.

1. In the **Quick start** window, select **Mongo Shell**.

    1. Enter the password for the admin user you created when you created the vCore-based Azure Cosmos DB for MongoDB account in the Mongo Shell window.

    1. To test the connection, let's run some MongoDB commands. Run the following commands:

        1. Show databases:
            ```bash
            show dbs
            ```
    
        1. switch to the quickstartDB database.
            ```bash
            use quickstartDB
            ```
    
        1. Show collections:
            ```bash
            show collections
            ```
    
        1. find all documents in the sampleCollection collection:
            ```bash
            db.sampleCollection.find()
            ```
            
        1. exit the Mongo Shell:
           ```
           exit
           ```

        

You now have a fully configured vCore-based Azure Cosmos DB for MongoDB account and you connected to it using the Azure portal's Mongo Shell. You're ready to start using it to store and retrieve data.

## Clean Up

After completing the lab exercises, it's important to clean up any resources you created to avoid incurring unnecessary costs. Here's how:

1. **Azure Portal**: Sign in to the Azure portal.

1. **Delete Resource Group**: If you created a new resource group for this lab, navigate to *Resource groups*, find your group, and delete it. This action removes all the resources contained within it, including your Azure Cosmos DB instance.

1. **Manually Delete Individual Resources**: If you added resources to an existing resource group, you need to delete each resource individually. Navigate to the vCore-based Azure Cosmos DB for MongoDB account and delete it.

1. **Verify Deletion**: Confirm that the vCore-based Azure Cosmos DB for MongoDB account resource you no longer need was successfully removed and is no longer listed in your Azure portal.

1. **Review Billing**: Check your Azure billing section to ensure no unexpected charges are incurred, verifying that all unwanted resources were successfully deleted.

>[!alert] This cleanup process helps maintain your Azure account organized and free from unnecessary charges, ensuring you only pay for resources you actively use.

## Conclusion

This lab guided you through how to set up a vCore-based Azure Cosmos DB for MongoDB account using the Azure portal. The lab showed you how to connect to the newly created vCore-based Azure Cosmos DB for MongoDB account using the Azure portal's Mongo Shell. You learned how to configure the network settings for your vCore-based Azure Cosmos DB for MongoDB account and how to retrieve the connection string for your application. You also learned how to reset the password for the admin user. You should now have a good understanding of the different configuration options available when setting up a vCore-based Azure Cosmos DB for MongoDB account and how to connect to it using the Azure portal's Mongo Shell. In the next module, you'll learn how to migrate existing MongoDB databases to your vCore-based Azure Cosmos DB for MongoDB account.
