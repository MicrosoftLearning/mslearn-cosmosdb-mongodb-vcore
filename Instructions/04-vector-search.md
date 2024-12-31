---
lab:
    title: 'Building an AI copilot using vCore-based Azure Cosmos DB for MongoDB vector search and Azure OpenAI'
    module: 'Module 4 - Use Azure AI OpenAI and vector search to create AI copilots with vCore-based Azure Cosmos DB for MongoDB'
---

In this lab, you use Azure OpenAI to create embeddings for vCore-based Azure Cosmos DB for MongoDB documents, establishing your AI copilot for advanced data exploration. You build a vector index from these embeddings, allowing you to create vector searches. The vector searches involves generating an embedding for user prompts, using those user prompt embeddings to find similar documents in the database through a vector search, and enhancing the search results deploying an Azure OpenAI GPT-3.5 chat. This process illustrates a Retrieval-Augmented Generation (RAG) approach, mixing AI with database technologies to refine search results and responses.

### Objectives

- Load data from Azure Blob Storage to a local directory.
- Import data into vCore-based Azure Cosmos DB for MongoDB, generating embeddings for *category* and *name* fields of each product during the process.
- Create a Vector index on the generated vector column.
- Perform vector searches using prompts and display the closest matching products.
- Use GPT-3.5 to enhance vector search results, enabling your AI copilot to provide more detailed insights.

These objectives showcase the practical use of the Retrieval-Augmented Generation (RAG) approach, combining vector search accuracy with the depth provided by GPT-3.5 insights.

### Build your own lab environment

If you need to build your own lab environment, you need the following components and resource access.

- **Visual Studio Code**: Ensure Visual Studio Code is installed on your machine.
- **Azure Subscription**: Have access to an Azure Subscription for creating and using the necessary resources:
  - **vCore-based Azure Cosmos DB for MongoDB**: Access to create or use an existing a vCore-based Azure Cosmos DB for MongoDB account.
  - **Azure OpenAI Account**: Access to create or use an existing Azure OpenAI account.
  - **Azure OpenAI Deployments**: Access to create deployments for embeddings and completions in your Azure OpenAI account.

## Clone the Repository

1. Open **Visual Studio Code**.
1. Press **CTRL+SHIFT+P** to open the command palette.
1. Run +++**Git: Clone**+++ and clone the repository +++https://github.com/MicrosoftLearning/mslearn-cosmosdb-mongodb-vcore.git+++.
1. Navigate to the cloned repository directory.
1. Right-click on the **04-vector-search** folder and select **Open in integrated Terminal**.

## Create Azure Resources

To support your AI copilot, you need access to the following Azure resources for this lab:

- vCore-based Azure Cosmos DB for MongoDB account
- Azure OpenAI account, including deployments for embeddings and completions

You can create these resources via the *Azure portal* or use the ***create-azure-resources.ps1*** PowerShell script with the ***.env** file. Don't use existing production resources for this lab or any lab.

### Use the .env file

*This file must either be populated manually, or by the create-azure-resources.ps1 script before you can run your application, since it contains the connection information to your Azure resources.*

This file is both used to retrieve and store the necessary environment variables for both the PowerShell script and the vector search application APIs. It's the easiest way to prepopulate your resource information. The file is used to store the environment variables for your vCore-based Azure Cosmos DB for MongoDB and Azure OpenAI account.

If you already have an existing Resource Group, a vCore-based Azure Cosmos DB for MongoDB account, or an Azure OpenAI account that you would like to use, just fill in those values in the .env file and set the skip create option for that resource to **true**. By default, the *create-azure-resources.ps1* script uses this file to retrieve the necessary environment variables. The *create-azure-resources.ps1* script populates the environment variables with default values if not specified in the .env file.

To learn more about the ***.env*** file and its parameters, review the [***.env*** file documentation](./00-env-file.md).

### Use the create-azure-resources.ps1 script

>[!note]
> You don't need to run the *create-azure-resources.ps1* script and can skip to the next section if you already have the necessary Azure resources created.

