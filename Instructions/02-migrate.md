---
lab:
    title: 'Migrate a MongoDB database to a vCore-based Azure Cosmos DB for MongoDB account'
    module: 'Module 2 - Migrate to vCore-based Azure Cosmos DB for MongoDB'
---

Data migration is a critical step in the process of moving from an existing MongoDB database to a vCore-based Azure Cosmos DB for MongoDB account. While there are several ways to migrate a MongoDB database to a vCore-based Azure Cosmos DB for MongoDB account, this lab focuses on using the MongoDB native tools to migrate the database. The MongoDB native tools are the most common way to migrate a MongoDB database to another. Most MongoDB administrators and developers are familiar with these tools.

>[!NOTE]
> While this lab uses the MongoDB community edition, similar migration steps can be used for other MongoDB editions.

### Objectives

In this lab, you learn how to use the MongoDB native tools to migrate a MongoDB database to a vCore-based Azure Cosmos DB for MongoDB account. You use the following tools:

- **mongodump**: This tool is used to dump the data from the local MongoDB server into a BSON (Binary JSON) file.
- **mongorestore**: This tool is used to restore the dumped data into the vCore-based Azure Cosmos DB for MongoDB server.

### Build your own lab environment

If you need to build your own lab environment, you need the following components and resource access.

- **Visual Studio Code**: Ensure Visual Studio Code is installed on your machine.
- **Azure Subscription**: Have access to an Azure Subscription for creating necessary resources.

## Clone the Repository

- Open **Visual Studio Code**.
- Press **CTRL+SHIFT+P** to open the command palette.
- Run +++**Git: Clone**+++ and clone the repository +++https://github.com/MicrosoftLearning/mslearn-cosmosdb-mongodb-vcore.git+++.
- Navigate to the cloned repository directory.
- Right-click on the **02-migrate** folder and select **Open in integrated Terminal**.

## Create Azure Resources

You need access to the following Azure resources for this lab:

- vCore-based Azure Cosmos DB for MongoDB account

You can create these resources via the *Azure portal* or use the ***create-azure-resources.ps1*** PowerShell script with the ***.env** file. Don't use existing production resources for this lab or any lab.

### Use the .env file

*This file must either be populated manually, or by the create-azure-resources.ps1 script before you can run your application, since it contains the connection information to your Azure resources.*

This file is both used to retrieve and store the necessary environment variables for both the PowerShell script and the vector search application APIs. It's the easiest way to prepopulate your resource information. The file is used to store the environment variables for your Azure Cosmos DB and Azure OpenAI account.

If you already have an existing Resource Group, a vCore-based Azure Cosmos DB for MongoDB account, an Azure Storage Account or an Azure Log Analytics workspace that you would like to use, just fill in those values in the **.env** file and set the skip create option for that resource to **true**. By default, the *create-azure-resources.ps1* script uses this file to retrieve the necessary environment variables. Note that the *create-azure-resources.ps1* script will populate the environment variables with default values if not specified in the .env file.

To learn more about the ***.env*** file and its parameters, review the [***.env*** file documentation](./00-env-file.md).

### Use the create-azure-resources.ps1 script

>[!note]
> You don't need to run the *create-azure-resources.ps1* script and can skip to the next section if you already have the necessary Azure resources created.

If you aren't using existing resources, or you aren't creating them through the Azure portal, this script creates the necessary Azure resources for this lab. It gives you the flexibility to create some or all of the resources required for this lab. You can either run the script as is or modify it to suit your needs. The resources created by the script include:

- Resource Group
- vCore-based Azure Cosmos DB for MongoDB account

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

## Install and load data into the MongoDB community edition on your local machine

Unless you have a nonproduction MongoDB server installed with access the internet, let's install the MongoDB community edition on your local machine. For more information on how to do this installation, review the instructions in the official MongoDB documentation by visiting +++https://docs.mongodb.com/manual/administration/install-community+++.

### Install the MongoDB community edition

Let's install the MongoDB community edition on your local machine.

1. Open your browser and go to the **MongoDB Community Server Download** page from the official MongoDB website +++https://www.mongodb.com/try/download/community+++.

1. Select the **Select package** button and select the proper settings for your environment. For example, if you're using *Windows*, select the **Windows x64** platform and the **msi** package.

    | **Version** | ***6.0.14*** |
    | **Platform** | Your current OS/Platform |
    | **Package** | Your current install package type |

1. Select the **Download** button to download the installer.

1. Once the installer is downloaded, run the installer and follow the installation instructions for a **Complete** install.

    - Choose all default options.
    - Service name should be +++**MongoDB**+++.
    - Select to **Install MongoDB Compass**.

    This install should take a few minutes to complete.

1. Once the installation is complete, select the **Finish** button to close the installer if needed.

### Install the MongoDB Database Tools

We need a few tools to help us with the migration process. Let's install the MongoDB database tools on your local machine.

1. Open your browser and go to the **MongoDB Command Line Database Tools Download** page from the official MongoDB website +++https://www.mongodb.com/try/download/database-tools+++.

1. Select the proper settings for your environment. For example, if you're using *Windows*, select the **Windows x86_64** platform and the **msi** package.

    | **Version** | ***100.9.4*** or the latest version |
    | **Platform** | Your current OS/Platform |
    | **Package** | Your current install package type |

1. Select the **Download** button to download the installer.

1. Once the installer is downloaded, run the installer and follow the installation instructions for a **Complete** install. Choose all default options.

1. Once the installation is complete, select the **Finish** button to close the installer if needed.

Time to verify the installation.

1. Close Visual Studio Code and reopen it to ensure the environment variables are loaded.

1. Right-click on the **02-migrate** folder and select **Open in integrated Terminal**.

