// Import the required modules
const VectorSearch = require('../SearchComponents/vectorSearch');
const Completion = require('../SearchComponents/completion');

function vectorSearchPrompt() {
    return "What would you like to know about our bike shop's inventory?";
}

function GPTSearchPrompt() {
    return "What would you like to ask about our bike shop's inventory? Type 'end' to end the session.";
}

// Asynchronous function to run a vector search
async function runVectorSearch(embeddingsDeployment, AzureOpenAIClient, client, cosmosDbMongodbDatabase, userInput) {

    // Define the maximum number of results, the vector column, and the collection name
    const maxResults = 20;
    const vectorColumn = "productVector";
    const collectionName = "products";

    // Connect to the database and get the collection
    const db = client.db(cosmosDbMongodbDatabase);
    const collection = db.collection(collectionName);
    
    // Run the vector search and return the results
    let resultArray = [];
    const results = await VectorSearch.vectorSearch(userInput, vectorColumn, collection, embeddingsDeployment, AzureOpenAIClient, maxResults);
    for (let result of results) {
        resultArray.push(`Similarity Score: ${result.similarityScore}, category: ${result.document.categoryName}, Product: ${result.document.name}`);
    }
    return resultArray;
}

// Asynchronous function to run a GPT-3 search
async function runGPTSearch(embeddingsDeployment, AzureOpenAIClient, completionDeployment, client, cosmosDbMongodbDatabase, userInput) {

    // Define the maximum number of results, the vector column, and the collection name
    const maxResults = 20;
    const vectorColumn = "productVector";
    const collectionName = "products";

    // Connect to the database and get the collection
    const db = client.db(cosmosDbMongodbDatabase);
    const collection = db.collection(collectionName);

    // Run the vector search
    const resultsForPrompt = await VectorSearch.vectorSearch(userInput, vectorColumn, collection, embeddingsDeployment, AzureOpenAIClient, maxResults);

    // Generate completions based on the vector search results
    const completionsResults = await Completion.generateCompletion(resultsForPrompt, completionDeployment, AzureOpenAIClient, userInput);
    return completionsResults.choices[0].message.content;
}

// Export functions
module.exports.runVectorSearch = runVectorSearch;
module.exports.runGPTSearch = runGPTSearch;
module.exports.vectorSearchPrompt = vectorSearchPrompt;
module.exports.GPTSearchPrompt = GPTSearchPrompt;