If you aren't using existing resources, or you aren't creating them through the Azure portal, this script creates the necessary Azure resources for this lab. It gives you the flexibility to create some or all of the resources required for this lab. You can either run the script as is or modify it to suit your needs. The resources created by the script include:

- Resource Group
- vCore-based Azure Cosmos DB for MongoDB account
- Azure OpenAI account
- Azure OpenAI deployments for embeddings
- Azure OpenAI deployments for completions

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
> The vCore-based Azure Cosmos DB for MongoDB account will need a firewall rule to allow access from your current public IP address.  If your vCore-based Azure Cosmos DB for MongoDB account was generated by the *create-azure-resources.ps1* script, it should have created the firewall rule for you.  Check the existing firewall rules under the ***Networking*** *Setting* section of the *vCore-based Azure Cosmos DB for MongoDB Account*.  If you are not sure what your current public IP address is, you can use the following command to find out:
> ```powershell
> Invoke-RestMethod -Uri 'http://ipinfo.io/ip' -Method Get
> ```

Once the resources are created and your **.env** file is populated with the resource information, you can proceed to the next step.

## Implement a vector search

Setting up our environment and implementing the necessary functionality prepares our AI copilot for effective vector searches. This setup includes loading data into the database, generating embeddings for the documents, and creating a vector index.

### Create the document embeddings

In this lab, you focus on the **products** collection. You generate embeddings for the *category* + *name* fields of each product.

#### Update the generateProductEmbedding function

Let's first choose the fields to generate embeddings for and then call Azure OpenAI to generate these embeddings.