1. In the terminal windows, run the following command to verify the installation:

    If the server is up and running, it will reply every second or so, if it's down, it will eventually time out after around a minute.

    If the server is down, follow the instructions in the official MongoDB documentation at +++https://www.mongodb.com/docs/v6.0/tutorial/+++ to start the server.

>[!note]
> While the installation of MongoDB and its tools should have updated your PATH environment variable, if the command is not found, specify the path when calling the *mongostat* command. For example, if you installed the tools in the default location in the Windows environment, you can run the following command to verify the installation (replace the path with the actual path where the tools were installed and use that path in the other MongoDB Tools commands in this lab):
> ```bash
> & "C:\Program Files\MongoDB\Tools\100\bin\mongostat"
> ```

We should now have a running MongoDB server on your local machine. Let's load some data into it.

### Load data into the MongoDB community edition

1. Open a new terminal and navigate to the MongoDB Tools installation folder.

1. Run the following command to load the sample data into the MongoDB server:

    ```bash-wrap
    & mongoimport --host localhost --port 27017 --db cosmicworks --collection customers --jsonArray --file ../data/cosmicworks/customers.json
    & mongoimport --host localhost --port 27017 --db cosmicworks --collection products --jsonArray --file ../data/cosmicworks/products.json
    & mongoimport --host localhost --port 27017 --db cosmicworks --collection salesOrders --jsonArray --file ../data/cosmicworks/salesOrders.json
    ```

    This command loads the sample data into the MongoDB server running on your local machine.

We should now have a running MongoDB server with some data into it, it's time to migrate it to vCore-based Azure Cosmos DB for MongoDB.

## Migrate to a vCore-based Azure Cosmos DB for MongoDB account using MongoDB native tools (offline)

To export the data from the local MongoDB server and import it into the vCore-based Azure Cosmos DB for MongoDB account, you use the MongoDB **mongodump** and **mongorestore** native tools. In a production environment, if your database is large, you might need to search for other ways to migrate the database like through *Azure Data Migration Service*.

1. Dump the data from your local MongoDB server into a BSON file. Run the following command in the terminal:

    ```bash
    & mongodump --host localhost --port 27017 --db cosmicworks --out ../data/cosmicworks
    ```

    This command creates a BSON file in the `../data/cosmicworks` folder. The **mongodump** command outputs the progress of the dump operation.

1. Restore the dumped data into your vCore-based Azure Cosmos DB for MongoDB server. Replace **<user>**, **<password>**, **yourMongoDBClusterName**, and **yourDatabaseName** with your actual username, password, Azure MongoDB cluster name, and database name:

    ```bash
    & mongorestore --uri "mongodb+srv://<user>:<password>@yourMongoDBClusterName.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000" --db cosmicworks1 ../data/cosmicworks/cosmicworks
    ```

    This command restores the BSON file into your vCore-based Azure Cosmos DB for MongoDB server. The **mongorestore** command  outputs the progress of the restore operation.

>[!note]
> Don't forget to make sure the firewall rules for your vCore-based Azure Cosmos DB for MongoDB account are set to allow access from your current public IP address. If your Azure Cosmos DB account was generated by the *create-azure-resources.ps1* script, it should have created the firewall rule for you. Check the existing firewall rules under the ***Networking*** *Setting* section of the *vCore-based Azure Cosmos DB for MongoDB* account. If you are not sure what your current public IP address is, you can use the following command to find out:
> ```powershell
> Invoke-RestMethod -Uri 'http://ipinfo.io/ip' -Method Get
> ```

Let's verify the migration completed successfully.

1. Open the MongoDB Compass application.

1. Connect to your vCore-based Azure Cosmos DB for MongoDB connection string.

1. Select **Continue** on the warning screen.

1. You should see your database, collections, and documents in the left-hand navigation pane.

1. Close the MongoDB Compass application.

>[!note]
> Note that while you used the **mongodump** and **mongorestore** tools to migrate the data from your local MongoDB server to the vCore-based Azure Cosmos DB for MongoDB account, we could have also use **mongoexport** and **mongoimport** tools to do the same.

You should now have a running vCore-based Azure Cosmos DB for MongoDB server with the data from your local MongoDB server. You successfully migrated the data from your local MongoDB server to the vCore-based Azure Cosmos DB for MongoDB account using the MongoDB native tools.

## Clean Up

After completing the lab exercises, it's important to clean up any resources you created to avoid incurring unnecessary costs. Here's how:

1. **Azure Portal**: Sign in to the Azure portal.

1. **Delete Resource Group**: If you created a new resource group for this lab, navigate to *Resource groups*, find your group, and delete it. This action removes all the resources contained within it, including your Azure Cosmos DB instance and any Azure OpenAI resources.

1. **Manually Delete Individual Resources**: If you added resources to an existing group, you need to delete each resource individually. Navigate to each resource created for this lab (for example, Azure Cosmos DB for MongoDB, Azure OpenAI account) and delete them.

1. **Verify Deletion**: Confirm all resources you no longer need were successfully removed and are no longer listed in your Azure portal.

1. **Review Billing**: Check your Azure billing section to ensure no unexpected charges are incurred, verifying that all unwanted resources were successfully deleted.

This cleanup process helps maintain your Azure account organized and free from unnecessary charges, ensuring you only pay for resources you actively use.

## Conclusion

You successfully migrated a MongoDB database to a vCore-based Azure Cosmos DB for MongoDB account using the MongoDB native tools. There are several other ways to migrate a MongoDB database to a vCore-based Azure Cosmos DB for MongoDB account, including using Azure Data Studio for offline migrations and Azure Databricks for online/offline migrations. The method you choose depends on your specific requirements and constraints.
