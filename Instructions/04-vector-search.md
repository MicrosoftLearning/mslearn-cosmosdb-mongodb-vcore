# Lab: Implement Vector Search with Azure Cosmos DB for MongoDB and Azure OpenAI

## Introduction

In this lab, we'll guide you through the process of implementing a vector search in a v-Core-based Azure Cosmos DB for MongoDB. We'll utilize Azure Blob Storage for storing our data and Azure OpenAI for generating document embeddings. The focus will be on the `products` collection, where we'll perform vector searches based on product categories and names.

### Objectives

- Load data from Azure Blob Storage to a local directory.
- Import data into v-Core-based Azure Cosmos DB for MongoDB, generating embeddings for `category` and `name` fields of each product during the process.
- Create a Vector index on the generated vector column.
- Perform vector searches using prompts and display the closest matching products.
- Enhance vector search results with GPT-3 for more detailed insights.

## Build the Environment

TBD (To be detailed later)

## Pre-requisites

### Software and Account Setup

1. **Visual Studio Code**: Ensure Visual Studio Code is installed on your machine.
2. **Azure Subscription**: Have access to an Azure Subscription for creating necessary resources.

### Clone the Repository

- Open **Visual Studio Code**.
- Press **CTRL+SHIFT+P** to open the command palette.
- Run **Git: Clone** and clone the repository `https://github.com/MicrosoftLearning/mslearn-cosmosdb-mongodb-vcore.git`.
- Navigate to the cloned repository directory, right-click on the language-specific folder (Python/Node.js) and select **Open in Integrated Terminal**.
- Installation script details will be provided later.

## Create Azure Resources

You'll need several Azure resources for this lab:

- Azure Cosmos DB for MongoDB (v-Core-based)
- Azure OpenAI account, including completion deployments

You can create these resources via the Azure Portal or use the `create-azure-resources.ps1` PowerShell script. Details on script usage and .env configuration will be shared later.

<details>
<summary>Python</summary>

```python
# Python-specific instructions and code snippets
```
</details>

<details>
<summary>Node.js</summary>

```javascript
// Node.js-specific environment setup instructions and code
```
</details>

## Implementing Vector Search

### Creating Document Embeddings

Focus on the `products` collection. We'll generate embeddings for the `category` + `name` fields of each product.

#### Update `generateProductEmbedding` Function

- Navigate to `./Collections/products`.
- Replace the `generateProductEmbedding` function with the provided code snippet.

CODE HERE


This function selects fields to generate embeddings for, calls Azure OpenAI to generate these embeddings, and stores them in a vector column in the database.

#### Update `generateEmbeddings` Function

- Navigate to `./SearchComponents/embeddings`.
- Replace the `generateEmbeddings` function with the provided code snippet.

CODE HERE


This function uses Azure OpenAI to generate embeddings for any given string, facilitating the creation of our vector column for searches.

### Generating the Vector Index

#### Update `loadAndVectorize` Function

- Navigate to `./Blobs/loadAndVectorize`.
- Find the section labeled "# Product indexList" and replace it with the provided code snippet.

CODE HERE


This code snippet specifies the vector indexes to be created based on our vector columns.

#### Update `createVectorIndexes` Function

- Navigate to `./SearchComponents/indexes`.
- Replace the `createVectorIndexes` function with the provided code snippet.

CODE HERE

This function creates an IVF vector index for our vector columns, enabling efficient vector searches.

## Performing Vector Searches

### Update `runVectorSearch` Function

- Navigate to `./SearchComponents/searches`.
- Replace the `runVectorSearch` function with the provided code snippet.

CODE HERE


This function prompts for a search query, generates embeddings, and searches the vector index for matching documents.

### Update `vectorSearch` Function

- Navigate to `./SearchComponents/vectorSearch`.
- Replace the `vectorSearch` function with the provided code snippet.

CODE HERE