- In VS Code, open the file **./[language]/Collections/products** (with a .js or .py extension for the file's respective language).
- On the **generateProductEmbedding** function, replace the line with the comment *Replace this line with the lab's code* with the provided code snippet, and **Save**.

<details>
<summary>Python</summary>

```python
    # Construct the product name by concatenating the category name and product name
    productName = "Category - " + product["categoryName"] + ", Name -" + product["name"]

    # If the product name exists
    if productName:
        # Generate embeddings for the product name
        product["productVector"] = Embeddings.generateEmbeddings (productName,embeddings_deployment,AzureOpenAIClient)

    # Return the product data with the generated embeddings
    return product
```

</details>

<details>
<summary>Node.js</summary>

```javascript
    // Construct a string representing the product's name and category
    const productName = "Category - " + product["categoryName"] + ", Name -" + product["name"];
    
    // If the productName exists, generate an embedding for it
    if (productName) {
        // The embedding is generated using the Embeddings module's generateEmbeddings function
        // The resulting embedding is stored in the product object under the key "productVector"
        product["productVector"] = await Embeddings.generateEmbeddings(productName, embeddingsDeployment, AzureOpenAIClient);
    }

    // Return the product object with the added embedding
    return product;
```

</details>

This function selects fields to generate embeddings for, calls Azure OpenAI to generate these embeddings, and stores them in a vector column in the database.

#### Update the generateEmbeddings function

Time to generate the embeddings for a string. In this case, for your products' name + category.

- In VS Code, open the file **./[language]/SearchComponents/embeddings** (with a .js or .py extension for the file's respective language).
- On the **generateEmbeddings** function, replace the line with the comment *Replace this line with the lab's code* with the provided code snippet, and **Save**.

<details>
<summary>Python</summary>

```python
    # Generate embeddings from string of text.
    # This will be used to vectorize data and user input for interactions with Azure OpenAI.
    # Call the create method of the AzureOpenAIClient's embeddings object to generate embeddings for the input text
    response = AzureOpenAIClient.embeddings.create(
        input=text
        , model=embeddings_deployment)
    
    # Parse the response into a json object
    embeddings = json.loads(response.model_dump_json(indent=2))
    
    # Sleep for 0.01 seconds to avoid rate limiting
    # If using the free tier of Azure OpenAI, you may need to increase this to 0.5 seconds
    time.sleep(0.01)
    
    # Return the embedding from the response
    return embeddings["data"][0]["embedding"]
```

</details>

<details>
<summary>Node.js</summary>

```javascript
    //Generate embeddings from string of text.
    //This will be used to vectorize data and user input for interactions with Azure OpenAI.
    // Use the async-retry module to attempt the following code block
    // If an error occurs, it will retry up to 10 times, with an increasing timeout between each attempt
    return await retry(async bail => {
        try {
            // Call the Azure OpenAI Client's getEmbeddings function with the embeddings deployment and text
            // Await the response and store it in the response variable
            const response = await AzureOpenAIClient.embeddings.create({ input: text, model: embeddingsDeployment });

            // Extract the embeddings from the response data
            const embeddings = response.data[0].embedding;
            // Wait for 10 milliseconds to avoid rate limiting (change to 500 on AOAI for free tier)
            await new Promise(resolve => setTimeout(resolve, 10));
            // Return the embeddings
            return embeddings;
        } catch (err) {
            // If a 429 error (Too Many Requests) is received, rethrow the error to trigger a retry
            if (err.response && err.response.status === 429) {
                throw err;
            } else {
                // For any other error, stop retrying and throw the error
                bail(err);
            }
        }
    }, {
        retries: 10, // Maximum number of retries
        minTimeout: 1000, // Minimum timeout between retries (1 second)
        factor: 2, // Factor by which the timeout increases each time
        maxTimeout: 20000 // Maximum timeout between retries (20 seconds)
    });
```

</details>

This function uses the Azure OpenAI embeddings function to generate embeddings for any given string. These embeddings are sent back to be stored in your vector columns or used in your vector searches.

The process of generating embeddings for the MongoDB documents using Azure OpenAI, sets the stage for RAG by optimizing the data for both retrieval and generative analysis.

### Generate the vector index

Just creating a vector column with the respective embeddings isn't enough. You need to create a vector index on that column to enable your vector searches.

#### Update the loadAndVectorize function

Now you create the vector indexes for the collection based on our vector columns. In this function, you choose which vector columns and index names need to be created.

- In VS Code, open the file **./[language]/Blobs/loadAndVectorize** (with a .js or .py extension for the file's respective language).
- Towards the bottom of the **loadAndVectorizeLocalBlobDataToMongoDBCluster** function, replace the line with the comment *Replace this line with the lab's code* with the provided code snippet, and **Save**.

<details>
<summary>Python</summary>

```python
                # Create the vector indexes for the collection
                if (process_customers_vector and collection_name == "customers"):
                    index_list = [
                                    ("customerTypeVectorSearchIndex", "customerTypeVector")
                                    , ("customerTitleVectorSearchIndex", "customerTitleVector")
                                    , ("customerNameVectorSearchIndex", "customerNameVector")
                                    , ("customerEmailAddressVectorSearchIndex", "customerEmailAddressVector")
                                    , ("customerPhoneNumberVectorSearchIndex", "customerPhoneNumberVector")
                                    , ("customerAddressesVectorSearchIndex", "customerAddressesVector")
                                ]
                    Indexes.createVectorIndexes(collection, index_list, db, collection_name)

                elif (process_products_vector and collection_name == "products"):
                    index_list = [
                                    ("productVectorSearchIndex", "productVector")
                                ]
                    Indexes.createVectorIndexes(collection, index_list, db, collection_name)

                elif (process_sales_orders_vector and collection_name == "salesOrders"):
                    index_list = [
                                    ("salesOrderDetailVectorSearchIndex", "salesOrderDetailVector")
                                ]
                    Indexes.createVectorIndexes(collection, index_list, db, collection_name)
```

</details>

<details>
<summary>Node.js</summary>

```javascript
                // Create the vector indexes for the collection
                if (processCustomersVector && collectionName === "customers") {
                    indexList = [
                        ["customerTypeVectorSearchIndex", "customerTypeVector"],
                        ["customerTitleVectorSearchIndex", "customerTitleVector"],
                        ["customerNameVectorSearchIndex", "customerNameVector"],
                        ["customerEmailAddressVectorSearchIndex", "customerEmailAddressVector"],
                        ["customerPhoneNumberVectorSearchIndex", "customerPhoneNumberVector"],
                        ["customerAddressesVectorSearchIndex", "customerAddressesVector"]
                    ];
                    await Indexes.createVectorIndexes(collection, indexList, db, collectionName);
                } else if (processProductsVector && collectionName === "products") {
                    indexList = [
                        ["productVectorSearchIndex", "productVector"]
                    ];
                    await Indexes.createVectorIndexes(collection, indexList, db, collectionName);
                } else if (processSalesOrdersVector && collectionName === "salesOrders") {
                    indexList = [
                        ["salesOrderDetailVectorSearchIndex", "salesOrderDetailVector"]
                    ];
                    await Indexes.createVectorIndexes(collection, indexList, db, collectionName);
                }
```

</details>

This function has multiple purposes. It loops through all the local data files, extract their documents, if needed calls a function to create embeddings on those documents, and saves the documents to the database. But more to the point of this lab, it also calls a function to create the vector indexes for the collections based on the vector columns.

#### Update the createVectorIndexes function

Now that you know what vector columns and vector index names you want to create, let's update the function that creates the indexes themselves. There are two types of vector indexes that can be created, IVF (Inverted File index), and HNSW (Hierarchical Navigable Small World index). For this lab, you're creating IVF indexes.

- In VS Code, open the file **./[language]/SearchComponents/indexes** (with a .js or .py extension for the file's respective language).
- In the **createVectorIndexes** function, replace the line with the comment *Replace this line with the lab's code* with the provided code snippet, and **Save**.

<details>
<summary>Python</summary>

```python
    # Get information about the existing indexes in the collection
    collection_indexes = collection.index_information()    

    # Iterate over each index in the index_list
    for indexname, vectorColumn in index_list:
        # Iterate over each index in the collection indexes
        for index in collection_indexes:
            # If the index already exists in the collection
            if index == indexname:
                # Drop the existing index
                collection.drop_index(indexname)
                break
        
            # Create a new IVF index in the collection
            # The index is created using the MongoDB command function
            # The command specifies the collection to create the index in, the name of the index, 
            # the key to index on, and the options for the CosmosDB search        
            db.command({
            'createIndexes': collection_name,
            'indexes': [
                {
                'name': indexname,
                'key': {
                    f"{vectorColumn}": "cosmosSearch"
                },
                'cosmosSearchOptions': {
                    'kind': 'vector-ivf',
                    'numLists': 1,
                    'similarity': 'COS',
                    'dimensions': 1536
                }
                }
            ]
            })
```

</details>

<details>
<summary>Node.js</summary>

```javascript
    // Get the current indexes in the collection
    const collectionIndexes = await collection.indexInformation();

    // Iterate over each index in the indexList
    for (let [indexName, vectorColumn] of indexList) {
        // Iterate over each index in the collection
        for (let index of Object.keys(collectionIndexes)) {
            // If the index already exists in the collection, drop it
            if (index === indexName) {
                await collection.dropIndex(indexName);
                break;
            }
        }

        // Create a new IVF index in the collection
        // The index is created using the MongoDB command function
        // The command specifies the collection to create the index in, the name of the index, 
        // the key to index on, and the options for the CosmosDB search
        const commandResult = await db.command({
            'createIndexes': collectionName,
            'indexes': [
                {
                    'name': indexName,
                    'key': {
                        [vectorColumn]: "cosmosSearch"
                    },
                    'cosmosSearchOptions': {
                        'kind': 'vector-ivf',
                        'numLists': 1,
                        'similarity': 'COS',
                        'dimensions': 1536
                    }
                }
            ]
        });
    }
```

</details>

This function first drops the index if it already exists, then creates a new IVF index in the collection based on the vector column and index name provided. It creates the index using the MongoDB **command** function.

## Perform vector searches

It's time to perform vector searches using the generated embeddings and vector indexes. Later, you enhance the vector search results with GPT-3.5.

### Update the runVectorSearch function

Since in this lab you only created a vector index on the **products'** collection, let's prepare your vector search specifically for that collection.

- In VS Code, open the file **./[language]/SearchComponents/searches** (with a .js or .py extension for the file's respective language).
- In the **runVectorSearch** function, replace the line with the comment *Replace this line with the lab's code* with the provided code snippet, and **Save**.

<details>
<summary>Python</summary>

```python
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Ask the user for their query
    print("What would you like to know about our bike shop's inventory?")
    user_input = input("Prompt: ")
    
    # Define the maximum number of results, the vector column name, and the collection name
    maxResults = 20
    vector_column = "productVector"
    collection_name = "products"

    # Connect to the database and the collection
    db = client[cosmos_db_mongodb_database]
    collection = db[collection_name]
    
    # Run the vector search and print the results
    results = VectorSearch.vectorSearch(user_input, vector_column, collection, embeddings_deployment, AzureOpenAIClient, maxResults)
    for result in results: 
        print(f"Similarity Score: {result['similarityScore']}"
              + f", category: {result['document']['categoryName']}" 
              + f", Product: {result['document']['name']}")  
```

</details>

<details>
<summary>Node.js</summary>

```javascript
    // Clear the console and ask the user for input
    console.clear();
    console.log("What would you like to know about our bike shop's inventory?");
    // read the user input for a new prompt
    const userInput = await new Promise(resolve => rl.question("Prompt: ", resolve));
    // Define the maximum number of results, the vector column, and the collection name
    const maxResults = 20;
    const vectorColumn = "productVector";
    const collectionName = "products";

    // Connect to the database and get the collection
    const db = client.db(cosmosDbMongodbDatabase);
    const collection = db.collection(collectionName);
    // Run the vector search and print the results
    const results = await VectorSearch.vectorSearch(userInput, vectorColumn, collection, embeddingsDeployment, AzureOpenAIClient, maxResults);
    for (let result of results) {
        console.log(`Similarity Score: ${result.similarityScore}, category: ${result.document.categoryName}, Product: ${result.document.name}`);
    }
```

</details>

This function prompts for a search query and calls a function to generate embeddings of that prompt and search the vector index for similar documents. It then displays the results to the console including a similarity score.

### Update the vectorSearch function

Let's now update the function that performs the vector search itself.

- In VS Code, open the file **./[language]/SearchComponents/vectorSearch** (with a .js or .py extension for the file's respective language).
- In the **vectorSearch** function, replace the line with the comment *Replace this line with the lab's code* with the provided code snippet, and **Save**.

<details>
<summary>Python</summary>

```python
    # Generate embeddings for the query using the generateEmbeddings function from the embeddings module
    query_embedding = Embeddings.generateEmbeddings(query,embeddings_deployment,AzureOpenAIClient)

    # Define the pipeline for the MongoDB aggregation query
    pipeline = [
                {
                    # The $search stage performs a search query on the collection
                    '$search': {
                        # The cosmosSearch operator performs a vector search
                        "cosmosSearch": {
                            # The vector to search for
                            "vector": query_embedding,
                            # The path in the documents where the vector data is stored
                            "path": vector_column,
                            # The number of results to return
                            "k": num_results 
                        },
                        # Return the original document in the results
                        "returnStoredSource": True }},
                # The $project stage includes or excludes fields from the documents
                {'$project': { 
                    # Include the similarity score in the results
                    'similarityScore': { '$meta': 'searchScore' }, 
                    # Include the original document in the results
                    'document' : '$$ROOT' } }
            ]
    # Perform the aggregation query on the collection and store the results
    results = collection.aggregate(pipeline)
    # Return the results
    return results
```

</details>

<details>
<summary>Node.js</summary>

```javascript
    // Generate embeddings for the query using the Embeddings module
    const queryEmbedding = await Embeddings.generateEmbeddings(query, embeddingsDeployment, AzureOpenAIClient);

    // Define the aggregation pipeline for the MongoDB query
    // The pipeline first performs a search using the generated embeddings and the specified vector column
    // It then projects the results to include the similarity score and the original document
    const pipeline = [
        {
            '$search': {
                "cosmosSearch": {
                    "vector": queryEmbedding,
                    "path": vectorColumn,
                    "k": numResults
                },
                "returnStoredSource": true
            }
        },
        { '$project': { 'similarityScore': { '$meta': 'searchScore' }, 'document': '$$ROOT' } }
    ];

    // Execute the aggregation pipeline on the collection and convert the results to an array
    const results = await collection.aggregate(pipeline).toArray();
    // Return the results
    return results;
```

</details>

The interesting part of this function is that to create the embeddings of the user prompt, it calls the same ***generateEmbeddings*** function that was earlier used to generate the embeddings for the document columns. This is because you generate embeddings for any string, what you do with the generated embedding is up to you (store it, search on it). It then uses the generated embeddings to perform a vector search on the collection and returns the results. Note how the function uses a MongoDB **aggregation** pipeline to perform the search.

## Integrate GPT-3.5 for enhanced search results

Vector search results can be powerful, but they might require extra coding to fully interpret and utilize the results. To address this issue, you can integrate GPT-3 to provide more detailed, human-readable insights from the vector search results.

### Update the runGPTSearch function

Setting up this function, just like the ***runVectorSearch*** function, readies your AI copilot to draw on deeper insights for the **products'** collection.

- In VS Code, open the file **./[language]/SearchComponents/searches** (with a .js or .py extension for the file's respective language).
- In the **runGPTSearch** function, replace the line with the comment *Replace this line with the lab's code* with the provided code snippet, and **Save**.

<details>
<summary>Python</summary>

```python
    # Define the maximum number of results, the vector column name, and the collection name
    maxResults = 20
    vector_column = "productVector"
    collection_name = "products"

    # Connect to the database and the collection
    db = client[cosmos_db_mongodb_database]
    collection = db[collection_name]

    # Clear the console and ask the user for their query
    user_input = ""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("What would you like to ask about our bike shop's inventory? Type 'end' to end the session. ")
    user_input = input("Prompt: ")
    
    # Keep asking for queries until the user types 'end'
    while user_input.lower() != "end":
        # Run the vector search and generate completions
        results_for_prompt = VectorSearch.vectorSearch(user_input, vector_column, collection, embeddings_deployment, AzureOpenAIClient, maxResults)
        completions_results = Completion.generateCompletion(results_for_prompt,completion_deployment,AzureOpenAICompletionClient,user_input)
        
        # Print the completions
        print("\n"+completions_results['choices'][0]['message']['content'])

        # Ask for the next query
        print("\nWhat would you like to ask about our bike shop's inventory? Type 'end' to end the session. ")
        user_input = input("Prompt: ")
```

</details>

<details>
<summary>Node.js</summary>

```javascript
    // Define the maximum number of results, the vector column, and the collection name
    const maxResults = 20;
    const vectorColumn = "productVector";
    const collectionName = "products";

    // Connect to the database and get the collection
    const db = client.db(cosmosDbMongodbDatabase);
    const collection = db.collection(collectionName);

    // Initialize the user input variable
    let userInput = "";
    // Clear the console and ask the user for input
    console.clear();
    console.log("What would you like to ask about our bike shop's inventory? Type 'end' to end the session. ");
    userInput = await new Promise(resolve => rl.question("Prompt: ", resolve));
    // Continue asking for input until the user types 'end'
    while (userInput.toLowerCase() !== "end") {
        // Run the vector search
        const resultsForPrompt = await VectorSearch.vectorSearch(userInput, vectorColumn, collection, embeddingsDeployment, AzureOpenAIClient, maxResults);

        // Generate completions based on the vector search results
        const completionsResults = await Completion.generateCompletion(resultsForPrompt, completionDeployment, AzureOpenAIClient, userInput);
        // Print the first completion result
        console.log("\n" + completionsResults.choices[0].message.content);

        // Ask the user for more input
        console.log("\nWhat would you like to ask about our bike shop's inventory? Type 'end' to end the session. ");
        userInput = await new Promise(resolve => rl.question("Prompt: ", resolve));
    }
```

</details>

Like the *runVectorSearch* function, this function asks you for your prompt to run against the vector index. However, after obtaining vector search results, this function further call a function to process those results with GPT-3.5 to generate more detailed, human-readable insights.

### Update the generateCompletion function

Using GPT-3.5 to enhance search results brings our RAG process full circle. It turns basic data searches into detailed, interactive conversations, demonstrating the power of combining database technology with AI.

Let's turn those vector search results into more comprehensive and understandable responses using GPT-3.5.

- In VS Code, open the file **./[language]/SearchComponents/completion** (with a .js or .py extension for the file's respective language).
- In the **generateCompletion** function, replace the line with the comment *Replace this line with the lab's code* with the provided code snippet, and **Save**.

<details>
<summary>Python</summary>

```python
    # Define the system prompt
    system_prompt = '''
    You are an intelligent assistant for the Adventure Works Bike Shop.
    You are designed to provide helpful answers to user questions about the store inventory given the information about to be provided.
        - Only answer questions related to the information provided below, provide 3 clear suggestions in a list format.
        - Write two lines of whitespace between each answer in the list.
        - Only provide answers that have products that are part of the Adventure Works Bike Shop.
        - If you're unsure of an answer, you can say ""I don't know"" or ""I'm not sure"" and recommend users search themselves."
    '''

    # Initialize the messages list with the system prompt and user input
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ]
    
    # Add each item in the prompt to the messages list
    for item in prompt:
        messages.append({"role": "system", "content": item['document']['categoryName']+" "+item['document']['name']})
    
    # Generate the chat completions using the AzureOpenAICompletionClient
    response = AzureOpenAICompletionClient.chat.completions.create(model=completion_deployment, messages=messages)
    
    # Parse the response into a json object
    completions = json.loads(response.model_dump_json(indent=2))

    # Return the completions
    return completions
```

</details>

<details>
<summary>Node.js</summary>

```javascript
    // Define the system prompt that sets the context for the AI
    const systemPrompt = `
    You are an intelligent assistant for the Adventure Works Bike Shop.
    You are designed to provide helpful answers to user questions about the store inventory given the information about to be provided.
        - Only answer questions related to the information provided below, provide 3 clear suggestions in a list format.
        - Write two lines of whitespace between each answer in the list.
        - Only provide answers that have products that are part of the Adventure Works Bike Shop.
        - If you're unsure of an answer, you can say "I don't know" or "I'm not sure" and recommend users search themselves.
    `;

    // Initialize the messages array with the system prompt and user input
    let messages = [
        {role: "system", content: systemPrompt},
        {role: "user", content: userInput},
    ];

    // Add each item from the prompt to the messages array
    for (let item of prompt) {
        messages.push({role: "system", content: `${item.document.categoryName} ${item.document.name}`});
    }

    // Call the Azure OpenAI Completion Client's getChatCompletions function with the completion deployment and messages
    // Await the response and store it in the response variable
    const response = await AzureOpenAICompletionClient.chat.completions.create({ messages: messages, model: completionDeployment });
    
    // Return the response
    return response;
```

</details>

This function has three sets of prompts. The first is a system prompt (***systemPrompt***) that sets the context for the AI, or in other words, who is the AI supposed to be, and what parameters/rules it should follow. The second is the user's input (**userInput***), which is the question or prompt we asked. The third is the an array of results from the vector search (**prompt**) on that same previous question or prompt we asked. It then calls the Azure OpenAI Chat Completions function to generate completions based on those prompts.

Moving from conducting vector searches to improving results with GPT-3.5 chat highlights the RAG method, seamlessly integrating precise data search with AI-driven conversational insights.

## Running the Application

After completing the setup and configuration steps, you're now ready to explore the capabilities of vector search combined with Azure OpenAI. Here's how to run the application and test out its features:

>[!note]
> Make sure you have the necessary environment variables in your **.env** file before running the application.  

>[!note]
> Make sure you have the vCore-based Azure Cosmos DB for MongoDB account firewall rules set to allow access from your current public IP address.  

1. **Launch the Application**: Navigate to the root directory of your project in the integrated terminal within Visual Studio Code. To start the application, enter the following commands.

    <details>
    <summary>Python</summary>
    
    ```powershell
    cd ./python
    py -m pip install -v "pymongo==4.6.2"
    py -m pip install -v "openai==1.13.3" 
    py -m pip install -v "tenacity==9.0.0"
    py -m pip install -v "azure-storage-blob==12.23.1"
    py load-and-vectorize-data.py
    ```
    </details>
    
    <details>
    <summary>Node.js</summary>
    
    ```powershell
    cd ./node.js
    npm install
    npm install openai
    npm start
    ```

    </details>

1. **Interact with the Menu**: Upon starting the application, you're presented with a menu of options:
    - **Option 1**: Download data from Azure Blob Storage, load it into the database, and create the vector index.
    - **Option 2**: Load local data into MongoDB and create vector index.
    - **Option 3**: Run a Vector Search.
    - **Option 4**: Conduct a GPT-3 enhanced vector search.

1. **Prepare your database**: Choose either option 1 or 2 to load data into the database and create the vector index. This step is essential for performing searches.

    - **Option 1**: Download data from Azure Blob Storage, load it into the database, and create the vector index.
    - **Option 2**: Load local data into MongoDB and create vector index.

    Let's select **Option 1**. The application guides you through the process of loading data and creating the vector index.

1. **Conduct Vector Search**:
   - Select **Option 3** to perform our first vector search and enter the following query:

        ***What are your bikes' colors?***

    Review the results of this query to help you understand how vector search results, while powerful, might require extra coding to fully interpret and utilize the results.

1. **Conduct GPT-3 Enhanced Vector Search**:
   - After evaluating the results from *Option 3*, proceed with **Option 4** for a GPT-3.5 enhanced vector search using the same query ***What are your bikes' colors***. This step demonstrates how integrating with GPT-3.5 can provide richer and more human-readable insights from the vector search results. GPT-3.5 makes the data more accessible and understandable without the need for further complex coding.

1. **Experiment with Queries**: Utilize the following queries to test the system's response and then, using option 4, run as many queries as you can think of:
    - What is the biggest bike you sell?
    - Can you recommend some accessories for my bike?
    - I need some biking clothing, what do you have?

Even running the same query multiple times can yield different results, demonstrating the power of GPT-3.5 in providing more detailed insights.

## Clean Up

After completing the lab exercises, it's important to clean up any resources you created to avoid incurring unnecessary costs. Here's how:

1. **Azure Portal**: Sign in to the Azure portal.

1. **Delete Resource Group**: If you created a new resource group for this lab, navigate to *Resource groups*, find your group, and delete it. This action removes all the resources contained within it, including your Azure Cosmos DBvCore-based Azure Cosmos DB for MongoDB account and any Azure OpenAI resources.

1. **Manually Delete Individual Resources**: If you added resources to an existing group, you need to delete each resource individually. Navigate to each resource created for this lab (for example, vCore-based Azure Cosmos DB for MongoDB account, Azure OpenAI account) and delete them.

1. **Verify Deletion**: Confirm all resources you no longer need were successfully removed and are no longer listed in your Azure portal.

1. **Review Billing**: Check your Azure billing section to ensure no unexpected charges are incurred, verifying that all unwanted resources were successfully deleted.

This cleanup process helps maintain your Azure account organized and free from unnecessary charges, ensuring you only pay for resources you actively use.

# Conclusion

In this lab, you employed Azure OpenAI to generate embeddings for vCore-based Azure Cosmos DB for MongoDB documents and built a vector index for in-depth searches, effectively integrating these tools as your AI copilot. By transforming user prompts into embeddings to search for similar documents in the database, and then enhancing these search outcomes using GPT-3.5 chat from Azure OpenAI, you effectively demonstrated a Retrieval-Augmented Generation (RAG) approach. This step shows how integrating AI with database searches can refine the relevance and depth of query results.

This lab not only guided you through the technical steps of implementing vector search and AI enhancements. The lab also illustrated the powerful capabilities of the Retrieval-Augmented Generation (RAG) approach in creating more dynamic, intelligent, and user-friendly data retrieval systems.