Utilizes the generated embeddings to search the Cosmos DB vector index for similar documents based on the query prompt.

## Integrating GPT-3 for Enhanced Search Results

### Update `runGPTSearch` Function

- Navigate to `./SearchComponents/searches`.
- Replace the `runGPTSearch` function with the provided code snippet.

CODE HERE


After obtaining vector search results, this function further processes them with GPT-3 to generate more detailed, human-readable insights.

### Update `generateCompletion` Function

- Navigate to `./SearchComponents/completion`.
- Replace the `generateCompletion` function with the provided code snippet.

CODE HERE

This function constructs prompts for GPT-3 based on vector search results, generating comprehensive and understandable responses.

## Running the Application

After completing the setup and configuration steps, you're now ready to explore the capabilities of vector search combined with Azure OpenAI. Here's how to run the application and test out its features:

1. **Launch the Application**: Navigate to the root directory of your project in the integrated terminal within Visual Studio Code. Enter the command to start the application. The specific command will be provided later.

    ```
    Placeholder for code
    ```

2. **Interact with the Menu**: Upon starting the application, you'll be presented with a menu of options:
    - **Option 1**: Download data from Azure Blob Storage, load it into the database, and create the vector index.
    - **Option 2**: Load local data into MongoDB and create vector index.
    - **Option 3**: Run a Vector Search.
    - **Option 4**: Conduct a GPT-3 enhanced vector search.

3. **Prepare your database**: Choose either option 1 or 2 to load data into the database and create the vector index. This step is essential for performing searches.

    - **Option 1**: Download data from Azure Blob Storage, load it into the database, and create the vector index.
    - **Option 2**: Load local data into MongoDB and create vector index.

    After selecting one of these options, the application will guide you through the process of loading data and creating the vector index.

4. **Conduct Vector Search**:
   - First, select **Option 3** to perform a vector search. Use the query "What color bikes do you sell?" to see how the system responds with a list of products and their similarity scores. This will help you understand how vector search results, while powerful, might require additional processing or coding to fully interpret and utilize the results.

5. **Conduct GPT-3 Enhanced Vector Search**:
   - After evaluating the results from Option 3, proceed with **Option 4** for a GPT-3 enhanced vector search using the same query "What color bikes do you sell?". This step demonstrates how integrating with GPT-3 can provide richer and more human-readable insights from the vector search results, making the data more accessible and understandable without the need for further complex processing.

6. **Experiment with Queries**: Utilize the following queries to test the system's response and then, using option 4, run as many queries as you can think of:
    - What is the biggest bike you sell?
    - Can you recommend some accessories for my bike?
    - I need some biking clothing, what do you have?

By experimenting with various queries, you'll gain insights into how the system processes and understands your requests, showcasing the power of combining vector search with GPT-3 for enhanced data interaction and discovery.

## Clean Up

After completing the lab exercises, it's important to clean up any resources you've created to avoid incurring unnecessary costs. Here's how:

1. **Azure Portal**: Log in to the [Azure Portal](https://portal.azure.com).

2. **Delete Resource Group**: If you created a new resource group for this lab, navigate to "Resource groups", find your group, and delete it. This action removes all the resources contained within it, including your Azure Cosmos DB instance and any Azure OpenAI resources.

    ```
    Placeholder for code
    ```

3. **Manually Delete Individual Resources**: If you added resources to an existing group, you need to delete each resource individually. Navigate to each resource created for this lab (e.g., Azure Cosmos DB for MongoDB, Azure OpenAI account) and delete them.

    ```
    Placeholder for code
    ```

4. **Verify Deletion**: Ensure all resources are no longer listed in your Azure Portal to confirm they've been successfully removed.

5. **Review Billing**: Check your Azure billing section to ensure no unexpected charges are incurred, verifying that all unwanted resources have been successfully deleted.

This cleanup process helps maintain your Azure account organized and free from unnecessary charges, ensuring you only pay for resources you actively use.
